from pydantic import BaseModel

class ProposalContent(BaseModel):
    introduction: str
    relevantExperience: str
    approach: str
    timeline: str
    pricing: str


class ProposalResponse(BaseModel):
    proposal: ProposalContent