from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tag.id"), nullable=True)

    children: Mapped[list["Tag"]] = relationship(
        "Tag",
        back_populates="parent",
        foreign_keys="Tag.parent_id",
    )
    parent: Mapped["Tag | None"] = relationship(
        "Tag",
        back_populates="children",
        remote_side="Tag.id",
        foreign_keys="Tag.parent_id",
    )
