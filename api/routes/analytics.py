from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from api.dependencies import analytics_service
from api.schemas.proposal_responses.dashboard_stats import DashboardStatsResponse
from api.schemas.proposal_responses.analytics import (StatusDistributionResponse,
                                                      ProposalTrendResponse,
                                                      AIScoreTrendResponse,
                                                      AcceptanceTrendResponse,
                                                      RecentActivityResponse,
                                                      TopClientsResponse,
                                                      FeatureUsageResponse,
                                                      ProductHealthResponse)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/dashboard",
    response_model=DashboardStatsResponse
)
def get_dashboard_stats(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    """
    Dashboard KPI cards.
    """

    return analytics_service.get_dashboard_stats(
        db=db,
        user_id=user_id
    )

@router.get(
    "/status-distribution",
    response_model=StatusDistributionResponse,
)
def get_status_distribution(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    """
    Returns proposal status distribution.
    """

    return analytics_service.get_status_distribution(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/proposal-trend",
    response_model=ProposalTrendResponse,
)
def get_proposal_trend(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    return analytics_service.get_proposal_trend(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/ai-score-trend",
    response_model=AIScoreTrendResponse,
)
def get_ai_score_trend(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    return analytics_service.get_ai_score_trend(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/acceptance-trend",
    response_model=AcceptanceTrendResponse,
)
def get_acceptance_trend(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    return analytics_service.get_acceptance_trend(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/recent-activity",
    response_model=RecentActivityResponse,
)
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return analytics_service.get_recent_activity(
        db=db,
        limit=limit,
    )

@router.get(
    "/top-clients",
    response_model=TopClientsResponse,
)
def get_top_clients(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    return analytics_service.get_top_clients(
        db=db,
        user_id=user_id,
    )

@router.get("/proposal-funnel")
def get_proposal_funnel(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    """
    Returns proposal funnel analytics.
    """

    return analytics_service.get_proposal_funnel(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/feature-usage",
    response_model=FeatureUsageResponse,
)
def get_feature_usage(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    """
    Returns feature usage analytics.
    """

    return analytics_service.get_feature_usage(
        db=db,
        user_id=user_id,
    )

@router.get(
    "/product-health",
    response_model=ProductHealthResponse,
)
def get_product_health(
    user_id: int = 1,
    db: Session = Depends(get_db),
):
    return analytics_service.get_product_health(
        db=db,
        user_id=user_id,
    )