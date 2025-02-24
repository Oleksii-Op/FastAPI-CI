from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.models import User
from main import app
from sqlalchemy import StaticPool
from core.get_db import DatabaseHelper, get_db
from core.schemas.user import UserCreate
from faker import Faker

# in memory sqlite3 database
db_testing = DatabaseHelper(
    url="sqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
    echo_pool=True,
    echo=True,
)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown() -> Generator[None, None, None]:
    """Fixture to create and drop tables for each test"""
    db_testing.create_database()
    yield


app.dependency_overrides[get_db.session_getter] = db_testing.session_getter  # type: ignore


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture to yield a test client for each test
    :return: client: TestClient
    """
    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def get_session() -> Generator[Session, None, None]:
    with db_testing.session_factory() as session:
        yield session
        session.rollback()


def generate_10_users() -> list[UserCreate]:
    faker = Faker()
    users: list = []
    while len(users) < 10:
        try:
            user = UserCreate(
                name=faker.first_name(),
                username=faker.user_name(),
                password=faker.password(length=12) + "somepayload",
                email=faker.email(),  # type: ignore
                age=faker.random_int(min=1, max=100),
                is_active_user=True,
                is_superuser=False,
            )
            users.append(user)
        except Exception:
            continue
    return users


@pytest.fixture(scope="module")
def users_for_jwt() -> list[UserCreate]:
    return generate_10_users()
