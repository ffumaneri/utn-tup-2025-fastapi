from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from functools import lru_cache

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:55433/UTN")

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session

@lru_cache()
def get_settings():
    """Get database settings"""
    return {
        "database_url": DATABASE_URL
    }
