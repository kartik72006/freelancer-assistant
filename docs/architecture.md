# Freelancer Assistant – System Architecture

# AI-Powered Freelancer Proposal Assistant

Version: 1.0

Author: Kartik Bansal

---

# Table of Contents

1. Project Overview
2. System Goals
3. High-Level Architecture
4. Folder Structure
5. Core Components
6. Request Flow
7. AI Pipeline
8. Design Patterns
9. Configuration Management
10. Knowledge Base
11. Evaluation System
12. Technologies Used
13. Future Improvements

---

# 1. Project Overview

Freelancer Assistant is an AI-powered application that helps freelancers automate one of the most repetitive parts of freelancing—writing high-quality personalized proposals.

The system analyzes a job description, retrieves relevant freelancer information, generates a personalized proposal, estimates pricing and timeline, reviews the generated proposal, evaluates its quality, and produces detailed reports.

Unlike a simple chatbot, this project follows a modular software architecture built around specialized AI agents, reusable services, and an orchestration layer.

---

# 2. System Goals

The primary objectives of the project are:

* Analyze freelancer job descriptions.
* Generate personalized proposals.
* Suggest pricing and timelines.
* Review proposal quality.
* Evaluate AI outputs automatically.
* Generate benchmark reports.
* Maintain a clean, scalable architecture.
* Prepare the project for backend APIs and future frontend integration.

---

# 3. High-Level Architecture

```
                        User
                          │
                          ▼
                     main.py
                          │
                          ▼
               AgentOrchestrator
                          │
     ┌──────────┬──────────┴──────────┬──────────┐
     ▼          ▼                     ▼          ▼
 Analyzer   Proposal Agent      Pricing Agent  Review Agent
    │            │                   │             │
    └────────────┴──────────┬────────┴─────────────┘
                            ▼
                     PromptService
                            │
                            ▼
                 OpenRouter / Gemini Service
                            │
                            ▼
                  Large Language Model
                            │
                            ▼
                   ProposalResult Model
                            │
                            ▼
                     Evaluation Module
                            │
                            ▼
                      Report Generator
```

The application follows a layered architecture where each layer has a single responsibility.

---

# 4. Folder Structure

```
Freelancer-Assistant/

agents/
services/
models/
knowledge_base/
evaluation/
reports/
config/
utils/
docs/
main.py
requirements.txt
README.md
```

---

## agents/

Responsible for AI business logic.

Each agent performs one dedicated task.

Components:

* AnalyzerAgent
* ProposalAgent
* PricingAgent
* ReviewAgent
* EvaluationAgent

Responsibilities:

* Receive processed inputs.
* Build prompts.
* Call AI services.
* Return structured outputs.

---

## services/

Provides reusable application services.

Components:

* PromptService
* OpenRouterService
* GeminiService
* RetrievalService
* KnowledgeService
* AgentOrchestrator

Responsibilities:

* External API communication.
* Prompt construction.
* Knowledge retrieval.
* Pipeline orchestration.
* AI model interaction.

---

## models/

Contains application data models.

Current Models:

* FreelancerProfile
* Job
* Proposal
* Evaluation
* ProposalResult

Responsibilities:

* Represent structured application data.
* Provide consistent interfaces.
* Improve maintainability.
* Prepare for FastAPI request/response models.

---

## knowledge_base/

Stores reusable freelancer information.

Files include:

* profile.json
* skills.json
* projects.json
* past_proposals.json

Purpose:

Provide contextual information to the language model for better personalization.

---

## evaluation/

Responsible for AI benchmarking.

Tasks include:

* Dataset generation.
* Proposal evaluation.
* Score calculation.
* Benchmark execution.

---

## reports/

Generates analytics reports.

Modules include:

* statistics.py
* visualization.py
* recommendations.py
* markdown_writer.py
* feedback_analyzer.py
* report_generator.py

Outputs:

* Markdown reports.
* CSV score files.
* Evaluation summaries.
* Engineering recommendations.

---

## config/

Stores centralized application configuration.

Includes:

* API Keys
* Base URLs
* Retry configuration
* Model configuration
* Application constants

Purpose:

Avoid duplicated configuration across services.

---

## utils/

Reusable helper functions.

Examples:

* JSON parsing.
* Display formatting.
* Result parsing.
* Shared helper utilities.

---

# 5. Core Components

## AgentOrchestrator

Acts as the controller of the application.

Responsibilities:

* Coordinate execution order.
* Call each agent.
* Aggregate outputs.
* Return the final response.

It does not generate AI content itself.

---

## Analyzer Agent

Input:

Job Description

Output:

Structured job analysis including:

* Required skills
* Complexity
* Project summary

---

## Proposal Agent

Input:

* Job description
* Freelancer profile
* Relevant projects

Output:

Personalized proposal.

---

## Pricing Agent

Input:

* Job description
* Complexity

Output:

Estimated:

* Budget
* Timeline

---

## Review Agent

Input:

Generated proposal.

Output:

Quality assessment including:

* Professionalism
* Personalization
* Tone
* Clarity
* Overall feedback

---

## Evaluation Agent

Evaluates generated proposals using another LLM.

Measures:

* Relevance
* Accuracy
* Personalization
* Tone
* Completeness
* Hallucination

Produces benchmark scores.

---

# 6. Complete Request Flow

```
User

↓

Paste Job Description

↓

Analyzer Agent

↓

Retrieve Knowledge

↓

Proposal Agent

↓

Pricing Agent

↓

Review Agent

↓

ProposalResult

↓

Evaluation Agent

↓

Report Generator

↓

Final Output
```

---

# 7. AI Pipeline

```
Knowledge Base

↓

Retrieval Service

↓

Prompt Service

↓

OpenRouter / Gemini

↓

LLM

↓

Generated Proposal

↓

Review Agent

↓

Evaluation Agent

↓

Analytics Reports
```

---

# 8. Design Patterns Used

## Service Layer

Purpose:

Separate reusable services from business logic.

Examples:

* PromptService
* RetrievalService
* OpenRouterService

---

## Agent Pattern

Each AI capability is implemented as an independent agent.

Advantages:

* Modular
* Easy to extend
* Easy to test

---

## Dependency Injection

Dependencies are created in main.py and injected into the AgentOrchestrator.

Advantages:

* Loose coupling
* Easier testing
* Better maintainability

---

## Orchestrator Pattern

The AgentOrchestrator controls the execution order of all agents.

Advantages:

* Centralized workflow.
* Cleaner business logic.
* Better scalability.

---

## Single Responsibility Principle

Each module performs exactly one task.

Examples:

PromptService:

Only builds prompts.

OpenRouterService:

Only communicates with OpenRouter.

ReportGenerator:

Only creates reports.

---

# 9. Configuration Management

Configuration is centralized in:

```
config/settings.py
```

Contains:

* API keys
* Base URLs
* Retry limits
* Default AI settings

Benefits:

* Single source of truth.
* Easier maintenance.
* Safer credential handling.

---

# 10. Knowledge Base

The project currently uses JSON files as a lightweight knowledge base.

```
profile.json

skills.json

projects.json

past_proposals.json
```

Purpose:

Provide freelancer-specific context during proposal generation.

Future versions will replace this with:

* Embeddings
* Vector database
* Semantic retrieval (RAG)

---

# 11. Evaluation System

The project includes a complete evaluation pipeline.

Workflow:

```
Generate Proposal

↓

Store Result

↓

LLM-as-a-Judge

↓

Generate Scores

↓

Create Statistics

↓

Produce Markdown Report

↓

Engineering Recommendations
```

Evaluation Criteria:

* Relevance
* Personalization
* Accuracy
* Completeness
* Tone
* Hallucination

---

# 12. Technologies Used

| Category      | Technology          |
| ------------- | ------------------- |
| Language      | Python              |
| AI Models     | OpenRouter, Gemini  |
| Architecture  | Multi-Agent         |
| Prompting     | Prompt Engineering  |
| Knowledge     | JSON Knowledge Base |
| Evaluation    | LLM-as-a-Judge      |
| Reports       | Markdown + CSV      |
| Configuration | python-dotenv       |
| IDE           | VS Code             |

---

# 13. Future Improvements

Planned enhancements include:

## Backend

* FastAPI
* REST APIs
* Input validation
* Response models

## Database

* SQLite
* PostgreSQL

## Frontend

* React
* Tailwind CSS

## AI

* Embeddings
* Vector Database
* Semantic Search
* Full RAG Pipeline

## Analytics

* Dashboard
* User Metrics
* Proposal History
* Acceptance Tracking

## DevOps

* Docker
* CI/CD
* Cloud Deployment
* Automated Testing

---

# Conclusion

The Freelancer Assistant has evolved from a simple proposal generation script into a modular AI application with dedicated agents, reusable services, centralized configuration, automated evaluation, benchmarking, and reporting.

The current architecture emphasizes modularity, maintainability, and scalability while providing a strong foundation for future enhancements such as FastAPI APIs, database integration, retrieval-augmented generation (RAG), and a web-based frontend.
