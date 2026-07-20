from database.db import Base, engine

# Import models so SQLAlchemy knows about them
from database import models


def initialize_database():

    Base.metadata.create_all(bind=engine)

    print("=" * 50)
    print("Database created successfully.")
    print("=" * 50)


if __name__ == "__main__":
    initialize_database()