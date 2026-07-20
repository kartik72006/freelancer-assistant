"""
Base Repository

Provides generic CRUD operations for all SQLAlchemy models.

Every repository in the project should inherit from this class.

Example:
    class UserRepository(BaseRepository[User]):
        def __init__(self):
            super().__init__(User)

Author: Kartik Bansal
Project: AI Freelancer Proposal Assistant
"""

from typing import (
    Generic,
    TypeVar,
    Type,
    Optional,
    List,
    Any
)

from sqlalchemy.orm import Session

from database.db import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository implementing reusable database operations.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        db: Session,
        **kwargs
    ) -> ModelType:
        """
        Create a new record.
        """

        obj = self.model(**kwargs)

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        db: Session,
        object_id: int
    ) -> Optional[ModelType]:
        """
        Retrieve an object by primary key.
        """

        return (
            db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
        )
    
    def get_all(
        self,
        db: Session
    ) -> List[ModelType]:
        """
        Retrieve all records.
        """

        return db.query(self.model).all()

    def get_first(
        self,
        db: Session,
        **filters
    ) -> Optional[ModelType]:
        """
        Return the first record matching the filters.

        Example:
            get_first(db, email="abc@gmail.com")
        """

        query = db.query(self.model)

        for field, value in filters.items():
            query = query.filter(
                getattr(self.model, field) == value
            )

        return query.first()

    def filter(
        self,
        db: Session,
        **filters
    ) -> List[ModelType]:
        """
        Return all records matching the filters.

        Example:
            filter(db, user_id=1)

            filter(db, source="Upwork")
        """

        query = db.query(self.model)

        for field, value in filters.items():
            query = query.filter(
                getattr(self.model, field) == value
            )

        return query.all()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        db: Session,
        db_object: ModelType,
        **kwargs
    ) -> ModelType:
        """
        Update an existing record.
        """

        for key, value in kwargs.items():

            if hasattr(db_object, key):

                setattr(db_object, key, value)

        db.commit()

        db.refresh(db_object)

        return db_object

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        db: Session,
        db_object: ModelType
    ) -> None:
        """
        Delete an object.
        """

        db.delete(db_object)

        db.commit()

    def delete_by_id(
        self,
        db: Session,
        object_id: int
    ) -> bool:
        """
        Delete an object by ID.

        Returns True if deleted successfully.
        """

        obj = self.get_by_id(db, object_id)

        if obj is None:
            return False

        db.delete(obj)

        db.commit()

        return True

    # ==========================================================
    # UTILITIES
    # ==========================================================

    def exists(
        self,
        db: Session,
        object_id: int
    ) -> bool:
        """
        Check whether a record exists.
        """

        return self.get_by_id(db, object_id) is not None

    def count(
        self,
        db: Session
    ) -> int:
        """
        Return total number of records.
        """

        return db.query(self.model).count()

    def paginate(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10
    ) -> List[ModelType]:
        """
        Return paginated results.
        """

        offset = (page - 1) * page_size

        return (
            db.query(self.model)
            .offset(offset)
            .limit(page_size)
            .all()
        )

    def order_by(
        self,
        db: Session,
        field: str,
        descending: bool = False
    ) -> List[ModelType]:
        """
        Return ordered records.

        Example:
            order_by(db, "created_at")

            order_by(db, "created_at", descending=True)
        """

        column = getattr(self.model, field)

        if descending:
            column = column.desc()

        return (
            db.query(self.model)
            .order_by(column)
            .all()
        )