from services.ai.prompt_service import PromptService
from utils.json_parser import parse_json

class ReviewAgent:

    def __init__(
        self,
        llm
    ):
        self.llm = llm

    def review(
        self,
        proposal
    ):

        proposal_text = f"""
        Introduction:
        {proposal["introduction"]}

        Relevant Experience:
        {proposal["relevantExperience"]}

        Approach:
        {proposal["approach"]}

        Timeline:
        {proposal["timeline"]}

        Pricing:
        {proposal["pricing"]}
        """

        prompt = PromptService.review_prompt(
            proposal_text
        )

        review = self.llm.generate(prompt)

        if review is None:
            return {
                "overallScore": 0,
                "verdict": "Generation Failed",
                "metrics": {
                    "professionalism": 0,
                    "personalization": 0,
                    "clarity": 0,
                    "tone": 0
                },
                "strengths": [],
                "improvements": [
                    "Review generation failed."
                ]
            }

        return (parse_json(review))