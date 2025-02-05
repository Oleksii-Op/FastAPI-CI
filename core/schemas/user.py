import re
from typing import Annotated

from pydantic import BaseModel, AfterValidator, Field


def validate_username_or_name(value: str) -> str:
    if not re.match(r"^[a-zA-Z0-9]+$", value):
        raise ValueError(
            "Can only contain letters and numbers",
        )
    return value


ValidString = Annotated[str, AfterValidator(validate_username_or_name)]


class UserBase(BaseModel):
    name: ValidString = Field(
        min_length=1,
        max_length=20,
    )
    username: ValidString = Field(
        min_length=8,
        max_length=20,
    )
    age: int | None

    class Config:
        from_attributes = True


class FullUser(UserBase):
    id: int
