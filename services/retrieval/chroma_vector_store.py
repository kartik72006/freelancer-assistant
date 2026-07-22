from typing import Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings

from config.settings import CHROMA_COLLECTION_NAME, CHROMA_DB_PATH, TOP_K


class ChromaVectorStore:
    """
    Persistent vector store using ChromaDB.

    Responsibilities:
    - Store project embeddings
    - Store project metadata
    - Perform similarity search
    - Manage the collection

    Does NOT:
    - Generate embeddings
    - Read JSON files
    - Rank results
    - Format context
    """

    def __init__(
        self,
        collection_name: str = CHROMA_COLLECTION_NAME,
        persist_directory = CHROMA_DB_PATH,
    ):
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "AI Freelancer Proposal Assistant Knowledge Base",
                "hnsw:space": "cosine"
            },
        )

         

        print("=" * 60)
        print("CHROMA_DB_PATH:", CHROMA_DB_PATH)
        print("Resolved path:", Path(CHROMA_DB_PATH).resolve())
        print("Path exists:", Path(CHROMA_DB_PATH).exists())

        print("Contents:")
        for item in Path(CHROMA_DB_PATH).iterdir():
            print(" -", item)

        print("=" * 60)

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def add_document(self, project: Dict[str, Any], embedding) -> None:
        """
        Add a project to the vector store.
        """

        self.collection.add(
            ids=[project["id"]],
            embeddings=[embedding],
            documents=[self._build_search_text(project)],
            metadatas=[self._build_metadata(project)],
        )

    def search(
        self,
        query_embedding,
        top_k: int = TOP_K,
        where: Optional[Dict[str, Any]] = None,
    ):
        """
        Perform semantic similarity search.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
        )

    def count(self) -> int:
        """
        Number of indexed documents.
        """

        return self.collection.count()

    def clear(self) -> None:
        """
        Remove all indexed documents.
        """

        existing = self.collection.get()

        ids = existing.get("ids", [])

        if ids:
            self.collection.delete(ids=ids)

    def is_empty(self) -> bool:
        """
        Returns True if the collection has no indexed documents.
        """
        print("Collection count:", self.collection.count())
        print("Collection name:", self.collection.name)
        print("Collections:", [c.name for c in self.client.list_collections()])

        return self.count() == 0

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    def _build_metadata(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lightweight metadata used for filtering.
        """

        return {
            "title": project["title"],
            "role": project["role"],
            "domain": project["domain"],
            "project_type": project["project_type"],
            "source": "projects.json",
        }

    def _build_search_text(self, project: Dict[str, Any]) -> str:
        """
        Rich semantic document that gets embedded and retrieved.
        """

        return f"""
Title:
{project['title']}

Role:
{project['role']}

Domain:
{project['domain']}

Project Type:
{project['project_type']}

Problem Solved:
{project['problem']}

Description:
{project['description']}

Responsibilities:
{", ".join(project['responsibilities'])}

Technical Solution:
{project['technical_solution']}

Architecture:
{project['architecture']}

Key Features:
{", ".join(project['key_features'])}

Technologies:
{", ".join(project['technologies'])}

Business Impact:
{project['business_impact']}

Results:
{project['results']}

Skills:
{", ".join(project['skills'])}
""".strip()