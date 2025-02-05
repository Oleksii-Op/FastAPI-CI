from typing import Annotated
from sqlalchemy.orm import Session
from core.get_db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from core.models import User
from core.schemas import UserPatch, UserBase
from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)


@router.post(
    "/create-user/",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserBase,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> UserBase:
    user_in = User(**user.model_dump())
    session.add(user_in)
    session.commit()
    return user


@router.get(
    "/user/{id}",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: int,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> User | None:
    user: User | None = session.get(
        User,
        user_id,
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
        )
    return user


@router.patch(
    "/user/{id}",
    response_model=UserBase,
)
def update_user(
    user_id: int,
    user_in: UserPatch,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> User | None:
    user: User | None = session.get(
        User,
        user_id,
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
        )
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    return user


@router.delete("/user/{id}")
def delete_user(
    user_id: int,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> None:
    user: User | None = session.get(
        User,
        user_id,
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
        )
    session.delete(user)
    session.commit()
