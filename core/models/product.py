from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from core.models.base import Base
from datetime import datetime, UTC

if TYPE_CHECKING:
    from core.models.manufacturer import Manufacturer


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        index=True,
        unique=True,
    )
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.id"),
        index=True,
    )
    year: Mapped[int] = mapped_column(
        index=True,
    )
    cpu: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC),
    )

    manufacturer: Mapped["Manufacturer"] = relationship(
        back_populates="products",
    )
