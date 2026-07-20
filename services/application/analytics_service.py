from typing import Optional
import re
from database.repositories.analytics_repository import AnalyticsRepository
from sqlalchemy.orm import Session
import json
from api.schemas.proposal_responses.dashboard_stats import DashboardStatsResponse
from database.repositories.proposal_repository import ProposalRepository
from api.schemas.proposal_responses.analytics import (
    StatusDistributionItem,
    StatusDistributionResponse,
    ProposalTrendItem,
    ProposalTrendResponse,
    AIScoreTrendItem,
    AIScoreTrendResponse,
    AcceptanceTrendItem,
    AcceptanceTrendResponse,
    RecentActivityItem,
    RecentActivityResponse,
    TopClientItem,
    TopClientsResponse,
    FeatureUsageItem,
    FeatureUsageResponse,
    ProductHealthResponse
)
from collections import defaultdict

class AnalyticsService:
    """
    Handles product analytics operations.

    This service acts as the business layer between
    application services and the analytics repository.
    """

    def __init__(self, analytics_repository: AnalyticsRepository,proposal_repository: ProposalRepository):
        self.analytics_repository = analytics_repository
        self.proposal_repository = proposal_repository

    # ----------------------------------
    # Event Logging
    # ----------------------------------

    def log_event(
        self,
        db:Session,
        event_name: str,
        proposal_id: Optional[int] = None,
        user_id: Optional[int] = None,
        properties: Optional[dict] = None,
    ):
        """
        Log a new analytics event.
        """

        return self.analytics_repository.create_event(
            db=db,
            event_name=event_name,
            proposal_id=proposal_id,
            user_id=user_id,
            properties=properties,
        )

    # ----------------------------------
    # Event Retrieval
    # ----------------------------------

    def get_all_events(self,db:Session):
        return self.analytics_repository.get_events(db=db)

    def get_events_by_name(self, db:Session, event_name: str):
        return self.analytics_repository.get_events_by_name(db=db, event_name=event_name)

    def get_events_by_user(self, db:Session, user_id: int):
        return self.analytics_repository.get_events_by_user(db=db, user_id=user_id)

    def get_events_by_proposal(self, db:Session, proposal_id: int):
        return self.analytics_repository.get_events_by_proposal(db=db, proposal_id=proposal_id)

    # ----------------------------------
    # Event Statistics
    # ----------------------------------

    def count_events(self, db: Session):
        """
        Count all analytics events.
        """
        return self.analytics_repository.count_events(db=db)

    def count_events_by_name(self, db: Session, event_name: str):
        return self.analytics_repository.count_events_by_name(db=db, event_name=event_name)
    
    def get_dashboard_stats(
            self,
            db,
            user_id: int
        ):
                proposals = self.proposal_repository.get_proposals_by_user(
                    db=db,
                    user_id=user_id
                )
                    
                total_proposals = len(proposals)

                proposals_sent = len(
                [
                    p for p in proposals
                    if p.status in (
                        "Sent",
                        "Accepted",
                        "Rejected"
                    )
                ]
            )

                accepted_proposals = len(
                [
                    p for p in proposals
                    if p.status == "Accepted"
                ]
            )
                
                acceptance_rate = (
                    accepted_proposals / proposals_sent * 100
                    if proposals_sent
                    else 0
                )

                scores = []

                for proposal in proposals:

                    review = self._parse_review(proposal)

                    scores.append(
                        review.get(
                            "overallScore",
                            0
                        )
                    )

                average_ai_score = (
                    sum(scores) / len(scores)
                    if scores
                    else 0
                )

                average_response_days = 0

                return DashboardStatsResponse(
                    total_proposals=total_proposals,
                    proposals_sent=proposals_sent,
                    accepted_proposals=accepted_proposals,
                    acceptance_rate=round(
                        acceptance_rate,
                        1
                    ),
                    average_ai_score=round(
                        average_ai_score,
                        1
                    ),
                    average_response_days=average_response_days
                )
    
    def get_status_distribution(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposal status distribution for dashboard.
        """

        results = self.proposal_repository.get_status_distribution(
            db=db,
            user_id=user_id,
        )

        return StatusDistributionResponse(
            data=[
                StatusDistributionItem(
                    status=status,
                    count=count,
                )
                for status, count in results
            ]
        )
    
    def get_proposal_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposal generation trend.
        """

        results = self.proposal_repository.get_proposal_trend(
            db=db,
            user_id=user_id,
        )

        return ProposalTrendResponse(
            data=[
                ProposalTrendItem(
                    month=period,
                    proposals=generated,
                    accepted=accepted or 0,
                )
                for period, generated, accepted in results
            ]
        )
    
    def _parse_review(self, proposal):
        """
        Safely parse the proposal review JSON.
        """

        if not proposal.review:
            return {}

        try:
            return json.loads(proposal.review)
        except Exception:
            return {}
        
    

    def _parse_pricing(self, pricing: str) -> float:
            """
            Extract the estimated quoted price.
            Returns the average if a range is provided.
            """

            if not pricing:
                return 0

            numbers = re.findall(r"\d[\d,]*", pricing)

            values = [
                int(n.replace(",", ""))
                for n in numbers
            ]

            if len(values) >= 2:
                return (values[0] + values[1]) / 2

            if len(values) == 1:
                return values[0]

            return 0


    def get_ai_score_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns average AI score grouped by month.
        """

        proposals = self.proposal_repository.get_proposals_for_ai_trend(
            db=db,
            user_id=user_id,
        )

        monthly_scores = defaultdict(list)

        for proposal in proposals:

            review = self._parse_review(proposal)

            score = review.get("overallScore", 0)

            period = proposal.created_at.strftime("%Y-%m")

            monthly_scores[period].append(score)

        data = []

        for period in sorted(monthly_scores.keys()):

            scores = monthly_scores[period]

            average = sum(scores) / len(scores)

            data.append(
                AIScoreTrendItem(
                    month=period,
                    aiScore=round(average, 1)
                )
            )

        return AIScoreTrendResponse(data=data)
    
    def get_acceptance_trend(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns monthly acceptance rate.
        """

        proposals = self.proposal_repository.get_proposals_for_acceptance_trend(
            db=db,
            user_id=user_id,
        )

        monthly = defaultdict(
            lambda: {
                "accepted": 0,
                "sent": 0,
            }
        )

        for proposal in proposals:

            period = proposal.created_at.strftime("%Y-%m")

            if proposal.status in (
                "Sent",
                "Accepted",
                "Rejected",
            ):
                monthly[period]["sent"] += 1

            if proposal.status == "Accepted":
                monthly[period]["accepted"] += 1

        data = []

        for period in sorted(monthly.keys()):

            accepted = monthly[period]["accepted"]
            sent = monthly[period]["sent"]

            rate = (
                accepted / sent * 100
                if sent
                else 0
            )

            data.append(
                AcceptanceTrendItem(
                    month=period,
                    rate=round(rate, 1)
                )
            )

        return AcceptanceTrendResponse(data=data)
    
    def _get_activity_type(
        self,
        event_name: str,
    ) -> str:
        mapping = {
            "proposal_saved": "saved",
            "proposal_sent": "sent",
            "proposal_status_updated": "accepted",
            "proposal_deleted": "deleted",
            "proposal_duplicated": "duplicated",
        }

        return mapping.get(event_name, "saved")


    def _get_activity_text(
        self,
        event_name: str,
    ) -> str:
        mapping = {
            "proposal_saved": "Proposal saved",
            "proposal_sent": "Proposal sent",
            "proposal_status_updated": "Proposal accepted",
            "proposal_deleted": "Proposal deleted",
            "proposal_duplicated": "Proposal duplicated",
        }

        return mapping.get(
            event_name,
            event_name.replace("_", " ").title(),
        )

    def get_recent_activity(
            self,
            db: Session,
            limit: int = 5,
        ):
            """
            Returns recent analytics events.
            """

            events = self.analytics_repository.get_recent_activity(
                db=db,
                limit=limit,
            )



            return RecentActivityResponse(
                data=[
                    RecentActivityItem(
                        id=event.id,
                        type=self._get_activity_type(event.event_name),
                        title=job.title,
                        client=job.client_name,
                        description=self._get_activity_text(event.event_name),
                        created_at=event.created_at,
                    )
                    for event, proposal, job in events
                ]
            )
    
    def get_top_clients(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns top clients based on proposal history.
        """

        proposals = self.proposal_repository.get_proposals_with_jobs(
            db=db,
            user_id=user_id,
        )

        clients = defaultdict(
            lambda: {
                "won": 0,
                "total": 0,
                "revenue": 0,
            }
        )


        for proposal in proposals:

            if proposal.job is None:
                continue

            client = proposal.job.client_name or "Unknown"

            clients[client]["total"] += 1

            if proposal.status == "Accepted":

                clients[client]["won"] += 1

                revenue = self._parse_pricing(
                    proposal.pricing
                )

                clients[client]["revenue"] += revenue

        data = []

        for client, stats in clients.items():

            rate = (
                stats["won"] / stats["total"] * 100
                if stats["total"]
                else 0
            )

            data.append(
                TopClientItem(
                    client_name=client,
                    won=stats["won"],
                    total=stats["total"],
                    revenue=stats['revenue'],
                    win_rate=round(rate, 1),
                )
            )

        data.sort(
            key=lambda x: (x.revenue, x.win_rate),
            reverse=True,
        )

        return TopClientsResponse(
            data=data[:5]
        )
    
    def get_proposal_funnel(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns proposal funnel with conversion rates.
        """

        funnel = self.analytics_repository.get_proposal_funnel(
            db=db,
            user_id=user_id,
        )

        generated = funnel["generated"]
        sent = funnel["sent"]
        accepted = funnel["accepted"]

        send_rate = (
            round(sent / generated * 100, 1)
            if generated
            else 0
        )

        acceptance_rate = (
            round(accepted / sent * 100, 1)
            if sent
            else 0
        )

        overall_success_rate = (
            round(accepted / generated * 100, 1)
            if generated
            else 0
        )

        return {
            "counts": {
                "generated": generated,
                "sent": sent,
                "accepted": accepted,
            },
            "conversion": {
                "send_rate": send_rate,
                "acceptance_rate": acceptance_rate,
                "overall_success_rate": overall_success_rate,
            },
        }
    
    def get_feature_usage(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns feature usage statistics.
        """

        results = self.analytics_repository.get_feature_usage(
            db=db,
            user_id=user_id,
        )

        feature_names = {
            "proposal_generated": "Proposal Generated",
            "proposal_sent": "Proposal Sent",
            "proposal_accepted": "Proposal Accepted",
            "proposal_rejected": "Proposal Rejected",
            "proposal_edited": "Proposal Edited",
            "proposal_duplicated": "Proposal Duplicated",
            "proposal_deleted": "Proposal Deleted",
            "proposal_exported": "Proposal Exported",
        }

        # Initialize all features with 0
        feature_counts = {key: 0 for key in feature_names}

        # Populate counts from DB
        for event_name, count in results:
            if event_name in feature_counts:
                feature_counts[event_name] = count

        # Build response
        data = [
            FeatureUsageItem(
                feature=feature_names[event_name],
                count=count,
            )
            for event_name, count in feature_counts.items()
        ]

        # Sort by usage
        data.sort(key=lambda x: x.count, reverse=True)

        return FeatureUsageResponse(data=data)
    
    def get_product_health(
        self,
        db: Session,
        user_id: int,
    ):
        """
        Returns overall product health summary.
        """

        dashboard = self.get_dashboard_stats(
            db=db,
            user_id=user_id,
        )

        feature_usage = self.get_feature_usage(
            db=db,
            user_id=user_id,
        )

        top_clients = self.get_top_clients(
            db=db,
            user_id=user_id,
        )

        ignored_features = {
            "Proposal Deleted",
            "Proposal Duplicated",
            "Proposal Exported",
            "Proposal Edited"
        }

        filtered = [
            feature
            for feature in feature_usage.data
            if feature.feature not in ignored_features
        ]

        most_used_feature = (
            filtered[0].feature
            if filtered
            else "N/A"
        )

        top_client = (
            top_clients.data[0].client_name
            if top_clients.data
            else "N/A"
        )

        proposal_success_rate = (
            round(
                dashboard.accepted_proposals
                / dashboard.total_proposals
                * 100,
                1,
            )
            if dashboard.total_proposals
            else 0
        )

        if proposal_success_rate >= 70:
            health = "Excellent"

        elif proposal_success_rate >= 50:
            health = "Good"

        elif proposal_success_rate >= 30:
            health = "Needs Improvement"

        else:
            health = "Poor"

        return ProductHealthResponse(
            health_status=health,
            total_proposals=dashboard.total_proposals,
            proposal_success_rate=proposal_success_rate,
            acceptance_rate=dashboard.acceptance_rate,
            average_ai_score=dashboard.average_ai_score,
            most_used_feature=most_used_feature,
            top_client=top_client,
        )
