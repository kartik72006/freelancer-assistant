"""Generate matched keyword-baseline vs semantic-RAG proposal datasets."""

import os
import sys
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from services.ai.gemini_service import GeminiService
from services.ai.knowledge_service import KnowledgeService
from services.ai.prompt_service import PromptService
from services.ai.retrieval_service import RetrievalService as KeywordRetrievalService
from services.retrieval.context_fromatter import ContextFormatter
from services.retrieval.embedding_service import EmbeddingService
from services.retrieval.chroma_vector_store import ChromaVectorStore
from services.retrieval.knowledge_base_indexer import KnowledgeBaseIndexer
from services.retrieval.retrieval_service import RetrievalService as SemanticRetrievalService
from services.retrieval.semantic_retriever import SemanticRetriever
from utils.json_parser import parse_json

BASE_DIR = os.path.dirname(__file__)
JOBS_DIR = os.path.join(BASE_DIR, "jobs")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODES = ("without_rag", "with_rag")
EMPTY_CONTEXT = "No relevant projects found."


def build_semantic_retrieval_service():
    embedding_service = EmbeddingService()
    vector_store = ChromaVectorStore()
    service = SemanticRetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        semantic_retriever=SemanticRetriever(),
        context_formatter=ContextFormatter(),
        knowledge_base_indexer=KnowledgeBaseIndexer(
            embedding_service,
            vector_store,
        ),
    )
    service.initialize()
    return service


def format_keyword_context(retrieval):
    """Format the legacy technology-stack retrieval result for the proposal prompt."""
    projects = retrieval["projects"]
    if not projects:
        return EMPTY_CONTEXT

    blocks = []
    for index, project in enumerate(projects, start=1):
        blocks.append(
            f"Relevant Project {index}\n\n"
            f"Title:\n{project['title']}\n\n"
            f"Project Description:\n{project['description']}\n\n"
            f"Technologies:\n{', '.join(project['tech_stack'])}\n\n"
            f"Keyword Match Score:\n{project['score']}"
        )
    return "\n\n------------------------------------------------------------\n\n".join(blocks)


def generate_proposal(llm, profile, job_description, context, retries=3):
    prompt = PromptService.proposal_prompt(profile, context, job_description)
    for attempt in range(1, retries + 1):
        proposal = parse_json(llm.generate(prompt))
        if proposal is not None:
            return proposal
        print(f"    Invalid proposal response ({attempt}/{retries}); retrying.")
        time.sleep(2**attempt)
    raise RuntimeError("Proposal generation failed after three attempts.")


def save_result(mode, job_file, job_description, proposal, context, error=None):
    output_dir = os.path.join(RESULTS_DIR, mode)
    os.makedirs(output_dir, exist_ok=True)
    number = os.path.splitext(job_file)[0].split("_")[-1]
    output_path = os.path.join(output_dir, f"proposal_{number}.txt")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("=" * 80 + f"\nJOB FILE : {job_file}\nMODE : {mode}\n" + "=" * 80 + "\n\n")
        file.write("ORIGINAL JOB DESCRIPTION\n" + "-" * 80 + "\n" + job_description + "\n\n")
        # Keep the context outside the evaluator's job-description section.
        file.write("ANALYSIS\n" + "=" * 80 + "\n")
        file.write(f"Evaluation mode: {mode}\n\nRETRIEVED CONTEXT\n" + "-" * 80 + "\n")
        file.write(context + "\n\n")
        file.write("PROPOSAL\n" + "=" * 80 + "\n")
        file.write(str(proposal if error is None else {"error": error}) + "\n")


def main():
    job_files = sorted(file for file in os.listdir(JOBS_DIR) if file.endswith(".txt"))
    if not job_files:
        raise RuntimeError(f"No benchmark jobs found in {JOBS_DIR}")

    llm = GeminiService()
    profile = KnowledgeService.load_profile()
    semantic_retrieval = build_semantic_retrieval_service()
    failures = 0
    print(f"Generating matched RAG evaluation dataset for {len(job_files)} jobs.\n")

    for index, job_file in enumerate(job_files, start=1):
        with open(os.path.join(JOBS_DIR, job_file), encoding="utf-8") as file:
            job_description = file.read().strip()
        print(f"[{index}/{len(job_files)}] {job_file}")

        for mode in MODES:
            context = (
                format_keyword_context(KeywordRetrievalService.retrieve_projects(job_description))
                if mode == "without_rag"
                else semantic_retrieval.search(job_description)["context"] or EMPTY_CONTEXT
            )
            try:
                proposal = generate_proposal(llm, profile, job_description, context)
                save_result(mode, job_file, job_description, proposal, context)
                print(f"  {mode}: success")
            except Exception as error:
                failures += 1
                save_result(mode, job_file, job_description, None, context, str(error))
                print(f"  {mode}: failed ({error})")

    total = len(job_files) * len(MODES)
    print(f"\nDataset generation complete: {total - failures}/{total} successful.")


if __name__ == "__main__":
    main()
