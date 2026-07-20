from services.ai.prompt_service import PromptService
from services.ai.knowledge_service import KnowledgeService
from utils.json_parser import parse_json


class ProposalAgent:

    def __init__(
        self,
        llm,
        retrieval_service
    ):
        self.llm = llm
        self.retrieval_service=retrieval_service

    def generate(
        self,
        job_description,
        prompt_version="v1",
    ):

        profile = (
            KnowledgeService.load_profile()
        )

        retrieval = self.retrieval_service.search(job_description)

        context = retrieval["context"]

        prompt = (PromptService.proposal_prompt(profile,
                                                context,
                                                job_description,
                                                prompt_version
                                            )
        )

        proposal = (
            self.llm.generate(
                prompt
            )
        )
        proposal = parse_json(proposal)

        if proposal is None:
            return {
                "introduction": "",
                "relevantExperience": "",
                "approach": "",
                "timeline": "Unavailable",
                "pricing": "Unavailable"
            }

        return proposal