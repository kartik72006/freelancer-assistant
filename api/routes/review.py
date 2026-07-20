from fastapi import APIRouter, HTTPException

from api.dependencies import review_service

from api.schemas.proposal_responses.review import ReviewResponse
from api.schemas.requests.review import ReviewRequest

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


@router.post("/generate", response_model=ReviewResponse)
def get_review(request: ReviewRequest):

    try:

        result = review_service.review_proposal(
            request.job_description,
            request.proposal
        )
        
        return ReviewResponse(
            overallScore=result.review["overallScore"],
            verdict=result.review["verdict"],
            metrics=result.review["metrics"],
            strengths=result.review["strengths"],
            improvements=result.review["improvements"],
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )