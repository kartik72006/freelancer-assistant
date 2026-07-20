from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import AnalyticsEvent, Job, Proposal
from database.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository[AnalyticsEvent]):
    def __init__(self):
        super().__init__(AnalyticsEvent)

    # -------------------------
    # Create
    # -------------------------

    def create_event(
        self,
        db:Session,
        event_name: str,
        proposal_id: Optional[int] = None,
        user_id: Optional[int] = None,
        properties: Optional[dict] = None,
    ) -> AnalyticsEvent:
        """
        Create a new analytics event.
        """

        event = AnalyticsEvent(
            event_name=event_name,
            proposal_id=proposal_id,
            user_id=user_id,
            properties=properties or {},
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    # -------------------------
    # Read
    # -------------------------

    def get_event_by_id(self,db, event_id: int) -> Optional[AnalyticsEvent]:
        return (
            db.query(self.model)
            .filter(self.model.id == event_id)
            .first()
        )

    def get_events(self,db) -> List[AnalyticsEvent]:
        return (
            db.query(AnalyticsEvent)
            .order_by(AnalyticsEvent.created_at.desc())
            .all()
        )

    def get_events_by_name(
        self,
        db,
        event_name: str
    ) -> List[AnalyticsEvent]:

        return (
            db.query(AnalyticsEvent)
            .filter(AnalyticsEvent.event_name == event_name)
            .order_by(AnalyticsEvent.created_at.desc())
            .all()
        )

    def get_events_by_user(
        self,
        db,
        user_id: int
    ) -> List[AnalyticsEvent]:

        return (
            db.query(AnalyticsEvent)
            .filter(AnalyticsEvent.user_id == user_id)
            .order_by(AnalyticsEvent.created_at.desc())
            .all()
        )

    def get_events_by_proposal(
        self,
        db,
        proposal_id: int
    ) -> List[AnalyticsEvent]:

        return (
            db.query(AnalyticsEvent)
            .filter(AnalyticsEvent.proposal_id == proposal_id)
            .order_by(AnalyticsEvent.created_at.desc())
            .all()
        )

    # -------------------------
    # Count
    # -------------------------

    def count_events(self,db) -> int:
        return db.query(AnalyticsEvent).count()

    def count_events_by_name(
        self,
        db,
        event_name: str
    ) -> int:

        return (
            db.query(AnalyticsEvent)
            .filter(AnalyticsEvent.event_name == event_name)
            .count()
        )

    # -------------------------
    # Delete
    # -------------------------

    def delete_event(self,db,event_id: int) -> bool:
        event = self.get_event_by_id(db,event_id)

        if not event:
            return False

        db.delete(event)
        db.commit()

        return True
    
    def get_recent_activity(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Returns latest analytics events.
        """

        return (
    db.query(
        AnalyticsEvent,
        Proposal,
        Job,
    )
    .join(
        Proposal,
        AnalyticsEvent.proposal_id == Proposal.id,
    )
    .join(
        Job,
        Proposal.job_id == Job.id,
    )
    .order_by(
        AnalyticsEvent.created_at.desc()
    )
    .limit(limit)
    .all()
)
    
    def get_proposal_funnel(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposal funnel counts.
        """

        proposals = (
            db.query(
                Proposal.status,
                func.count(Proposal.id),
            )
            .filter(
                Proposal.user_id == user_id
            )
            .group_by(
                Proposal.status
            )
            .all()
        )

        status_counts = {
            status: count
            for status, count in proposals
        }

        generated = (
            db.query(Proposal)
            .filter(
                Proposal.user_id == user_id
            )
            .count()
        )

        sent = (
            status_counts.get("Sent", 0)
            + status_counts.get("Accepted", 0)
            + status_counts.get("Rejected", 0)
        )

        accepted = status_counts.get("Accepted", 0)

        return {
            "generated": generated,
            "sent": sent,
            "accepted": accepted,
        }
    
    def get_feature_usage(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns feature usage counts grouped by event name.
        """

        return (
            db.query(
                AnalyticsEvent.event_name,
                func.count(AnalyticsEvent.id),
            )
            .filter(
                AnalyticsEvent.user_id == user_id
            )
            .group_by(
                AnalyticsEvent.event_name
            )
            .all()
        )
#     def count_events_between_dates(
#     self,
#     event_name,
#     start_date,
#     end_date,
# ):
        # ...
    
#     def get_events_between_dates(
#     self,
#     start_date,
#     end_date,
# ):
#     ...