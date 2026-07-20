from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):

    total_proposals: int

    proposals_sent: int

    accepted_proposals: int

    acceptance_rate: float

    average_ai_score: float

    average_response_days: float