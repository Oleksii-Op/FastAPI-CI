from typing import Annotated

from sqlmodel import Field, SQLModel
from pydantic import AfterValidator
import re


def validate_username_or_name(value: str) -> str:
    if not re.match(r"^[a-zA-Z0-9]+$", value):
        raise ValueError(
            "Can only contain letters and numbers",
        )
    return value


ValidString = Annotated[str, AfterValidator(validate_username_or_name)]


class User(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
    )
    name: ValidString = Field(
        min_length=0,
        max_length=20,
    )
    username: ValidString = Field(
        min_length=8,
        max_length=20,
    )
    age: int | None = Field(
        default=None,
        gt=0,
    )

    __table_args__ = {"extend_existing": True}
