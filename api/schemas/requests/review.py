from pydantic import BaseModel

class ReviewRequest(BaseModel):
    job_description: str
    proposal: dict