from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExperimentSample:
    job_id: str

    proposal: dict[str, Any]

    review: dict[str, Any]

    generation_time: float = 0.0

    metadata: dict[str, Any]= field(default_factory=dict)


@dataclass
class StrategyMetrics:
    overall_score: float = 0.0
    professionalism: float = 0.0
    personalization: float = 0.0
    clarity: float = 0.0
    tone: float = 0.0
    latency: float = 0.0


@dataclass
class StrategyResult:
    name: str
    metrics: StrategyMetrics
    samples: list[ExperimentSample] = field(default_factory=list)


@dataclass
class ExperimentResult:
    experiment_name: str
    strategy_a: StrategyResult
    strategy_b: StrategyResult
    winner: str
    improvement_percentage: float
    recommendation: str