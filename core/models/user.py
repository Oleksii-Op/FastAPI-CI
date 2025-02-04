from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        index=True,
    )
    name: str
    username: str
    age: int | None = None

    __table_args__ = {"extend_existing": True}
