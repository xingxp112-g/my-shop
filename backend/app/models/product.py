from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, DateTime, Table, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# 多对多中间表（使用 Table，不需要独立 Model）
product_tag_table = Table(
    "product_tag",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("brand.id"), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    remark: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(SmallInteger, default=1, nullable=False)  # 1=上架 0=下架
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")  # noqa: F821
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=product_tag_table)  # noqa: F821
