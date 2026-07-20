# Semantic Retrieval System

## Overview

The AI Freelancer Proposal Assistant uses a semantic retrieval system to identify the most relevant projects from the knowledge base based on the meaning of a user's query rather than simple keyword matching.

Unlike traditional keyword search, semantic retrieval converts both the user query and project descriptions into dense vector embeddings. Similarity between these vectors is then computed using cosine similarity to retrieve contextually relevant projects.

This enables the proposal generator to reference previous work that closely matches the client's requirements, resulting in more personalized and higher-quality proposals.

---

# System Architecture

```
                    User Query
                         │
                         ▼
              Embedding Generation
                         │
                         ▼
                 Semantic Retriever
                         │
        ┌────────────────────────────────┐
        │ Cosine Similarity Calculation  │
        │ Candidate Selection            │
        │ Score Filtering                │
        │ Duplicate Removal              │
        │ Retrieval Statistics           │
        └────────────────────────────────┘
                         │
                         ▼
                Context Formatter
                         │
                         ▼
                    Gemini LLM
                         │
                         ▼
                Personalized Proposal
```

---

# Components

## 1. Embedding Service

**Purpose**

Converts text into numerical vector embeddings using the Sentence Transformers model.

### Responsibilities

- Load embedding model
- Generate embeddings
- Produce consistent vector representations
- Support both project descriptions and user queries

---

## 2. Vector Store

**Purpose**

Stores project information together with their embeddings.

Each stored document contains:

```python
{
    "project": project_title,
    "embedding": embedding_vector,
    "text": project_description,
    "metadata": {
        "tech_stack": [...]
    }
}
```

### Responsibilities

- Store embedded projects
- Retrieve stored vectors
- Provide documents for similarity search

---

## 3. Semantic Retriever

The semantic retriever is responsible for finding the most relevant projects.

### Retrieval Pipeline

```
Query
   │
   ▼
Generate Query Embedding
   │
   ▼
Cosine Similarity Search
   │
   ▼
Candidate Selection
   │
   ▼
Score Filtering
   │
   ▼
Duplicate Removal
   │
   ▼
Retrieval Statistics
   │
   ▼
Top Results
```

---

### Candidate Retrieval

Instead of immediately returning the Top-K results, the retriever first selects a larger candidate pool.

Example

```
Top 15 Candidates

↓

Filtering

↓

Top 5 Results
```

This improves retrieval quality and provides better flexibility for filtering.

---

### Cosine Similarity

Similarity between the query embedding and project embeddings is calculated using cosine similarity.

Formula

```
Similarity(A,B) =
A · B
────────────
||A|| ||B||
```

Higher similarity indicates greater semantic relevance.

---

### Score Filtering

Projects with similarity below the minimum threshold are discarded.

Benefits

- Removes irrelevant projects
- Improves proposal quality
- Reduces hallucinations

---

### Duplicate Removal

Projects with duplicate titles are removed before returning the final results.

This prevents nearly identical projects from occupying multiple retrieval slots.

---

### Retrieval Statistics

The retriever generates useful statistics for debugging and evaluation.

Example

```python
{
    "total_documents": 6,
    "candidate_results": 6,
    "filtered_results": 2,
    "unique_results": 2,
    "average_similarity": 0.557
}
```

Statistics help evaluate retrieval quality and identify potential improvements.

---

## 4. Context Formatter

The Context Formatter converts retrieved documents into a structured format suitable for Large Language Models.

Example output

```
Project:
AI Freelancer Proposal Assistant

Description:
Designed and developed a full-stack AI-powered proposal generation platform...

Tech Stack:
Python, FastAPI, React, TypeScript

-----------------------------------
```

Structured context improves prompt clarity and helps the LLM generate more accurate proposals.

---

# Knowledge Flow

```
Projects.json
      │
      ▼
Embedding Generation
      │
      ▼
Vector Store
      │
      ▼
User Query
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Projects
      │
      ▼
Context Formatter
      │
      ▼
Gemini Proposal Generator
```

---

# Features Implemented

- Semantic similarity search
- Sentence Transformer embeddings
- Candidate retrieval
- Cosine similarity ranking
- Similarity score filtering
- Duplicate removal
- Metadata support
- Retrieval statistics
- Context formatting
- Modular architecture

---

# Testing

The semantic retrieval system was validated using unit tests.

Tests include:

- Response structure validation
- Statistics validation
- Result validation
- Metadata validation
- Similarity score validation
- Duplicate removal validation
- Retrieval pipeline verification

Run tests using:

```bash
python -m tests.test_semantic_search
```

Successful execution prints:

```
✅ All semantic retrieval tests passed!
```

---

# Advantages

Compared to keyword search, semantic retrieval provides:

- Better understanding of user intent
- Context-aware project matching
- Higher proposal personalization
- Improved retrieval accuracy
- Better utilization of the knowledge base
- Reduced irrelevant results

---

# Current Limitations

- Linear search across all project embeddings
- Small knowledge base
- Basic duplicate detection using project title
- Single embedding model
- No metadata-based filtering

---

# Future Improvements

Planned enhancements include:

- FAISS vector indexing for faster retrieval
- ChromaDB or Pinecone integration
- Metadata-based filtering
- Hybrid Search (BM25 + Semantic Search)
- Cross-Encoder reranking
- Dynamic similarity thresholds
- Multi-source knowledge base
- Incremental embedding updates
- Retrieval evaluation metrics (Precision@K, Recall@K)

---

# Conclusion

The semantic retrieval system enables the AI Freelancer Proposal Assistant to retrieve relevant past projects based on semantic meaning rather than keyword matching. By combining embeddings, cosine similarity, score filtering, duplicate removal, retrieval statistics, and structured context formatting, the system provides high-quality context for proposal generation and forms the foundation of a scalable Retrieval-Augmented Generation (RAG) pipeline.