from enum import Enum


class ExperimentType(str, Enum):
    PROMPT = "prompt"
    RAG = "rag"
    MODEL = "model"
    RETRIEVAL = "retrieval"
    TEMPERATURE = "temperature"