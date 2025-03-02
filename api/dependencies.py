from typing import Annotated

from fastapi import Depends, Form, HTTPException
from starlette import status
from jwt.exceptions import InvalidTokenError
from core.models import User, Manufacturer, Product
from crud import get_user_by_username
from fastapi.security import OAuth2PasswordBearer
from core.schemas import UserBase
from auth import jwt_helper
from core.get_db import get_db
from sqlalchemy.orm import Session


SessionGetter = Annotated[Session, Depends(get_db.session_getter)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/jwt/login/")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt_helper.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return payload


def get_current_auth_user(
    session: SessionGetter,
    payload: dict = Depends(get_current_token_payload),
) -> User:
    username: str | None = payload.get("sub")
    user: User | None = get_user_by_username(
        session=session,
        username=username,  # type: ignore
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )
    return user


def get_current_superuser(
    user: UserBase = Depends(get_current_auth_user),
):
    if user.is_superuser:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have sufficient privileges",
    )


def get_current_active_auth_user(
    user: UserBase = Depends(get_current_auth_user),
):
    if user.is_active_user:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not active user",
    )


def validate_auth_user(
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    username: str = Form(),
    password: str = Form(),
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user = get_user_by_username(
        session=session,
        username=username,
    )
    if not user:
        raise unauth_exc

    if not jwt_helper.validate_password(
        password=password,
        hashed_password=str(user.password),
    ):
        raise unauth_exc
    if not user.is_active_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be active before you can use this method",
        )
    return user


def get_manufacturer_by_id_dep(
    session: SessionGetter,
    manufacturer_id: int,
) -> Manufacturer:
    manufacturer: Manufacturer | None = session.get(
        Manufacturer,
        manufacturer_id,
    )
    if not manufacturer:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )
    return manufacturer


def get_product_by_id_dep(
    session: SessionGetter,
    product_id: int,
) -> Product:
    product: Product | None = session.get(
        Product,
        product_id,
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


def get_user_by_id_dep(
    session: SessionGetter,
    user_id: int,
) -> User:
    user: User | None = session.get(
        User,
        user_id,
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
        )
    return user
