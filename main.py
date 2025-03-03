import uvicorn
from fastapi import FastAPI
from core.get_db import get_db
from contextlib import asynccontextmanager
from api import router as api_router
from core.config import settings, Environment
import logging
from logger_config import configure_logger
from actions.create_first_superuser import create_first_superuser


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):  # type: ignore
    logger.info("Starting app")
    logger.info("Creating database")
    if settings.environment != Environment.TESTING:
        get_db.create_database()
        create_first_superuser(session_factory=get_db.session_factory)
    yield
    logger.info("Stopping app")
    logger.info("Deleting database")
    get_db.dispose_database()


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
)
app.include_router(api_router)


if __name__ == "__main__":
    configure_logger()
    uvicorn.run(
        "main:app",
        host=settings.runtime.host,
        port=settings.runtime.port,
        reload=True if settings.environment == Environment.DEVELOPMENT else False,
        workers=settings.runtime.workers,
    )
