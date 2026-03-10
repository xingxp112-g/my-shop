from datetime import date, datetime
from typing import Optional

from sqlalchemy import DateTime, Date, DECIMAL, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Voucher(Base):
    __tablename__ = "voucher"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(6), nullable=False, unique=True)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="unused")
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    used_by: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    batch_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
