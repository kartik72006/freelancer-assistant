from datetime import datetime

from pydantic import BaseModel


class ProposalHistoryResponse(BaseModel):
    id: int
    title: str
    client: str
    budget: str
    category: str
    overall_score: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True