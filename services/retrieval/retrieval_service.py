from config.settings import CANDIDATE_K, MIN_SIMILARITY_SCORE, PROJECTS_FILE, TOP_K


class RetrievalService:
    def __init__(
        self,
        embedding_service,
        vector_store,
        semantic_retriever,
        context_formatter,
        knowledge_base_indexer
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.semantic_retriever = semantic_retriever
        self.context_formatter = context_formatter
        self.knowledge_base_indexer=knowledge_base_indexer

    def initialize(self):
        if self.knowledge_base_indexer.is_indexed():
            return

        print("Knowledge base not found. Building index...")

        self.knowledge_base_indexer.index_projects(PROJECTS_FILE)

        print("Knowledge base indexed successfully.")

    def search(self, job_description, top_k=TOP_K, candidate_k=CANDIDATE_K, min_score=MIN_SIMILARITY_SCORE,where=None):
        jd_embedding = self.embedding_service.generate_embedding(job_description)
        response = self.semantic_retriever.search(job_description,jd_embedding, self.vector_store, top_k, candidate_k, min_score, where)
        
        results = response["results"]
        stats = response["stats"]
        context = self.context_formatter.format(results)

        return {
            "context": context,
            "stats": stats
        }
