from typing import Annotated

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.dependencies import get_current_active_auth_user
from core.get_db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from core.models import User
from core.schemas import UserPatch, UserBase, UserPublic, UserCreate


from auth.jwt_helper import hash_password

router = APIRouter(
    tags=["Users"],
)


@router.post(
    "/create-user/",
    response_model=UserBase,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> UserBase:
    user_dict = user.model_dump()
    user_dict["is_active_user"] = True
    user_dict["is_superuser"] = False
    password = user_dict.pop("password")
    user_in = User(
        **user_dict,
        password=hash_password(password),
    )
    session.add(user_in)
    try:
        session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    return user


@router.get(
    "/user/{user_id}",
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
    "/user/{user_id}",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: int,
    user_in: UserPatch,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    user_dep: UserPublic = Depends(get_current_active_auth_user),
) -> User | None:
    if not user_dep.is_superuser and user_dep.id != user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="You do not have sufficient privileges",
        )
    user: User | None = session.get(
        User,
        user_id,
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
        )
    for field, value in user_in.model_dump(
        exclude_unset=True, exclude=user_in.password
    ).items():
        setattr(user, field, value)
    setattr(user, "password", hash_password(user_in.password))
    session.commit()
    return user


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
    user_dep: UserPublic = Depends(get_current_active_auth_user),
) -> None:
    if not user_dep.is_superuser and user_dep.id != user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="You do not have sufficient privileges",
        )
    if user_dep.is_superuser:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Superusers cannot be deleted",
        )
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


@router.get(
    "/me/",
    response_model=UserPublic,
)
def auth_user_check_self_info(
    user: UserPublic = Depends(get_current_active_auth_user),
):
    return user
