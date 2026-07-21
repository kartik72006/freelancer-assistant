from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.chroma_vector_store import ChromaVectorStore
from services.retrieval.knowledge_base_indexer import KnowledgeBaseIndexer

from config.settings import PROJECTS_FILE

embedding_service = EmbeddingService()
vector_store = ChromaVectorStore()

indexer = KnowledgeBaseIndexer(
    embedding_service,
    vector_store,
)

indexer.rebuild_index(PROJECTS_FILE)

print("Knowledge base indexed successfully.")