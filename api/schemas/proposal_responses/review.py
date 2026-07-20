from pydantic import BaseModel


class ReviewMetrics(BaseModel):
    professionalism: int
    personalization: int
    clarity: int
    tone: int


class ReviewResponse(BaseModel):
    overallScore: int
    verdict: str
    metrics: ReviewMetrics
    strengths: list[str]
    improvements: list[str]