from agents.review_agent import ReviewAgent


class ReviewService:
    """
    Responsible for reviewing proposals.
    """

    def __init__(
        self,
        orchestrator
    ):
        self.orchestrator = orchestrator

    def review_proposal(
    self,
    job_description,
    proposal
    ):

        return self.orchestrator.review_proposal(
            job_description,
            proposal
        )