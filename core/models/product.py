from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from core.models.base import Base
from core.models.mixins import CreatedUpdatedMixin

if TYPE_CHECKING:
    from core.models.manufacturer import Manufacturer


class Product(CreatedUpdatedMixin, Base):
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

    manufacturer: Mapped["Manufacturer"] = relationship(
        back_populates="products",
    )
