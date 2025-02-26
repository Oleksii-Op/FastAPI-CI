from datetime import datetime, UTC

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base


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
