# Production RAG Architecture

## AI Freelancer Proposal Assistant

**Version:** Week 6 -- Production RAG (Day 35)

**Author:** Kartik Bansal

------------------------------------------------------------------------

# Table of Contents

1.  Overview
2.  Why RAG?
3.  High-Level Architecture
4.  Retrieval Pipeline
5.  Component Responsibilities
6.  Knowledge Base
7.  Why ChromaDB?
8.  Retrieval Configuration
9.  Retrieval Diagnostics
10. Evaluation Framework
11. Benchmark Results
12. Design Decisions
13. Current Limitations
14. Future Improvements
15. Interview Talking Points
16. Conclusion

------------------------------------------------------------------------

# Overview

The AI Freelancer Proposal Assistant uses a **Retrieval-Augmented
Generation (RAG)** pipeline to generate personalized freelance
proposals.

Instead of relying solely on the LLM and a static freelancer profile,
the system retrieves semantically relevant projects from a persistent
knowledge base and injects them into the prompt before proposal
generation.

This improves:

-   Personalization
-   Technical relevance
-   Context awareness
-   Proposal quality
-   Trustworthiness

------------------------------------------------------------------------

# Why RAG?

The original proposal generation pipeline relied on:

-   Freelancer profile
-   Job description

Limitations included:

-   Generic proposals
-   Weak project references
-   Limited personalization
-   Greater hallucination risk

RAG solves these by retrieving the most relevant previous work before
the LLM generates the proposal.

------------------------------------------------------------------------

# High-Level Architecture

``` text
                      User
                        │
                        ▼
             Job Description Input
                        │
                        ▼
                Proposal Agent
                        │
                        ▼
               Retrieval Service
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
Embedding Service   ChromaDB       Semantic Retriever
        │               │                │
        └───────────────┼────────────────┘
                        ▼
               Context Formatter
                        │
                        ▼
             Prompt Construction
                        │
                        ▼
               Gemini / OpenRouter
                        │
                        ▼
              Personalized Proposal
```

------------------------------------------------------------------------

# Retrieval Pipeline

1.  **Job Description** received from the user.
2.  **EmbeddingService** converts the text into a semantic embedding
    using `all-MiniLM-L6-v2`.
3.  **ChromaDB** retrieves the most similar projects.
4.  **SemanticRetriever** ranks, filters and removes duplicates.
5.  **ContextFormatter** prepares clean prompt context.
6.  **ProposalAgent** combines:
    -   Freelancer Profile
    -   Retrieved Context
    -   Job Description
7.  **LLM** generates:
    -   Introduction
    -   Relevant Experience
    -   Technical Approach
    -   Timeline
    -   Pricing

------------------------------------------------------------------------

# Component Responsibilities

## EmbeddingService

Responsible for:

-   Loading the embedding model
-   Single embedding generation
-   Batch embedding generation

Does **not**:

-   Search vectors
-   Format prompts
-   Read JSON

------------------------------------------------------------------------

## ChromaVectorStore

Responsible for:

-   Persistent vector storage
-   Metadata storage
-   Similarity search
-   Collection management

Does **not**:

-   Generate embeddings
-   Rank results
-   Format context

------------------------------------------------------------------------

## SemanticRetriever

Responsible for:

-   Similarity search
-   Ranking
-   Score filtering
-   Duplicate removal
-   Retrieval diagnostics
-   Retrieval statistics

Does **not**:

-   Generate prompts
-   Generate embeddings
-   Load project files

------------------------------------------------------------------------

## ContextFormatter

Responsible only for transforming retrieval results into prompt-ready
context.

------------------------------------------------------------------------

## RetrievalService

Acts as the orchestrator:

``` text
Job Description
        │
        ▼
EmbeddingService
        │
        ▼
SemanticRetriever
        │
        ▼
ContextFormatter
        │
        ▼
ProposalAgent
```

------------------------------------------------------------------------

# Knowledge Base

Each indexed project contains:

-   Title
-   Role
-   Domain
-   Project Type
-   Problem
-   Description
-   Responsibilities
-   Technical Solution
-   Architecture
-   Key Features
-   Technologies
-   Business Impact
-   Results
-   Skills

This rich representation improves semantic retrieval quality.

------------------------------------------------------------------------

# Why ChromaDB?

The project initially used an in-memory vector store.

ChromaDB provides:

-   Persistent storage
-   Fast cosine similarity search
-   Metadata support
-   Scalable architecture
-   Faster startup

------------------------------------------------------------------------

# Retrieval Configuration

All retrieval parameters are centralized in:

``` text
config/settings.py
```

Current settings include:

-   Embedding Model
-   Chroma Database Path
-   Collection Name
-   Top-K Retrieval
-   Candidate Retrieval Size
-   Similarity Threshold
-   Retrieval Logging

This allows experimentation without changing retrieval logic.

------------------------------------------------------------------------

# Retrieval Diagnostics

Every retrieval logs:

-   Query
-   Retrieved projects
-   Similarity scores
-   Candidate count
-   Filtered results
-   Average similarity
-   Retrieval latency

Example:

``` text
RETRIEVAL DIAGNOSTICS

Backend Python Developer

1. AI Freelancer Proposal Assistant
Score: 0.53

Latency: 4.26 ms
```

------------------------------------------------------------------------

# Evaluation Framework

The system compares:

``` text
Without RAG

↓

Evaluation
```

against

``` text
With RAG

↓

Evaluation
```

Metrics:

-   Personalization
-   Relevance
-   Technical Accuracy
-   Completeness
-   Tone
-   Hallucination

------------------------------------------------------------------------

# Benchmark Results

Latest benchmark:

  Metric                Result
  --------------------- ------------
  Jobs Evaluated        20
  Average Improvement   +1.55 / 60
  Jobs Improved         11
  Jobs Declined         5
  No Change             4

------------------------------------------------------------------------

# Design Decisions

-   Sentence Transformers for semantic embeddings
-   ChromaDB for persistence
-   Cosine similarity for retrieval
-   Metadata for future filtering
-   RetrievalService to isolate retrieval logic
-   ContextFormatter to improve prompt readability

------------------------------------------------------------------------

# Current Limitations

-   Single embedding model
-   Fixed similarity threshold
-   Fixed Top-K
-   No hybrid retrieval
-   No reranker
-   No retrieval caching
-   No query rewriting

These were intentionally deferred to keep the implementation focused and
educational.

------------------------------------------------------------------------

# Future Improvements

-   Hybrid retrieval
-   Cross-encoder reranking
-   Dynamic Top-K
-   Query expansion
-   Metadata filtering
-   Retrieval cache
-   Multiple embedding models
-   Observability dashboard
-   Token usage analytics

------------------------------------------------------------------------

# Interview Talking Points

This implementation demonstrates:

-   Multi-agent AI architecture
-   Production-style RAG
-   SentenceTransformer embeddings
-   ChromaDB persistence
-   Modular service-oriented architecture
-   Prompt engineering with contextual augmentation
-   Benchmark-driven optimization
-   Controlled RAG evaluation
-   Clean separation of concerns

------------------------------------------------------------------------

# Conclusion

The AI Freelancer Proposal Assistant now uses a production-inspired
Retrieval-Augmented Generation pipeline with persistent vector storage,
semantic search, structured context construction, and quantitative
evaluation.

The architecture is modular, maintainable, and ready for future
enhancements such as hybrid retrieval, reranking, metadata filtering,
and production deployment.
