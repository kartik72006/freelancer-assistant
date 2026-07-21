from sentence_transformers import SentenceTransformer

from config.settings import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self):
        self._model = None

    def _get_model(self):
        if self._model is None:
            self._model = SentenceTransformer(EMBEDDING_MODEL)
        return self._model

    def generate_embedding(self, text: str):
        return self._get_model().encode(
            text,
            normalize_embeddings=True,
        )

    def generate_embeddings(self, texts: list[str]):
        return self._get_model().encode(
            texts,
            normalize_embeddings=True,
        )