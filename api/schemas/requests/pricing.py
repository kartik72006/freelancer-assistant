from pydantic import BaseModel, Field


class PricingRequest(BaseModel):
    job_description: str = Field(
        ...,
        example="Looking for a Python developer to build REST APIs."
    )