import json

from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.vector_store import VectorStore

# Initialize services
embedding_service = EmbeddingService()
vector_store = VectorStore()

# Load projects
with open("knowledge_base/projects.json", "r", encoding="utf-8") as file:
    projects = json.load(file)

print(f"\nLoaded {len(projects)} projects.\n")

# Generate embeddings
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

    print(f"Embedded: {project['title']}")

print("\n----------------------------------")
print(f"Vector Store Size: {len(vector_store.get_all_documents())}")
print("----------------------------------")