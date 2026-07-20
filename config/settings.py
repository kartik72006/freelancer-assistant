import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# API KEYS
# ===========================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ===========================
# BASE URLS
# ===========================

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ===========================
# DEFAULT AI SETTINGS
# ===========================

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1200
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# ===========================
# APP INFO
# ===========================

APP_NAME = "Freelancer Assistant"
VERSION = "1.0"


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"

SKILLS_FILE = KNOWLEDGE_BASE_DIR / "skills.json"

PROFILE_FILE = KNOWLEDGE_BASE_DIR / "profile.json"

PROJECTS_FILE = KNOWLEDGE_BASE_DIR / "projects.json"

# ===========================
# RAG SETTINGS
# ===========================

CHROMA_DB_PATH = "./data/chroma_db"

CHROMA_COLLECTION_NAME = "projects"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 3

MIN_SIMILARITY_SCORE = 0.35

CANDIDATE_K = 15

ENABLE_RETRIEVAL_LOGGING = True