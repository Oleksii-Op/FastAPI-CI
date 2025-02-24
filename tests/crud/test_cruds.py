from sqlalchemy.orm import Session
from core.models import User
from crud import get_user_by_username, get_user_by_email
import pytest


@pytest.fixture(scope="module")
def create_objects_for_crud(get_session) -> User:
    user = User(
        name="TestUser",
        username="TestUser",
        email="user@example.com",
        password="hashedpassword",
        is_active_user=True,
        is_superuser=False,
    )
    get_session.add(user)
    get_session.flush()  # do not commit to avoid conflict with test_users.py
    return user


def test_get_user_by_username(
    create_objects_for_crud: User,
    get_session: Session,
) -> None:
    user = get_user_by_username(
        session=get_session,
        username=create_objects_for_crud.name,
    )
    assert user is not None
    assert isinstance(user, User)
    assert user.username == create_objects_for_crud.username
    assert user.email == create_objects_for_crud.email
    assert user.name == create_objects_for_crud.name


def test_get_nonexist_user_by_username(
    create_objects_for_crud: User,
    get_session: Session,
) -> None:
    user = get_user_by_username(
        session=get_session,
        username="NonexistentUser",
    )
    assert user is None


def test_get_user_by_email(
    create_objects_for_crud: User,
    get_session: Session,
) -> None:
    user = get_user_by_email(
        session=get_session,
        email=create_objects_for_crud.email,
    )
    assert user is not None
    assert isinstance(user, User)
    assert user.username == create_objects_for_crud.username
    assert user.email == create_objects_for_crud.email
    assert user.name == create_objects_for_crud.name


def test_get_nonexist_user_by_email(
    create_objects_for_crud: User,
    get_session: Session,
) -> None:
    user = get_user_by_email(
        session=get_session,
        email="NonexistentUser@example.com",
    )
    assert user is None
