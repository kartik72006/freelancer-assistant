"""
User Repository

Handles user-specific database operations.
"""

from typing import Optional

from sqlalchemy.orm import Session

from database.models import User
from database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self):
        super().__init__(User)

    # ---------------------------------------------------------
    # USER SPECIFIC METHODS
    # ---------------------------------------------------------

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> Optional[User]:

        return self.get_first(
            db,
            email=email
        )

    def get_by_name(
        self,
        db: Session,
        name: str
    ) -> Optional[User]:

        return self.get_first(
            db,
            name=name
        )

    def exists_by_email(
        self,
        db: Session,
        email: str
    ) -> bool:

        return self.get_by_email(db, email) is not None