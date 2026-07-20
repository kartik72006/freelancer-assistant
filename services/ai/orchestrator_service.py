from models.proposal_result import ProposalResult


class AgentOrchestrator:

    def __init__(
    self,
    analyzer,
    proposal_agent,
    pricing_agent,
    review_agent
    ):

        self.analyzer = analyzer
        self.proposal_agent = proposal_agent
        self.pricing_agent = pricing_agent
        self.review_agent = review_agent

    def analyze(self, job_description):

        analysis=self.analyzer.analyze(
            job_description
        )
        return ProposalResult(
            analysis=analysis
        )

    def generate_proposal(self, job_description,prompt_version="v1",):

        analysis_result = self.analyze(job_description)

        proposal = self.proposal_agent.generate(
            job_description,prompt_version
        )

        return ProposalResult(
            analysis=analysis_result.analysis,
            proposal=proposal
        )

    def generate_pricing(self, job_description):

        result = self.generate_proposal(job_description)
        pricing= self.pricing_agent.estimate(
                    job_description,
                    result.analysis["complexity"]
                )
        return ProposalResult(
            analysis=result.analysis,
            proposal=result.proposal,
            pricing=pricing
        )
    
    def review_proposal(
    self,
    job_description,
    proposal
):

        analysis = self.analyze(job_description)

        review = self.review_agent.review(
            proposal
        )

        return ProposalResult(
            analysis=analysis.analysis,
            proposal=proposal,
            review=review
        )

    def run(self, job_description,proposal):
        return self.review_proposal(job_description,proposal)