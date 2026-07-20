from pydantic import BaseModel
from typing import Any

class SaveProposalRequest(BaseModel):
    job_description: str

    title: str
    client_name: str
    budget: str
    final_proposal: Any | None = None
    analysis: Any
    proposal: Any
    pricing: Any
    review: Any

    timeline: str | None = None