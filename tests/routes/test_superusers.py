from fastapi.testclient import TestClient
from core.config import settings
from tests.utils import superuser_token


def test_first_superuser(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/users/user/1",
    )
    assert response.status_code == 200
    assert response.json()["is_superuser"] is True
    assert response.json()["name"] == settings.superuser.name
    assert response.json()["username"] == settings.superuser.name
    assert response.json()["email"] == settings.superuser.email


def test_getme_auth_superuser(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/users/me",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 200
    assert response.json()["is_superuser"] is True
    assert response.json()["name"] == settings.superuser.name
    assert response.json()["username"] == settings.superuser.name
    assert response.json()["email"] == settings.superuser.email


def test_update_superuser(client: TestClient) -> None:
    response = client.patch(
        url="/api/v1/users/user/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "username": "UpdatedAdmin",
            "name": "UpdatedAdmin",
            "password": "TestSuperuserPassword",
        },
    )
    assert response.status_code == 200
    assert response.json()["is_superuser"] is True
    assert response.json()["name"] != settings.superuser.name
    assert response.json()["username"] != settings.superuser.username


def test_delete_superuser(client: TestClient) -> None:
    form_data = {
        "username": "UpdatedAdmin",
        "password": "TestSuperuserPassword",
    }
    response_token = client.post(
        url="/api/jwt/login/",
        data=form_data,
    )
    response = client.delete(
        url="/api/v1/users/user/1",
        headers={"Authorization": f"Bearer {response_token.json()['access_token']}"},
    )
    assert response_token.status_code == 200
    assert response_token.json()["access_token"] is not None
    assert response_token.json()["token_type"] == "Bearer"

    assert response.status_code == 400
