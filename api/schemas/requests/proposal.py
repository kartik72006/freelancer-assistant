from pydantic import BaseModel, Field


class ProposalRequest(BaseModel):
    job_description: str = Field(
        ...,
        example="Looking for a Python developer to build REST APIs."
    )