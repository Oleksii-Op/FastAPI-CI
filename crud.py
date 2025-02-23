from sqlalchemy.orm import Session
from sqlalchemy import select
from core.models import User


def get_user_by_email(
    session: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.scalar(statement)
    return session_user


def get_user_by_username(
    session: Session,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.scalar(statement)
    return session_user
