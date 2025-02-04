from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from core.get_db import get_db
from core.config import settings
import logging
from core.models.user import User
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
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


app = FastAPI(lifespan=lifespan)


@app.get("/user/{id}")
def create_user(
    user_id: int,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> User | None:
    user = session.get(User, user_id)
    return user


@app.post(
    "/create-user/",
    response_model=User,
)
def create_user(
    user: User,
    session: Annotated[
        Session,
        Depends(get_db.session_getter),
    ],
) -> User:
    user_in = user
    session.add(user_in)
    session.commit()
    return user_in


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
    )
