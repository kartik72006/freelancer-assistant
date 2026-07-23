from database.repositories.analytics_repository import AnalyticsRepository
from services.ai.gemini_service import GeminiService
from agents.analyzer_agent import AnalyzerAgent
from agents.proposal_agent import ProposalAgent
from agents.review_agent import ReviewAgent
from services.ai.orchestrator_service import AgentOrchestrator
from services.application.analytics_service import AnalyticsService
from services.application.proposal_service import ProposalService
from services.application.analysis_service import AnalysisService
from services.application.review_service import ReviewService
from database.repositories.job_repository import JobRepository
from database.repositories.proposal_repository import ProposalRepository
from services.retrieval.retrieval_service import RetrievalService
from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.semantic_retriever import SemanticRetriever
from services.retrieval.chroma_vector_store import ChromaVectorStore
from services.retrieval.context_fromatter import ContextFormatter
from services.retrieval.knowledge_base_indexer import KnowledgeBaseIndexer

print("1")
gemini_service = GeminiService()
print("2")
embedding_service = EmbeddingService()
print("3")
vector_store = ChromaVectorStore()
print("4")
semantic_retriever = SemanticRetriever()
print("5")
context_formatter = ContextFormatter()
print("6")
knowledge_base_indexer = KnowledgeBaseIndexer(
    embedding_service,
    vector_store
)
print("7")
retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
    semantic_retriever=semantic_retriever,
    context_formatter=context_formatter,
    knowledge_base_indexer=knowledge_base_indexer,
)
print("8")

analyzer_agent = AnalyzerAgent()
print("9")
proposal_agent = ProposalAgent(gemini_service,retrieval_service)
print("10")
review_agent = ReviewAgent(gemini_service)
print("11")
orchestrator = AgentOrchestrator(analyzer_agent, proposal_agent, review_agent)
print("12")
job_repository = JobRepository()
print("13")
proposal_repository = ProposalRepository()
print("14")
analytics_repository= AnalyticsRepository()
print("15")
analytics_service = AnalyticsService(
    analytics_repository=analytics_repository,
    proposal_repository=proposal_repository,
)
print("16")
proposal_service = ProposalService(
    orchestrator=orchestrator,
    job_repository=job_repository,
    proposal_repository=proposal_repository,
    analytics_service=analytics_service,
)
print("17")
review_service = ReviewService(orchestrator)
print("18")
analysis_service = AnalysisService(orchestrator)