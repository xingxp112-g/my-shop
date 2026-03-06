from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Brand(Base):
    __tablename__ = "brand"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")  # noqa: F821
