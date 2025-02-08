from collections.abc import Generator
import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import StaticPool
from core.get_db import DatabaseHelper, get_db

# in memory sqlite3 database
db_testing = DatabaseHelper(
    url="sqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
    echo_pool=True,
    echo=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
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
