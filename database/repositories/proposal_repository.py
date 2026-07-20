"""
Proposal Repository

Handles proposal-specific database operations.
"""

from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session,joinedload

from database.models import Proposal
from database.repositories.base_repository import BaseRepository


class ProposalRepository(BaseRepository[Proposal]):

    def __init__(self):
        super().__init__(Proposal)

    # ---------------------------------------------------------
    # PROPOSAL SPECIFIC METHODS
    # ---------------------------------------------------------

    def get_proposals_by_user(
        self,
        db: Session,
        user_id: int
    ) -> List[Proposal]:

        return self.filter(
            db,
            user_id=user_id
        )

    def get_proposals_by_job(
        self,
        db: Session,
        job_id: int
    ) -> List[Proposal]:

        return self.filter(
            db,
            job_id=job_id
        )

    def get_latest_proposals(
        self,
        db: Session,
        limit: int = 10
    ) -> List[Proposal]:

        return (
            db.query(Proposal)
            .order_by(Proposal.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_model(
        self,
        db: Session,
        model: str
    ) -> List[Proposal]:

        return self.filter(
            db,
            model=model
        )
    
    def get_history(
        self,
        db,
        user_id: int
    ):
        """
        Returns all proposals of a user ordered by newest first.
        """

        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .all()
        )
    
    def update_status(
    self,
    db,
    proposal_id: int,
    new_status: str
):
        proposal = self.get_by_id(db, proposal_id)

        if proposal is None:
            return None

        proposal.status = new_status

        db.commit()
        db.refresh(proposal)

        return proposal
    
    def update_final_proposal(
        self,
        db,
        proposal_id: int,
        final_proposal: str
    ):
        proposal = self.get_by_id(db, proposal_id)

        if proposal is None:
            return None

        proposal.final_proposal = final_proposal

        db.commit()
        db.refresh(proposal)

        return proposal
    
    def duplicate(
        self,
        db,
        proposal,
        job_id:int,
    ):
        duplicate = Proposal(
            job_id=job_id,
            user_id=proposal.user_id,

            analysis=proposal.analysis,
            proposal=proposal.proposal,
            pricing=proposal.pricing,
            timeline=proposal.timeline,
            review=proposal.review,

            final_proposal=proposal.final_proposal,

            model=proposal.model,
            prompt_version=proposal.prompt_version,

            status="Draft",

            category=proposal.category,
        )

        db.add(duplicate)
        db.commit()
        db.refresh(duplicate)

        return duplicate
    
    def get_status_distribution(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns the number of proposals in each status.
        """

        return (
            db.query(
                Proposal.status,
                func.count(Proposal.id)
            )
            .filter(
                Proposal.user_id == user_id
            )
            .group_by(
                Proposal.status
            )
            .all()
        )
    
    def get_proposal_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposal counts grouped by month.
        """

        return (
            db.query(
                func.strftime("%Y-%m", Proposal.created_at).label("period"),
                func.count(Proposal.id).label("generated"),
                func.sum(
                    Proposal.status == "Accepted"
                ).label("accepted")
            )
            .filter(
                Proposal.user_id == user_id
            )
            .group_by("period")
            .order_by("period")
            .all()
        )
    
    def get_proposals_for_ai_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposals ordered by creation date for AI score trend.
        """

        return (
            db.query(Proposal)
            .filter(
                Proposal.user_id == user_id
            )
            .order_by(
                Proposal.created_at
            )
            .all()
        )
    
    def get_proposals_for_acceptance_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposals ordered by date for acceptance trend.
        """

        return (
            db.query(Proposal)
            .filter(
                Proposal.user_id == user_id
            )
            .order_by(
                Proposal.created_at
            )
            .all()
        )
    
    def get_proposals_with_jobs(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposals with their related jobs.
        """

        return (
            db.query(Proposal)
            .options(
                joinedload(Proposal.job)
            )
            .filter(
                Proposal.user_id == user_id
            )
            .all()
        )