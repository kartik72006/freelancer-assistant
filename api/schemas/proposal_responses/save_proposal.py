from pydantic import BaseModel

class SaveProposalResponse(BaseModel):
    id: int
    message: str