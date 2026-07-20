from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def generate_embedding(self, text: str):
        return self.model.encode(
            text,
            normalize_embeddings=True
        )
    
    def generate_embeddings(self, texts: list[str]):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )