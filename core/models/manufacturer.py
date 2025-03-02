from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base
from core.models.mixins import CreatedUpdatedMixin

if TYPE_CHECKING:
    from core.models.product import Product


class Manufacturer(CreatedUpdatedMixin, Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)

    products: Mapped[list["Product"]] = relationship(
        back_populates="manufacturer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Manufacturer {self.id}>"
