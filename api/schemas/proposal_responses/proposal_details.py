from datetime import datetime

from pydantic import BaseModel


class ProposalDetailsResponse(BaseModel):

    id: int

    title: str

    client: str

    budget: str

    created_at: datetime

    category: str

    status: str

    overall_score: float

    job_description: str

    final_proposal: dict | None

    analysis: dict

    proposal: dict

    pricing: str

    timeline: str

    review: dict

    class Config:
        from_attributes = True