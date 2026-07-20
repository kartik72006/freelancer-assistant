from dataclasses import dataclass
from typing import List


@dataclass
class FeedbackItem:
    criterion: str
    rating: str
    comment: str


@dataclass
class Evaluation:
    score: str
    feedback: List[FeedbackItem]