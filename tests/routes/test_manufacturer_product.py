from starlette.testclient import TestClient
from tests.conftest import client
from tests.utils import superuser_token, encode_jwt

fake_company = {
    "name": "Test Company",
    "updated_name": "Test Company Updated",
}

fake_product = {
    "name": "Test Product",
    "year": 2020,
    "cpu": "FakeCore i7",
}
updated_fake_product = {
    "name": "Test Product Updated",
    "year": 2021,
    "cpu": "FakeCore i9",
}


def test_create_manufacturer(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/manufacturers/create",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "name": fake_company["name"],
        },
    )
    assert response.status_code == 201


def test_get_manufacturer(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/1",
    )
    assert response.status_code == 200
    assert response.json()["name"] == fake_company["name"]


def test_get_all_manufacturers(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/all",
    )
    assert response.status_code == 200
    assert response.json() != []


def test_update_manufacturer(client: TestClient) -> None:
    response = client.patch(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "name": fake_company["updated_name"],
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] != fake_company["name"]
    assert response.json()["name"] == fake_company["updated_name"]


def test_create_product(client: TestClient) -> None:
    manufacturer_id = 1
    response = client.post(
        url=f"/api/v1/products/create?manufacturer_id={manufacturer_id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=fake_product,
    )
    assert response.status_code == 201
    assert response.json()["name"] == fake_product["name"]
    assert response.json()["year"] == fake_product["year"]
    assert response.json()["cpu"] == fake_product["cpu"]
    assert response.json()["manufacturer_id"] == manufacturer_id


def test_get_product(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/products/1",
    )
    assert response.status_code == 200
    assert response.json()["name"] == fake_product["name"]
    assert response.json()["year"] == fake_product["year"]
    assert response.json()["cpu"] == fake_product["cpu"]


def test_get_all_products(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/products/all",
    )
    assert response.status_code == 200
    assert response.json() != []


def test_update_product_unauthorized(client: TestClient) -> None:
    response = client.patch(
        url=f"/api/v1/products/1",
    )
    assert response.status_code == 401


def test_update_product(client: TestClient) -> None:
    response = client.patch(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=updated_fake_product,
    )
    assert response.status_code == 200
    assert response.json()["name"] == updated_fake_product["name"]
    assert response.json()["year"] == updated_fake_product["year"]
    assert response.json()["cpu"] == updated_fake_product["cpu"]


def test_delete_product_unauthorized(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/products/1",
    )
    assert response.status_code == 401


def test_delete_product(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 204


def test_delete_manufacturer(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 204


def test_get_non_existent_manufacturer(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/1",
    )
    assert response.status_code == 404


def test_get_non_existent_product(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/products/1",
    )
    assert response.status_code == 404


def test_update_non_existent_product(client: TestClient) -> None:
    response = client.patch(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=updated_fake_product,
    )
    assert response.status_code == 404


def test_update_non_existent_manufacturer(client: TestClient) -> None:
    response = client.patch(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "name": fake_company["name"],
        },
    )
    assert response.status_code == 404


def test_delete_non_existent_product(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 404


def test_delete_non_existent_manufacturer(client: TestClient) -> None:
    response = client.delete(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )
    assert response.status_code == 404


def test_empty_get_all_manufacturers(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/manufacturers/all",
    )
    assert response.status_code == 404


def test_empty_get_all_products(client: TestClient) -> None:
    response = client.get(
        url="/api/v1/products/all",
    )
    assert response.status_code == 404


### AUTH USER
def test_create_manufacturer_forbidden(
    client: TestClient, create_test_user_token
) -> None:
    user_token = create_test_user_token
    response = client.post(
        url="/api/v1/manufacturers/create",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "name": fake_product["name"],
        },
    )
    assert response.status_code == 403


def test_update_manufacturer_forbidden(
    client: TestClient, create_test_user_token
) -> None:
    user_token = create_test_user_token
    response = client.patch(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "name": fake_company["updated_name"],
        },
    )
    assert response.status_code == 403


def test_delete_manufacturer_forbidden(
    client: TestClient, create_test_user_token
) -> None:
    user_token = create_test_user_token
    response = client.delete(
        url="/api/v1/manufacturers/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403


def test_create_product_forbidden(client: TestClient, create_test_user_token) -> None:
    user_token = create_test_user_token
    response = client.post(
        url="/api/v1/products/create?manufacturer_id=1",
        headers={"Authorization": f"Bearer {user_token}"},
        json=fake_product,
    )
    assert response.status_code == 403


def test_update_product_forbidden(client: TestClient, create_test_user_token) -> None:
    user_token = create_test_user_token
    response = client.patch(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {user_token}"},
        json=updated_fake_product,
    )
    assert response.status_code == 403


def test_delete_product_forbidden(client: TestClient, create_test_user_token) -> None:
    user_token = create_test_user_token
    response = client.delete(
        url="/api/v1/products/1",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403
