import pytest
from auth.jwt_helper import (
    hash_password,
    validate_password,
    encode_jwt,
    decode_jwt,
)
from faker import Faker
from tests.conftest import users_for_jwt
from jwt.exceptions import InvalidSignatureError

faker = Faker()


@pytest.mark.parametrize(
    "password",
    [faker.password() for _ in range(10)],
)
def test_hash_password(password):
    hashed_password = hash_password(password)
    assert hashed_password is not None
    assert validate_password(
        password=password,
        hashed_password=hashed_password,
    )


@pytest.mark.parametrize(
    "password",
    [faker.password() for _ in range(10)],
)
def test_false_hash_password(password):
    hashed_password = hash_password(password)
    assert hashed_password is not None
    assert not validate_password(
        password=password + "injected_false_values",
        hashed_password=hashed_password,
    )


@pytest.mark.parametrize(
    "index",
    list(range(10)),
)
def test_encode_decode_jwt(users_for_jwt, index):
    user = users_for_jwt[index]
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    # Encoding
    encoded_jwt = encode_jwt(payload=jwt_payload)
    assert encoded_jwt is not None
    assert isinstance(encoded_jwt, str)

    # Decoding
    decoded_payload = decode_jwt(token=encoded_jwt)
    assert decoded_payload is not None
    assert isinstance(decoded_payload, dict)

    # Integrity check
    assert decoded_payload["sub"] == user.username
    assert decoded_payload["username"] == user.username
    assert decoded_payload["email"] == user.email


@pytest.mark.xfail(raises=InvalidSignatureError)
def test_encode_decode_jwt_fail(users_for_jwt):
    user = users_for_jwt[0]
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    # Encoding
    encoded_jwt = encode_jwt(payload=jwt_payload)
    modified_token = encoded_jwt + "injected_false_values"
    with pytest.raises(InvalidSignatureError):
        decode_jwt(token=modified_token)
