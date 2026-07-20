from sqlalchemy.orm import Session
import json
from api.schemas.proposal_responses.dashboard_stats import DashboardStatsResponse
from api.schemas.proposal_responses.save_proposal import SaveProposalResponse
from api.schemas.proposal_responses.proposal_history import ProposalHistoryResponse
from api.schemas.proposal_responses.proposal_details import ProposalDetailsResponse

class ProposalService:

    def __init__(
        self,
        orchestrator,
        job_repository,
        proposal_repository,
        analytics_service     
    ):
        self.orchestrator = orchestrator
        self.job_repository = job_repository
        self.proposal_repository = proposal_repository
        self.analytics_service = analytics_service

    def generate_proposal(self, job_description,prompt_version:str="v1"):

        return self.orchestrator.generate_proposal(
            job_description,prompt_version
        )
    
    def save_proposal(
        self,
        db: Session,
        request
    ):
        saved_job = self.job_repository.create(
        db=db,
        title=request.title,
        description=request.job_description,
        client_name=request.client_name,
        budget=request.budget
    )
        saved_proposal = self.proposal_repository.create(
            db=db,
            job_id=saved_job.id,
            user_id=1,  # Temporary until authentication is implemented
            analysis=json.dumps(request.analysis),
            proposal=json.dumps(request.proposal),
            pricing=request.pricing,
            timeline=request.timeline,
            review=json.dumps(request.review),
            final_proposal=json.dumps(request.final_proposal) if request.final_proposal else None,
            model="gemini",
            prompt_version="v1",
            status="Saved",
            category = request.analysis["projectType"],
        )
        print(request.review)
        self.analytics_service.log_event(
            db=db,
            event_name="proposal_generated",
            proposal_id=saved_proposal.id,
            user_id=1,
            properties={
                "category": request.analysis["projectType"],
            }
        )

        return SaveProposalResponse(
            id=saved_proposal.id,
            message="Proposal saved successfully"
        )

    def get_history(
        self,
        db,
        user_id: int
    ):
        """
        Returns proposal history for the dashboard.
        """

        proposals = self.proposal_repository.get_history(
            db=db,
            user_id=user_id
        )

        history = []

        for proposal in proposals:

            review = json.loads(proposal.review)

            history.append(

                ProposalHistoryResponse(

                    id=proposal.id,

                    title=proposal.job.title,

                    client=proposal.job.client_name,

                    budget=proposal.job.budget,

                    category=proposal.category,

                    overall_score=review.get("overallScore", 0),

                    status=proposal.status,

                    created_at=proposal.created_at

                )

            )

        return history
    
    def get_proposal_details(
        self,
        db,
        proposal_id: int
    ):
        proposal = self.proposal_repository.get_by_id(
        db,
        proposal_id
    )
        if proposal is None:
            return None
        
        analysis = json.loads(proposal.analysis)
        proposal_content = json.loads(proposal.proposal)
        review = json.loads(proposal.review)
        pricing = proposal.pricing
        final_proposal = json.loads(proposal.final_proposal) if proposal.final_proposal else None
        return ProposalDetailsResponse(
            id=proposal.id,

            title=proposal.job.title,

            client=proposal.job.client_name,

            budget=proposal.job.budget,

            created_at=proposal.created_at,

            category=proposal.category,

            status=proposal.status,

            overall_score=review.get("overallScore", 0),

            job_description=proposal.job.description,

            analysis=analysis,

            proposal=proposal_content,

            pricing=pricing,

            timeline=proposal.timeline,

            review=review,
            final_proposal=final_proposal
        )
    
    def get_dashboard_stats(
    self,
    db,
    user_id: int
):
        proposals = self.proposal_repository.get_all(
            db=db
        )

        proposals = [
            proposal
            for proposal in proposals
            if proposal.user_id == user_id
        ]
            
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

            review = json.loads(proposal.review)

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
    
    def update_status(
        self,
        db,
        proposal_id: int,
        status: str
    ):
        proposal = self.proposal_repository.get_by_id(
            db,
            proposal_id
        )

        old_status=proposal.status
        proposal = self.proposal_repository.update_status(
            db=db,
            proposal_id=proposal_id,
            new_status=status
        )
        
        event_mapping = {
            "Sent": "proposal_sent",
            "Accepted": "proposal_accepted",
            "Rejected": "proposal_rejected",
            "Saved": "proposal_saved",
        }

        self.analytics_service.log_event(
            db=db,
            event_name=event_mapping.get(
                status,
                "proposal_status_updated",
            ),
            proposal_id=proposal.id,
            user_id=proposal.user_id,
            properties={
                "old_status": old_status,
                "new_status": status,
            },
        )

        if proposal is None:
            raise ValueError("Proposal not found")

        return proposal
    
    def update_final_proposal(
        self,
        db,
        proposal_id: int,
        final_proposal: dict
    ):
        proposal = self.proposal_repository.update_final_proposal(
            db=db,
            proposal_id=proposal_id,
            final_proposal=json.dumps(final_proposal)
        )

        self.analytics_service.log_event(
            db=db,
            event_name="proposal_edited",
            proposal_id=proposal.id,
            user_id=proposal.user_id,
            properties={
                "edited": True
            }
        )

        if proposal is None:
            raise ValueError("Proposal not found")

        return proposal
    
    def duplicate_proposal(
        self,
        db,
        proposal_id: int
    ):
        proposal = self.proposal_repository.get_by_id(
            db,
            proposal_id
        )

        original_job = proposal.job

        new_job = self.job_repository.create(
            db=db,
            title=original_job.title,
            description=original_job.description,
            client_name=original_job.client_name,
            budget=original_job.budget,
        )

        if proposal is None:
            raise ValueError("Proposal not found")

        duplicated = self.proposal_repository.duplicate(
            db=db,
            proposal=proposal,
            job_id=new_job.id
        )

        self.analytics_service.log_event(
            db=db,
            event_name="proposal_duplicated",
            proposal_id=duplicated.id,
            user_id=duplicated.user_id,
            properties={
                "source_proposal": proposal.id
            }
        )

        return SaveProposalResponse(
            id=duplicated.id,
            message="Proposal duplicated successfully"
        )
    
    def delete_proposal(
        self,
        db,
        proposal_id: int
    ):
        proposal = self.proposal_repository.get_by_id(
            db,
            proposal_id
        )

        if proposal is None:
            raise ValueError("Proposal not found")
        
        self.analytics_service.log_event(
                    db=db,
                    event_name="proposal_deleted",
                    proposal_id=proposal.id,
                    user_id=proposal.user_id,
                    properties={
                        "status": proposal.status
                    }
                )
        
        # Delete proposal
        self.proposal_repository.delete(
            db=db,
            db_object=proposal
        )

        # Delete the associated job
        self.job_repository.delete_by_id(
            db=db,
            object_id=proposal.job_id
        )

        return {
            "message": "Proposal deleted successfully"
        }