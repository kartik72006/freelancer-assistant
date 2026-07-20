from app.experiments.experiment_strategy import ExperimentStrategy
from app.experiments.experiment_results import ExperimentSample
import time

class PromptV1Strategy(ExperimentStrategy):

    def __init__(self, proposal_service,review_agent):
        self.proposal_service = proposal_service
        self.review_agent=review_agent

    @property
    def name(self) -> str:
        return "Standard Proposal Prompt"  

    def execute(
    self,
    benchmark_job: dict,
) -> ExperimentSample:

        """
        Generates proposal using the improved prompt.
        """

        start = time.perf_counter()

        proposal_result = self.proposal_service.generate_proposal(
            benchmark_job["description"],
            prompt_version="v1",
        )

        generation_time = time.perf_counter() - start

        review_result = self.review_agent.review(
            proposal_result.proposal
        )

        return ExperimentSample(
            job_id=benchmark_job["id"],
            proposal=proposal_result.proposal,
            review=review_result,
            generation_time=generation_time,
            metadata={
                "prompt_version": "v1",
            },
        )
    