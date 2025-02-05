from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from contextlib import asynccontextmanager

from core.get_db import get_db
from core.config import settings
import logging
from sqlalchemy.orm import Session
from logger_config import configure_logger

from core.schemas import UserBase
from core.models import User


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):  # type: ignore
    logger.info("Starting app")
    logger.info("Creating database")
    get_db.create_database()
    yield
    logger.info("Stopping app")
    logger.info("Deleting database")
    get_db.dispose_database()


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
)


@app.get(
    "/user/{id}",
    response_model=UserBase,
    status_code=status.HTTP_200_OK,
)
def get_user_by_id(
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


@app.post(
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


if __name__ == "__main__":
    configure_logger()
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
    )
