class AnalysisService:
    """
    Application service responsible for
    analyzing job descriptions.
    """

    def __init__(
        self,
        orchestrator
    ):
        self.orchestrator = orchestrator

    def analyze(self, job_description):

        return self.orchestrator.analyze(
            job_description
        )