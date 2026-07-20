
from services.ai.gemini_service import GeminiService
from services.ai.orchestrator_service import (
    AgentOrchestrator
)
from utils.display import display_result
from services.ai.openrouter_service import OpenRouterService
from agents.analyzer_agent import AnalyzerAgent
from agents.proposal_agent import ProposalAgent
from agents.review_agent import ReviewAgent
from agents.pricing_agent import PricingAgent

llm = GeminiService()

# llm = OpenRouterService()

analyzer = AnalyzerAgent()

proposal_agent = ProposalAgent(llm)

pricing_agent = PricingAgent(llm)

review_agent = ReviewAgent(llm)

orchestrator = AgentOrchestrator(

    analyzer,

    proposal_agent,

    pricing_agent,

    review_agent

)

job_description = """
Need a React and Node.js developer
to build a SaaS dashboard with authentication,
payment integration and analytics.
"""

result = (
    orchestrator.run(
        job_description
    )
)

display_result(result)