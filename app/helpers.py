from sqlmodel import SQLModel
from .repository.database import engine
from .repository.models import model


def create_tables_if_not_exists() -> None:
    SQLModel.metadata.create_all(engine)
