from fastapi import APIRouter

from core.config import settings
from api.v1 import router as router_api_v1

from .v1.auth_jwt import router as jwt_router

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_api_v1)

router.include_router(jwt_router)
