from fastapi import APIRouter, HTTPException
from typing import List

from api.schemas.proposal_responses.dashboard_stats import DashboardStatsResponse
from api.schemas.proposal_responses.proposal_details import ProposalDetailsResponse
from api.schemas.proposal_responses.proposal_history import ProposalHistoryResponse
from api.schemas.requests.proposal import ProposalRequest
from api.schemas.proposal_responses.proposal import  ProposalResponse
from api.schemas.requests.save_proposal import SaveProposalRequest
from api.schemas.proposal_responses.save_proposal import SaveProposalResponse
from api.schemas.requests.update_final_proposal import UpdateFinalProposalRequest
from api.schemas.requests.update_status import UpdateStatusRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import get_db
from api.dependencies import proposal_service

router = APIRouter(
    prefix="/proposal",
    tags=["Proposal"]
)

@router.post(
    "/generate",
    response_model=ProposalResponse
)
def generate_proposal(request: ProposalRequest):

    try:
        result = proposal_service.generate_proposal(
            request.job_description
        )

        return ProposalResponse(
                proposal=result.proposal
            )
    
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.post(
    "/save",
    response_model=SaveProposalResponse
)
def save_proposal(
    request: SaveProposalRequest,
    db: Session = Depends(get_db)
):
    return proposal_service.save_proposal(
        db,
        request
    )

@router.get(
    "/history",
    response_model=List[ProposalHistoryResponse]
)
def get_proposal_history(
    db=Depends(get_db)
):
    """
    Returns all saved proposals for the dashboard.
    """

    return proposal_service.get_history(
        db=db,
        user_id=1
    )

@router.get(
    "/stats",
    response_model=DashboardStatsResponse
)
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    return proposal_service.get_dashboard_stats(
        db,
        user_id=1
    )

@router.put("/{proposal_id}/status")
def update_status(
    proposal_id: int,
    request: UpdateStatusRequest,
    db: Session = Depends(get_db)
):
    proposal = proposal_service.update_status(
        db=db,
        proposal_id=proposal_id,
        status=request.status
    )

    return {
        "id": proposal.id,
        "status": proposal.status
    }

@router.put("/{proposal_id}/final")
def update_final_proposal(
    proposal_id: int,
    request: UpdateFinalProposalRequest,
    db: Session = Depends(get_db)
):
    proposal_service.update_final_proposal(
        db=db,
        proposal_id=proposal_id,
        final_proposal=request.final_proposal
    )

    return {
        "message": "Final proposal updated successfully"
    }

@router.post(
    "/{proposal_id}/duplicate",
    response_model=SaveProposalResponse
)
def duplicate_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    return proposal_service.duplicate_proposal(
        db=db,
        proposal_id=proposal_id
    )

@router.get(
    "/{proposal_id}",
    response_model=ProposalDetailsResponse
)
def get_proposal_details(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    proposal = proposal_service.get_proposal_details(
    db,
    proposal_id
)
    if proposal is None:

        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )
    return proposal

@router.delete("/{proposal_id}")
def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    return proposal_service.delete_proposal(
        db=db,
        proposal_id=proposal_id
    )