"""
Job Repository

Handles job-specific database operations.
"""

from typing import List

from sqlalchemy.orm import Session

from database.models import Job
from database.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):

    def __init__(self):
        super().__init__(Job)

    # ---------------------------------------------------------
    # JOB SPECIFIC METHODS
    # ---------------------------------------------------------

    def get_jobs_by_user(
        self,
        db: Session,
        user_id: int
    ) -> List[Job]:

        return self.filter(
            db,
            user_id=user_id
        )

    def get_jobs_by_source(
        self,
        db: Session,
        source: str
    ) -> List[Job]:

        return self.filter(
            db,
            source=source
        )

    def get_latest_jobs(
        self,
        db: Session,
        limit: int = 10
    ) -> List[Job]:

        return (
            db.query(Job)
            .order_by(Job.created_at.desc())
            .limit(limit)
            .all()
        )