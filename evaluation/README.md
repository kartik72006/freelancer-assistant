# Day 32: RAG Evaluation

This folder contains a matched offline benchmark: every job is generated twice
with the same profile, model, and proposal prompt. The only intended variable is
the retrieval strategy: the legacy technology-stack keyword retriever
(`without_rag`) versus the current semantic retriever (`with_rag`). The legacy
retriever maps the current `technologies` field to its original `tech_stack`
baseline field and does not use embeddings.

Run from the project root:

```powershell
python evaluation/generate_dataset.py
python evaluation/evaluate.py
python evaluation/generate_rag_report.py
```

Generated artifacts:

- `results/without_rag/` and `results/with_rag/`
- `scores_without_rag.csv` and `scores_with_rag.csv`
- `rag_evaluation_report.md`

The report compares only jobs successfully scored in both arms. Treat small
differences cautiously: model generation and LLM-as-a-judge scoring are stochastic.
