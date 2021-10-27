from sqlmodel import SQLModel
from .repository.database import engine


def create_tables_if_not_exists() -> None:
    SQLModel.metadata.create_all(engine)
