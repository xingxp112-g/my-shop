from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("")
def get_stats(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    today = date.today()
    month_start = date(today.year, today.month, 1)

    def _query(start: date, end: date):
        result = (
            db.query(func.count(Order.id), func.coalesce(func.sum(Order.total_amount), 0))
            .filter(Order.created_at >= datetime.combine(start, datetime.min.time()))
            .filter(Order.created_at < datetime.combine(end, datetime.max.time()))
            .filter(Order.status != "已取消")
            .one()
        )
        return {"count": result[0], "amount": float(result[1])}

    # 今日：00:00 ~ 23:59
    today_stats = _query(today, today)
    # 本月：月初 ~ 今日
    month_stats = _query(month_start, today)

    return {
        "today_order_count": today_stats["count"],
        "today_order_amount": today_stats["amount"],
        "month_order_count": month_stats["count"],
        "month_order_amount": month_stats["amount"],
    }
