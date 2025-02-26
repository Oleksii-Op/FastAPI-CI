from tests.conftest import client
from fastapi.testclient import TestClient


def test_non_exists_get_manufacturer(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/1",
    )
    assert response.status_code == 404


def test_create_manufacturer(client: TestClient) -> None:
    response = client.post(
        "/api/v1/manufacturers/create",
        json={
            "name": "IBM",
        },
    )
    assert response.status_code == 201


def test_get_manufacturer(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/1",
    )
    assert response.status_code == 200
    assert response.json()["name"] == "IBM"
