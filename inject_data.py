from random import randint

from faker import Faker
from core import get_db
from core.models import User
from sqlalchemy.orm import Session
from time import time


def inject_data(multiple_of: int):
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
                    user_in = User(
                        name=fake.name(),
                        username=fake.user_name(),
                        age=randint(16, 80),
                    )
                    users.append(user_in)

                session.add_all(users)
                counter += 10
                session.commit()

        except Exception as e:
            counter -= 10
            print(f"Failed to inject data: {e}")

    print(f"Added {counter} users.")
    print("Done")


if __name__ == "__main__":
    start = time()
    inject_data(1000)
    end = time()
    print(f"Injected in {end - start} seconds.")
