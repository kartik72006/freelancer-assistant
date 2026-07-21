import json
from pathlib import Path
from typing import List, Dict, Any

from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.chroma_vector_store import ChromaVectorStore


class KnowledgeBaseIndexer:
    """
    Responsible for indexing the knowledge base into ChromaDB.

    Responsibilities:
    - Load knowledge base
    - Generate embeddings
    - Store in ChromaDB

    Does NOT:
    - Perform retrieval
    - Format context
    - Generate proposals
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ):
        self.embedding_service = embedding_service
        self.chroma_vector_store = vector_store

    # ------------------------------------------------------------------

    def index_projects(self, projects_path: str):
        """
        Index all projects into ChromaDB.
        """

        projects = self._load_projects(projects_path)

        for project in projects:

            search_text = self.chroma_vector_store._build_search_text(project)

            embedding = self.embedding_service.generate_embedding(search_text)

            self.chroma_vector_store.add_document(
                project=project,
                embedding=embedding,
            )


    # ------------------------------------------------------------------

    def rebuild_index(self, projects_path: str):
        """
        Delete existing index and rebuild it.
        """

        self.chroma_vector_store.clear()

        self.index_projects(projects_path)

    # ------------------------------------------------------------------

    def is_indexed(self) -> bool:
        """
        Returns True if ChromaDB already contains documents.
        """

        return not self.chroma_vector_store.is_empty()

    # ------------------------------------------------------------------

    @staticmethod
    def _load_projects(projects_path: str) -> List[Dict[str, Any]]:
        """
        Load projects.json
        """

        with open(Path(projects_path), "r", encoding="utf-8") as file:
            return json.load(file)