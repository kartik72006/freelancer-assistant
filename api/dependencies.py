from database.repositories.analytics_repository import AnalyticsRepository
from services.ai.gemini_service import GeminiService
from agents.analyzer_agent import AnalyzerAgent
from agents.proposal_agent import ProposalAgent
from agents.pricing_agent import PricingAgent
from agents.review_agent import ReviewAgent
from services.ai.orchestrator_service import AgentOrchestrator
from services.application.analytics_service import AnalyticsService
from services.application.proposal_service import ProposalService
from services.application.analysis_service import AnalysisService
from services.application.pricing_service import PricingService
from services.application.review_service import ReviewService
from database.repositories.job_repository import JobRepository
from database.repositories.proposal_repository import ProposalRepository
from services.retrieval.retrieval_service import RetrievalService
from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.semantic_retriever import SemanticRetriever
from services.retrieval.chroma_vector_store import ChromaVectorStore
from services.retrieval.context_fromatter import ContextFormatter
from services.retrieval.knowledge_base_indexer import KnowledgeBaseIndexer


gemini_service = GeminiService()

embedding_service = EmbeddingService()
vector_store = ChromaVectorStore()
semantic_retriever = SemanticRetriever()
context_formatter = ContextFormatter()
knowledge_base_indexer = KnowledgeBaseIndexer(
    embedding_service,
    vector_store
)

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
    semantic_retriever=semantic_retriever,
    context_formatter=context_formatter,
    knowledge_base_indexer=knowledge_base_indexer,
)

retrieval_service.initialize()

analyzer_agent = AnalyzerAgent()

proposal_agent = ProposalAgent(gemini_service,retrieval_service)

pricing_agent = PricingAgent(gemini_service)

review_agent = ReviewAgent(gemini_service)

orchestrator = AgentOrchestrator(analyzer_agent, proposal_agent, pricing_agent, review_agent)

job_repository = JobRepository()

proposal_repository = ProposalRepository()

analytics_repository= AnalyticsRepository()

analytics_service = AnalyticsService(
    analytics_repository=analytics_repository,
    proposal_repository=proposal_repository,
)

proposal_service = ProposalService(
    orchestrator=orchestrator,
    job_repository=job_repository,
    proposal_repository=proposal_repository,
    analytics_service=analytics_service,
)


pricing_service = PricingService(orchestrator)

review_service = ReviewService(orchestrator)

analysis_service = AnalysisService(orchestrator)