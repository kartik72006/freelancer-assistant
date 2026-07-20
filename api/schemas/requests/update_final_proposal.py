from pydantic import BaseModel
from typing import Any

class UpdateFinalProposalRequest(BaseModel):
    final_proposal: Any