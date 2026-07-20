"""Score both matched RAG datasets with the existing EvaluationAgent."""

import csv
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from agents.evaluation_agent import EvaluationAgent
from services.ai.gemini_service import GeminiService
from utils.result_parser import ResultParser

BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODES = ("without_rag", "with_rag")
FIELDS = ["job_id", "relevance", "accuracy", "personalization", "completeness", "tone", "hallucination", "overall", "relevance_feedback", "accuracy_feedback", "personalization_feedback", "completeness_feedback", "tone_feedback", "hallucination_feedback"]


def evaluate_mode(evaluator, mode):
    result_dir = os.path.join(RESULTS_DIR, mode)
    csv_path = os.path.join(BASE_DIR, f"scores_{mode}.csv")
    proposal_files = sorted(file for file in os.listdir(result_dir) if file.endswith(".txt"))

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        for proposal_file in proposal_files:
            parsed = ResultParser.parse(os.path.join(result_dir, proposal_file))
            if not parsed["proposal"] or "'error':" in parsed["proposal"]:
                print(f"Skipping failed generation: {mode}/{proposal_file}")
                continue
            print(f"Evaluating {mode}/{proposal_file}")
            result = evaluator.evaluate(parsed["job_description"], parsed["proposal"])
            if not result.get("success", True):
                print(f"Evaluation failed: {mode}/{proposal_file}")
                continue
            row = {"job_id": proposal_file, **{field: result[field] for field in FIELDS if field in result}}
            row.update({f"{metric}_feedback": result["feedback"][metric] for metric in ("relevance", "accuracy", "personalization", "completeness", "tone", "hallucination")})
            writer.writerow(row)
    return csv_path


def evaluate_single_dataset(evaluator):
    """Compatibility path for the original generate_dataset.py output."""
    result_dir = RESULTS_DIR
    csv_path = os.path.join(BASE_DIR, "scores.csv")
    proposal_files = sorted(file for file in os.listdir(result_dir) if file.endswith(".txt"))

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        for proposal_file in proposal_files:
            parsed = ResultParser.parse(os.path.join(result_dir, proposal_file))
            if not parsed["proposal"] or "EXECUTION FAILED" in parsed["proposal"]:
                print(f"Skipping failed generation: {proposal_file}")
                continue
            print(f"Evaluating {proposal_file}")
            result = evaluator.evaluate(parsed["job_description"], parsed["proposal"])
            if not result.get("success", True):
                print(f"Evaluation failed: {proposal_file}")
                continue
            row = {"job_id": proposal_file, **{field: result[field] for field in FIELDS if field in result}}
            row.update({f"{metric}_feedback": result["feedback"][metric] for metric in ("relevance", "accuracy", "personalization", "completeness", "tone", "hallucination")})
            writer.writerow(row)
    return csv_path


def main():
    evaluator = EvaluationAgent(GeminiService())
    if not all(os.path.isdir(os.path.join(RESULTS_DIR, mode)) for mode in MODES):
        print(f"Saved scores to: {evaluate_single_dataset(evaluator)}")
        return
    for mode in MODES:
        result_dir = os.path.join(RESULTS_DIR, mode)
        if not os.path.isdir(result_dir):
            raise RuntimeError(f"Missing {result_dir}. Run generate_dataset.py first.")
        print(f"Saved scores to: {evaluate_mode(evaluator, mode)}")


if __name__ == "__main__":
    main()
