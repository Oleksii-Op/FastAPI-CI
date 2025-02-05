from typing import TypedDict
import uuid
import pytest
from core.schemas import FullUser


class UserData(TypedDict):
    id: int
    name: str
    username: str
    age: int


valid_user_data: UserData = {
    "id": 1,
    "name": "TestUser",
    "username": "testuser",
    "age": 40,
}


def test_valid_user_data() -> None:
    user = FullUser(**valid_user_data)
    for key, value in valid_user_data.items():
        assert getattr(user, key) == value


@pytest.mark.parametrize(
    "invalid_id",
    [
        "-invalid@e?4",
        "somevalue",
        uuid.uuid4(),
    ],
)
def test_wrong_user_id(invalid_id: int | str) -> None:
    data: UserData = valid_user_data.copy()
    data["id"] = invalid_id  # type: ignore

    with pytest.raises(ValueError):
        FullUser(**data)


@pytest.mark.parametrize(
    "invalid_age",
    [
        -40,
        "-10",
        "somevalue",
    ],
)
def test_wrong_user_age(invalid_age: int | str) -> None:
    data: UserData = valid_user_data.copy()
    data["age"] = invalid_age  # type: ignore

    with pytest.raises(ValueError):
        FullUser(**data)


@pytest.mark.parametrize(
    "invalid_name",
    [
        "SuperVeryVeryLongName",
        1050,
        "some@value",
        "name@?1",
    ],
)
def test_wrong_name(invalid_name: int | str) -> None:
    data: UserData = valid_user_data.copy()
    data["name"] = invalid_name  # type: ignore

    with pytest.raises(ValueError):
        FullUser(**data)


@pytest.mark.parametrize(
    "invalid_username",
    [
        "SuperVeryVeryLongName",
        "Short",
        1050,
        "some@value",
        "name@?1",
    ],
)
def test_wrong_username(invalid_username: int | str) -> None:
    data: UserData = valid_user_data.copy()
    data["username"] = invalid_username  # type: ignore

    with pytest.raises(ValueError):
        FullUser(**data)
