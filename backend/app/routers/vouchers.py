import io
import random
import string
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.voucher import Voucher
from app.schemas.voucher import (
    VoucherBatchCreate,
    VoucherBatchResponse,
    VoucherListResponse,
    VoucherOut,
    VoucherRedeemRequest,
    VoucherRedeemResponse,
)
from app.utils.auth import get_current_user

router = APIRouter()


# ── 工具函数 ────────────────────────────────────────────────────────────────

def _get_actual_status(v: Voucher) -> str:
    if v.status == "used":
        return "used"
    if v.end_date < date.today():
        return "expired"
    return "unused"


def _to_voucher_out(v: Voucher) -> VoucherOut:
    return VoucherOut(
        id=v.id,
        code=v.code,
        amount=v.amount,
        start_date=v.start_date,
        end_date=v.end_date,
        status=_get_actual_status(v),
        used_at=v.used_at,
        used_by=v.used_by,
        batch_no=v.batch_no,
        created_at=v.created_at,
    )


def _generate_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=6))


def _generate_unique_codes(db: Session, count: int) -> list[str]:
    codes: set[str] = set()
    max_attempts = count * 10
    attempts = 0
    while len(codes) < count and attempts < max_attempts:
        attempts += 1
        code = _generate_code()
        if code in codes:
            continue
        if not db.query(Voucher).filter(Voucher.code == code).first():
            codes.add(code)
    if len(codes) < count:
        raise HTTPException(status_code=500, detail="券码生成失败，请重试")
    return list(codes)


def _make_batch_no() -> str:
    today = datetime.now().strftime("%Y%m%d")
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"BATCH-{today}-{suffix}"


def _build_query(
    db: Session,
    status: Optional[str],
    code: Optional[str],
    amount: Optional[float],
    date_from: Optional[date],
    date_to: Optional[date],
):
    q = db.query(Voucher)
    if status == "used":
        q = q.filter(Voucher.status == "used")
    elif status == "expired":
        q = q.filter(Voucher.status == "unused", Voucher.end_date < date.today())
    elif status == "unused":
        q = q.filter(Voucher.status == "unused", Voucher.end_date >= date.today())
    if code:
        q = q.filter(Voucher.code.like(f"%{code.upper()}%"))
    if amount is not None:
        q = q.filter(Voucher.amount == amount)
    if date_from:
        q = q.filter(Voucher.start_date >= date_from)
    if date_to:
        q = q.filter(Voucher.end_date <= date_to)
    return q


# ── 接口 ────────────────────────────────────────────────────────────────────

@router.post("/batch", response_model=VoucherBatchResponse)
def batch_create(
    body: VoucherBatchCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    batch_no = _make_batch_no()
    codes = _generate_unique_codes(db, body.quantity)
    vouchers = [
        Voucher(
            code=code,
            amount=body.amount,
            start_date=body.start_date,
            end_date=body.end_date,
            batch_no=batch_no,
        )
        for code in codes
    ]
    db.add_all(vouchers)
    db.commit()
    return VoucherBatchResponse(batch_no=batch_no, count=len(codes), codes=codes)


@router.get("", response_model=VoucherListResponse)
def list_vouchers(
    status: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    amount: Optional[float] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    q = _build_query(db, status, code, amount, date_from, date_to)
    total = q.count()
    items = q.order_by(Voucher.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return VoucherListResponse(total=total, items=[_to_voucher_out(v) for v in items])


@router.post("/redeem", response_model=VoucherRedeemResponse)
def redeem_voucher(
    body: VoucherRedeemRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    code = body.code.upper()
    v = db.query(Voucher).filter(Voucher.code == code).first()
    if not v:
        raise HTTPException(status_code=404, detail="券码不存在")
    if v.status == "used":
        used_str = v.used_at.strftime("%Y-%m-%d %H:%M") if v.used_at else "未知时间"
        raise HTTPException(status_code=400, detail=f"该券已于 {used_str} 核销")
    if v.end_date < date.today():
        raise HTTPException(status_code=400, detail=f"该券已于 {v.end_date} 过期")

    # 并发安全：带 status='unused' 条件的更新
    now = datetime.now()
    result = db.execute(
        text(
            "UPDATE voucher SET status='used', used_at=:used_at, used_by=:used_by "
            "WHERE code=:code AND status='unused'"
        ),
        {"used_at": now, "used_by": current_user, "code": code},
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="核销失败，该券可能已被其他操作使用")

    db.refresh(v)
    return VoucherRedeemResponse(code=v.code, amount=v.amount, used_at=now)


@router.get("/export")
def export_vouchers(
    status: Optional[str] = Query(None),
    code: Optional[str] = Query(None),
    amount: Optional[float] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        import openpyxl
    except ImportError:
        raise HTTPException(status_code=500, detail="导出功能不可用，请联系管理员安装 openpyxl")

    q = _build_query(db, status, code, amount, date_from, date_to)
    total = q.count()
    if total > 10000:
        raise HTTPException(status_code=400, detail="结果过多，请缩小筛选范围（最多导出 10000 条）")

    items = q.order_by(Voucher.id.desc()).all()

    status_map = {"used": "已使用", "expired": "已过期", "unused": "未使用"}

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "代金券"
    headers = ["券码", "面额（元）", "有效期开始", "有效期截止", "状态", "核销时间", "批次号"]
    ws.append(headers)

    for v in items:
        actual = _get_actual_status(v)
        ws.append([
            v.code,
            float(v.amount),
            str(v.start_date),
            str(v.end_date),
            status_map.get(actual, actual),
            v.used_at.strftime("%Y-%m-%d %H:%M:%S") if v.used_at else "",
            v.batch_no or "",
        ])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"vouchers_{timestamp}.xlsx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
