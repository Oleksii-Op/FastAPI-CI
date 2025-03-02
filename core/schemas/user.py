import re
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, AfterValidator, Field, ConfigDict, EmailStr


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
    email: EmailStr
    age: int | None = Field(
        default=None,
        gt=0,
    )
    is_active_user: bool = True
    is_superuser: bool = False
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=12,
        max_length=128,
    )

# DO NOT USE THIS SCHEMA IN ROUTES
class FullUser(UserCreate):
    id: int


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserPatch(BaseModel):
    name: ValidString | None = Field(  # type: ignore
        default=None,
        min_length=1,
        max_length=20,
    )
    password: str | None = Field(  # type: ignore
        default=None,
        min_length=12,
        max_length=128,
    )
    username: ValidString | None = Field(  # type: ignore
        default=None,
        min_length=8,
        max_length=20,
    )
    age: int | None = Field(
        default=None,
        gt=0,
    )
