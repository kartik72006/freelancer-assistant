from pydantic import BaseModel


class SkillEntry(BaseModel):
    label: str
    reason: str
    confidence: int


class JobAnalysisResponse(BaseModel):
    projectType: str
    skills: list[SkillEntry]
    complexity: str
    estimatedBudget: str
    timeline: str
    budgetConfidence: int
    timelineConfidence: int
    summary: str
    clientGoal: str
    toneSignals: list[str]
    redFlags: list[str]