# from tests.conftest import client, setup_and_teardown  # type: ignore
from typing import Any

from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def data() -> dict[str, Any]:
    data_dict = {
        "name": "Alexander",
        "username": "alexander",
        "email": "user@example.com",
        "age": 30,
        "password": "secure_test_password",
    }
    return data_dict


def test_create_user(client: TestClient, data) -> None:
    response = client.post(
        url="/api/v1/users/create-user/",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert "username" in content
    assert content["username"] == data["username"]
    assert "name" in content
    assert content["name"] == data["name"]
    assert "age" in content
    assert content["age"] == data["age"]
    assert "email" in content
    assert content["email"] == data["email"]


def test_auth_user_issue_jwt(client: TestClient, data) -> None:
    form_data = {
        "username": data["username"],
        "password": data["password"],
    }
    response = client.post(
        url="/api/jwt/login/",
        data=form_data,
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "Bearer"


def test_get_user(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/users/user/1",
    )
    assert response.status_code == 200
    content = response.json()
    assert "username" in content
    assert "name" in content
    assert "age" in content
    assert "email" in content
    assert "is_active_user" in content
    assert "is_superuser" in content


@pytest.mark.parametrize(
    "name",
    [
        "SuperVeryVeryLongName",
        "AAAAAAAAAAAAAAAAAAAAAAAA",
        "some@value",
        "name@?1",
    ],
)
def test_create_wrong_user_name(
    client: TestClient,
    name: str,
) -> None:
    data = {
        "name": name,
        "username": "alexander14",
        "age": 25,
    }
    response = client.post(
        url="/api/v1/users/create-user/",
        json=data,
    )
    assert response.status_code == 422


def get_non_existing_user(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/users/user/15000",
    )
    assert response.status_code == 404


def test_update_unauth_user(client: TestClient) -> None:
    data = {
        "name": "Alex",
        "username": "alexander14",
        "age": 25,
    }
    response = client.patch(
        url="/api/v1/users/user/1",
        json=data,
    )
    assert response.status_code == 401


def test_delete_unauth_user(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/users/user/1",
    )
    assert response.status_code == 401


def test_getme_unauth_user(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/users/me/",
    )
    assert response.status_code == 405
