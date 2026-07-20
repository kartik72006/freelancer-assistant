from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.semantic_retriever import SemanticRetriever
from services.retrieval.vector_store import VectorStore
import json
# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore()
semantic_retriever = SemanticRetriever()

with open("knowledge_base/projects.json", "r", encoding="utf-8") as file:
    projects = json.load(file)

for project in projects:

    search_text = f"""
    Title: {project['title']}

    Technologies:
    {', '.join(project['tech_stack'])}

    Description:
    {project['description']}
    """

    embedding = embedding_service.generate_embedding(search_text)

    vector_store.add_document(project, embedding)

query = """
Looking for an experienced FastAPI and Python backend developer
"""

query_embedding = embedding_service.generate_embedding(query)
response = semantic_retriever.search(query_embedding, vector_store, 3,15,0.5)


assert isinstance(response, dict)

assert "results" in response
assert "stats" in response

results = response["results"]
assert isinstance(results, list)

assert len(results) > 0

for result in results:

    assert "project" in result
    assert "score" in result
    assert "text" in result
    assert "metadata" in result

    assert -1 <= result["score"] <= 1

    metadata = result["metadata"]
    assert isinstance(metadata, dict)

    assert "tech_stack" in metadata
    assert isinstance(metadata["tech_stack"], list) 

projects = [result["project"] for result in results]

assert len(projects) == len(set(projects))


stats = response["stats"]
assert "total_documents" in stats
assert "candidate_results" in stats
assert "filtered_results" in stats
assert "unique_results" in stats
assert "average_similarity" in stats

assert stats["total_documents"] > 0

assert stats["candidate_results"] <= stats["total_documents"]

assert stats["filtered_results"] <= stats["candidate_results"]

assert stats["unique_results"] <= stats["filtered_results"]

print("\nTop 3 Results:")

for result in results:
    print(f"\nProject: {result['project']}")
    print(f"Score: {result['score']:.4f}")
    print(f"Description: {result['text']}")

    tech_stack = result["metadata"].get("tech_stack", [])
    print(f"Tech Stack: {', '.join(tech_stack)}")

print("\nRetrieval Statistics")
print("-" * 30)

for key, value in stats.items():
    print(f"{key}: {value}")

print("\n✅ All semantic retrieval tests passed!")