from fastapi import APIRouter, HTTPException

from api.dependencies import pricing_service


from api.schemas.requests.pricing import PricingRequest
from api.schemas.proposal_responses.pricing import PricingResponse

router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"]
)


@router.post("/generate", response_model=PricingResponse)
def get_pricing(request: PricingRequest):

    try:

        result = pricing_service.generate_pricing(
            request.job_description
        )

        return PricingResponse(
            analysis=result.analysis,
            proposal=result.proposal,
            pricing=result.pricing
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )