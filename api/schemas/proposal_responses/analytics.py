from pydantic import BaseModel
from datetime import datetime

class StatusDistributionItem(BaseModel):
    status: str
    count: int


class StatusDistributionResponse(BaseModel):
    data: list[StatusDistributionItem]

class ProposalTrendItem(BaseModel):
    month: str
    proposals: int
    accepted: int


class ProposalTrendResponse(BaseModel):
    data: list[ProposalTrendItem]


class AIScoreTrendItem(BaseModel):
    month: str
    aiScore: float


class AIScoreTrendResponse(BaseModel):
    data: list[AIScoreTrendItem]


class AcceptanceTrendItem(BaseModel):
    month: str
    rate: float


class AcceptanceTrendResponse(BaseModel):
    data: list[AcceptanceTrendItem]

class RecentActivityItem(BaseModel):
    id: int
    type: str
    title: str
    client: str
    description: str
    created_at: datetime

class RecentActivityResponse(BaseModel):
    data: list[RecentActivityItem]

class TopClientItem(BaseModel):
    client_name: str
    won: int
    total: int
    revenue: float
    win_rate: float


class TopClientsResponse(BaseModel):
    data: list[TopClientItem]

class FeatureUsageItem(BaseModel):
    feature: str
    count: int


class FeatureUsageResponse(BaseModel):
    data: list[FeatureUsageItem]

class ProductHealthResponse(BaseModel):
    health_status: str
    total_proposals: int
    proposal_success_rate: float
    acceptance_rate: float
    average_ai_score: float
    most_used_feature: str
    top_client: str