from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(20))
    username: Mapped[str] = mapped_column(String(20))
    age: Mapped[int | None]
