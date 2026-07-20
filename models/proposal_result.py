from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ProposalResult:
    analysis: Any = None
    proposal: Optional[Any] = None
    pricing: Optional[Any] = None
    review: Optional[Any] = None

    def summary(self):
        return {
            "analysis": self.analysis,
            "proposal": self.proposal,
            "pricing": self.pricing,
            "review": self.review,
        }