from models.proposal_result import ProposalResult


class AgentOrchestrator:

    def __init__(
    self,
    analyzer,
    proposal_agent,
    review_agent
    ):

        self.analyzer = analyzer
        self.proposal_agent = proposal_agent
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