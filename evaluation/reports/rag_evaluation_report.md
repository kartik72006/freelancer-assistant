# RAG Evaluation Report

## Executive Summary

- Matched benchmark jobs: **20**
- Average overall score without RAG: **51.65/60**
- Average overall score with RAG: **52.05/60**
- Average improvement: **+0.40/60**

## Outcome Distribution

| Metric | Value |
|---|---:|
| Jobs Improved | 11 |
| Jobs Declined | 7 |
| No Change | 2 |
| Mean Improvement | +0.40/60 |
| Median Improvement | +1.00/60 |
| Best Improvement | +6.00/60 |
| Worst Decline | -8.00/60 |

## Metric Comparison

| Metric | Without RAG | With RAG | Change |
|---|---:|---:|---:|
| Relevance | 8.70 | 8.65 | -0.05 |
| Accuracy | 8.65 | 8.75 | +0.10 |
| Personalization | 6.60 | 6.85 | +0.25 |
| Completeness | 9.05 | 9.00 | -0.05 |
| Tone | 8.75 | 8.80 | +0.05 |
| Hallucination | 9.90 | 10.00 | +0.10 |
| Overall | 51.65 | 52.05 | +0.40 |

## Jobs with the Largest Improvement

- **proposal_03.txt**: +6.00/60
- **proposal_05.txt**: +6.00/60
- **proposal_10.txt**: +3.00/60

## Jobs with the Smallest Improvement

- **proposal_06.txt**: -8.00/60
- **proposal_19.txt**: -6.00/60
- **proposal_20.txt**: -4.00/60

## Interpretation

This is a matched offline experiment: each job is generated once with the same model, profile, and prompt. The baseline ranks project technology stacks through legacy keyword matching; the RAG arm ranks the same portfolio records through semantic retrieval. Positive changes indicate that semantic RAG helped under this sample; negative changes identify jobs where it did not add value. Because generation and LLM judging are stochastic, rerun the benchmark (ideally multiple times per job) before treating small score differences as conclusive.
