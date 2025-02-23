from fastapi import APIRouter, Depends
from core.schemas import UserPublic
from auth import jwt_helper

from core.schemas.token import Token
from api.dependencies import (
    validate_auth_user,
)

router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)


@router.post(
    "/login/",
    response_model=Token,
)
def auth_user_issue_jwt(
    user: UserPublic = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = jwt_helper.encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )
