from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base
from sqlalchemy import String
from core.models.mixins import CreatedUpdatedMixin


class User(CreatedUpdatedMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(20))
    password: Mapped[str]
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int | None]
    is_active_user: Mapped[bool]
    is_superuser: Mapped[bool]
