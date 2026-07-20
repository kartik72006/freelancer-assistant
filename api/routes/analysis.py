

from fastapi import APIRouter, HTTPException

from api.dependencies import analysis_service


from api.schemas.requests.analysis import JobAnalysisRequest
from api.schemas.proposal_responses.analysis import JobAnalysisResponse

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.post("/analyze", response_model=JobAnalysisResponse)
def analyze(request: JobAnalysisRequest):

    try:

        result = analysis_service.analyze(
            request.job_description
        )
        return result.analysis

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )