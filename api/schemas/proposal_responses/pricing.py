from pydantic import BaseModel


class PricingResponse(BaseModel):
    analysis: dict
    proposal: str
    pricing: dict