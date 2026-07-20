class PricingService:
    """
    Responsible for pricing generation.
    """

    def __init__(
        self,
        orchestrator
    ):
        self.orchestrator = orchestrator

    def generate_pricing(self, job_description):

        return self.orchestrator.generate_pricing(
            job_description
        )