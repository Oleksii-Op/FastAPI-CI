from datetime import timedelta, datetime, UTC

import jwt
from core.config import settings
import bcrypt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


password_hash = PasswordHash(
    (Argon2Hasher(),),
)


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expires_in: int = settings.auth.access_token_expires_in_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expires_in)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth.public_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=algorithm,
    )
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return password_hash.hash(
        password=pwd_bytes,
        salt=salt,
    )


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        password=password,
        hash=hashed_password,
    )
