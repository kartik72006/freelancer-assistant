"""Create a quantitative RAG-vs-baseline Markdown report."""

import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
METRICS = ("relevance", "accuracy", "personalization", "completeness", "tone", "hallucination", "overall")


def score(value):
    return f"{value:+.2f}" if value else "0.00"


def main():
    baseline = pd.read_csv(os.path.join(BASE_DIR, "scores_without_rag.csv"))
    rag = pd.read_csv(os.path.join(BASE_DIR, "scores_with_rag.csv"))
    baseline = baseline.set_index("job_id")
    rag = rag.set_index("job_id")
    common_jobs = baseline.index.intersection(rag.index)
    if common_jobs.empty:
        raise RuntimeError("No matched jobs were scored in both datasets.")

    baseline, rag = baseline.loc[common_jobs], rag.loc[common_jobs]
    deltas = rag[list(METRICS)] - baseline[list(METRICS)]
    metric_rows = []
    for metric in METRICS:
        metric_rows.append(f"| {metric.title()} | {baseline[metric].mean():.2f} | {rag[metric].mean():.2f} | {score(deltas[metric].mean())} |")

    per_job = deltas["overall"].sort_values(ascending=False)
    biggest = per_job.head(3)
    smallest = per_job.tail(3).sort_values()
    improved = int((per_job > 0).sum())
    declined = int((per_job < 0).sum())
    unchanged = int((per_job == 0).sum())
    mean_change = per_job.mean()
    median_change = per_job.median()
    best_change = per_job.max()
    worst_change = per_job.min()
    report = f"""# RAG Evaluation Report

## Executive Summary

- Matched benchmark jobs: **{len(common_jobs)}**
- Average overall score without RAG: **{baseline['overall'].mean():.2f}/60**
- Average overall score with RAG: **{rag['overall'].mean():.2f}/60**
- Average improvement: **{score(deltas['overall'].mean())}/60**

## Outcome Distribution

| Metric | Value |
|---|---:|
| Jobs Improved | {improved} |
| Jobs Declined | {declined} |
| No Change | {unchanged} |
| Mean Improvement | {score(mean_change)}/60 |
| Median Improvement | {score(median_change)}/60 |
| Best Improvement | {score(best_change)}/60 |
| Worst Decline | {score(worst_change)}/60 |

## Metric Comparison

| Metric | Without RAG | With RAG | Change |
|---|---:|---:|---:|
{chr(10).join(metric_rows)}

## Jobs with the Largest Improvement

{chr(10).join(f'- **{job}**: {score(change)}/60' for job, change in biggest.items())}

## Jobs with the Smallest Improvement

{chr(10).join(f'- **{job}**: {score(change)}/60' for job, change in smallest.items())}

## Interpretation

This is a matched offline experiment: each job is generated once with the same model, profile, and prompt. The baseline ranks project technology stacks through legacy keyword matching; the RAG arm ranks the same portfolio records through semantic retrieval. Positive changes indicate that semantic RAG helped under this sample; negative changes identify jobs where it did not add value. Because generation and LLM judging are stochastic, rerun the benchmark (ideally multiple times per job) before treating small score differences as conclusive.
"""
    path = os.path.join(BASE_DIR, "rag_evaluation_report.md")
    with open(path, "w", encoding="utf-8") as file:
        file.write(report)
    print(f"RAG evaluation report written to: {path}")


if __name__ == "__main__":
    main()
