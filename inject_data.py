from random import randint

from faker import Faker

from auth.jwt_helper import hash_password
from core import get_db
from core.models import User
from core.schemas import UserCreate
from sqlalchemy.orm import Session
from time import time
import logging
from sqlite3 import OperationalError
from sys import exit

logger = logging.getLogger(__name__)


def inject_data(multiple_of: int) -> None:
    """
    Inserts fake user data into the database.

    :param multiple_of: The number of transaction batches to insert. Each batch contains 10 users.
    :return: None
    """
    fake = Faker()
    counter = 0  # Tracks the number of users successfully added

    for transaction in range(multiple_of):
        try:
            with Session(get_db.engine) as session:
                users = []
                for _ in range(10):
                    password = hash_password(fake.password())
                    try:
                        user_in = UserCreate(
                            name=fake.name().split(" ")[0],
                            username=fake.user_name(),
                            age=randint(16, 80),
                            password=password,
                            email=fake.email(),  # type: ignore
                            is_active_user=True,
                            is_superuser=False,
                        )
                    except Exception:
                        logger.warning("Could not validate user, skipping...")
                        continue
                    user = User(**user_in.model_dump())
                    users.append(user)

                session.add_all(users)
                counter += 10
                session.commit()
        except OperationalError:
            logger.exception(
                "Failed to inject fake user data, no connection",
            )
            exit(1)
        except Exception as e:
            counter -= 10
            logger.error(
                "Failed to inject data %r:",
                e,
            )

    logger.info(
        "Added %d users",
        counter,
    )
    logger.info("Finished injecting data")


if __name__ == "__main__":
    start = time()
    inject_data(1000)
    end = time()
    logger.info(
        "Injected data took %.2f seconds",
        end - start,
    )
