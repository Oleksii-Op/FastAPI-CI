from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class CreatedUpdatedMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
    )
