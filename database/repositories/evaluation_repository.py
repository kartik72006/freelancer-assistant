"""
Evaluation Repository

Handles evaluation-specific database operations.
"""

from typing import Optional, List

from sqlalchemy.orm import Session

from database.models import Evaluation
from database.repositories.base_repository import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):

    def __init__(self):
        super().__init__(Evaluation)

    # ---------------------------------------------------------
    # EVALUATION SPECIFIC METHODS
    # ---------------------------------------------------------

    def get_by_proposal(
        self,
        db: Session,
        proposal_id: int
    ) -> Optional[Evaluation]:

        return self.get_first(
            db,
            proposal_id=proposal_id
        )

    def get_best_evaluations(
        self,
        db: Session,
        limit: int = 10
    ) -> List[Evaluation]:

        return (
            db.query(Evaluation)
            .order_by(Evaluation.overall_score.desc())
            .limit(limit)
            .all()
        )

    def get_low_score_evaluations(
        self,
        db: Session,
        threshold: float
    ) -> List[Evaluation]:

        return (
            db.query(Evaluation)
            .filter(Evaluation.overall_score < threshold)
            .all()
        )