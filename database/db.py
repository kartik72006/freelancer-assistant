from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///proposal_assistant.db"

# Engine manages connections to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Creates database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """
    Creates a database session.

    Will be used later with FastAPI dependency injection.

    Example:
        db = next(get_db())
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()