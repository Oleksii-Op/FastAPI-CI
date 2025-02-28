from sqlalchemy.exc import IntegrityError
import logging
from core.models import User
from core.config import settings
from auth.jwt_helper import hash_password
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


def create_first_superuser(session_factory: sessionmaker) -> None:
    with session_factory() as session:
        superuser = User(
            name=settings.superuser.name,
            email=settings.superuser.email,
            password=hash_password(settings.superuser.password),
            username=settings.superuser.username,
            is_superuser=True,
            is_active_user=True,
        )
        session.add(superuser)
        try:
            session.commit()
            logger.info("Created superuser")
        except IntegrityError:
            logger.error("Superuser already exists")
            session.rollback()


# if __name__ == "__main__":
#     create_first_superuser()
