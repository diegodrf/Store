from sqlmodel import Session
from fastapi import Depends

from .repository.database import engine


async def get_session():
    """Create database sessions for dependency injection."""
    with Session(engine) as session:
        yield session

