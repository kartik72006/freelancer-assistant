from services.ai.prompt_service import PromptService
from utils.json_parser import parse_json

class PricingAgent:

    def __init__(
        self,
        llm
    ):
        self.llm = llm

    def estimate(
        self,
        job_description,
        complexity
    ):

        prompt = (
            PromptService.pricing_prompt(
                job_description,
                complexity
            )
        )

        pricing = self.llm.generate(prompt)

        if pricing is None:
            return {
                "price": "Unavailable",
                "timeline": "Unavailable"
            }

        return (parse_json(pricing))