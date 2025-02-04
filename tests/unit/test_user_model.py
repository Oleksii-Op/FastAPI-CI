import uuid

import pytest
from core.models.user import User

valid_user_data = {
    "id": 1,
    "name": "TestUser",
    "username": "testuser",
    "age": 40,
}


def test_valid_user_data() -> None:
    user = User(**valid_user_data)
    assert user.id == valid_user_data["id"]
    assert user.name == valid_user_data["name"]
    assert user.username == valid_user_data["username"]
    assert user.age == valid_user_data["age"]


@pytest.mark.parametrize(
    "invalid_id",
    [
        "-invalid@e?4",
        "somevalue",
        uuid.uuid4(),
    ],
)
def test_wrong_user_id(
    invalid_id: int | str,
) -> None:
    data = valid_user_data.copy()
    data["id"] = invalid_id

    with pytest.raises(
        ValueError,
    ):
        user = User(**data)
        User.model_validate(user.model_dump())


@pytest.mark.parametrize(
    "invalid_age",
    [
        -40,
        "-10",
        "somevalue",
    ],
)
def test_wrong_user_age(
    invalid_age: int | str,
) -> None:
    data = valid_user_data.copy()
    data["age"] = invalid_age

    with pytest.raises(
        ValueError,
    ):
        user = User(**data)
        User.model_validate(user.model_dump())


@pytest.mark.parametrize(
    "invalid_name",
    [
        "SuperVeryVeryLongName",
        1050,
        "some@value",
        "name@?1",
    ],
)
def test_wrong_name(
    invalid_name: int | str,
) -> None:
    data = valid_user_data.copy()
    data["name"] = invalid_name

    with pytest.raises(ValueError):
        user = User(**data)
        User.model_validate(user.model_dump())


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
def test_wrong_username(
    invalid_username: int | str,
) -> None:
    data = valid_user_data.copy()
    data["username"] = invalid_username

    with pytest.raises(
        ValueError,
    ):
        user = User(**data)
        User.model_validate(user.model_dump())
