from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine, create_engine
from core.models import Base
from typing import Generator
from core.config import settings
from core.models.user import User  # type: ignore
import logging

logger = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: Engine = create_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def dispose(self) -> None:
        self.engine.dispose()

    def create_database(self) -> None:
        Base.metadata.create_all(self.engine)
        logger.warning(
            "Database creation has finished",
        )

    def dispose_database(self) -> None:
        Base.metadata.drop_all(self.engine)
        logger.warning(
            "Database deletion has been successful",
        )

    def session_getter(self) -> Generator[Session, None, None]:
        with self.session_factory() as session:
            logger.info("Yielding session")
            yield session


get_db = DatabaseHelper(
    settings.db.url,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo_pool=settings.db.echo_pool,
)
