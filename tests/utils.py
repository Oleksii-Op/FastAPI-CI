from typing import Any
from auth.jwt_helper import encode_jwt
from core.config import settings

data_dict = {
    "name": "Alexander",
    "username": "alexander",
    "email": "user@example.com",
    "age": 30,
    "password": "secure_test_password",
}

superuser_dict = {
    "name": settings.superuser.name,
    "username": settings.superuser.username,
    "email": settings.superuser.email,
    "password": settings.superuser.password,
}


def issue_access_token(data: dict[str, Any]) -> str:
    jwt_payload = {
        "sub": data["username"],
        "username": data["username"],
        "email": data["email"],
    }
    return encode_jwt(jwt_payload)


def issue_superuser_access_token(data: dict[str, Any]) -> str:
    jwt_payload = {
        "sub": data["username"],
        "username": data["username"],
        "email": data["email"],
    }
    return encode_jwt(jwt_payload)


token = issue_access_token(data_dict)
superuser_token = issue_superuser_access_token(superuser_dict)
