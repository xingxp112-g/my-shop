from typing import Optional
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderOut, OrderDetailOut
from app.utils.auth import get_current_user

router = APIRouter()

VALID_STATUSES = {"待处理", "已确认", "已完成", "已取消"}


def _get_order_or_404(order_id: int, db: Session) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


# ── 前台：提交订单（无需登录）──────────────────────────────────────────────
@router.post("", response_model=OrderDetailOut, status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate, db: Session = Depends(get_db)):
    if not body.items:
        raise HTTPException(status_code=400, detail="订单商品不能为空")

    total = sum(item.price * item.quantity for item in body.items)
    order = Order(
        customer_name=body.customer_name,
        phone=body.phone,
        remark=body.remark,
        total_amount=total,
        status="待处理",
    )
    db.add(order)
    db.flush()  # 获取 order.id

    for item in body.items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
        ))

    db.commit()
    return _get_order_or_404(order.id, db)


# ── 后台：订单列表（需登录）───────────────────────────────────────────────
@router.get("", response_model=list[OrderOut])
def list_orders(
    order_status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    q = db.query(Order)
    if order_status:
        q = q.filter(Order.status == order_status)
    if date_from:
        q = q.filter(Order.created_at >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        q = q.filter(Order.created_at < datetime.combine(date_to + timedelta(days=1), datetime.min.time()))
    return q.order_by(Order.id.desc()).all()


# ── 后台：订单详情 ──────────────────────────────────────────────────────
@router.get("/{order_id}", response_model=OrderDetailOut)
def get_order(order_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    return _get_order_or_404(order_id, db)


# ── 后台：修改订单状态 ───────────────────────────────────────────────────
@router.patch("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"无效状态，可选值：{VALID_STATUSES}")
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    order.status = body.status
    db.commit()
    db.refresh(order)
    return order
