from typing import TYPE_CHECKING
from datetime import datetime, UTC

from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

if TYPE_CHECKING:
    from core.models.product import Product


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC),
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="manufacturer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Manufacturer {self.id}>"
