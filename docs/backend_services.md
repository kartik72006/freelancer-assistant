# Backend Services Architecture

**Project:** AI Freelancer Proposal Assistant

**Version:** 1.0

**Phase:** Week 4 – Backend Engineering

**Created:** Day 24

---

# 1. Overview

The Backend Service Layer is responsible for orchestrating the entire AI proposal generation workflow while maintaining a clean separation between the API layer and the business logic.

Prior to Day 24, the FastAPI routes directly interacted with the `AgentOrchestrator`. Although functional, this tightly coupled the API layer with the business workflow.

Day 24 introduces an **Application Service Layer**, resulting in a cleaner, more maintainable, and scalable architecture.

The application now follows a layered architecture where every component has a single responsibility.

---

# 2. Architecture

```
                Client
                   │
                   ▼
              FastAPI Routes
                   │
                   ▼
        Application Service Layer
                   │
                   ▼
          Agent Orchestrator
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Analyzer    Proposal    Pricing
      │            │           │
      └────────────┼───────────┘
                   ▼
             Review Agent
                   │
                   ▼
          AI Infrastructure Layer
                   │
                   ▼
        Gemini / Prompt / Retrieval
                   │
                   ▼
        Repository & Knowledge Base
                   │
                   ▼
                SQLite
```

---

# 3. Layer Responsibilities

---

## API Layer

Location

```
api/routes/
```

Responsibilities

- Receive HTTP requests
- Validate request bodies
- Call application services
- Return response models
- Handle HTTP exceptions

The API layer contains **no business logic**.

Example

```
POST /proposal/generate

↓

ProposalService.generate_proposal()

↓

Return ProposalResponse
```

---

## Application Service Layer

Location

```
services/application/
```

Contains

```
analysis_service.py

proposal_service.py

pricing_service.py

review_service.py
```

Responsibilities

- Represent application use cases
- Coordinate business workflows
- Delegate processing to the Agent Orchestrator
- Hide orchestration details from the API layer

The API communicates only with application services.

---

## Agent Orchestrator

Location

```
services/ai/orchestrator_service.py
```

Responsibilities

- Coordinate AI agents
- Execute workflows
- Reuse intermediate outputs
- Return domain objects

Instead of one large workflow, the orchestrator now exposes dedicated methods.

```
analyze()

generate_proposal()

generate_pricing()

review_proposal()

run()
```

Each method builds upon the previous one.

---

## AI Agent Layer

Location

```
agents/
```

Contains

```
AnalyzerAgent

ProposalAgent

PricingAgent

ReviewAgent
```

Responsibilities

### AnalyzerAgent

- Detect skills
- Estimate complexity
- Estimate budget
- Estimate timeline
- Detect category
- Retrieve relevant projects

Output

```
Analysis
```

---

### ProposalAgent

Responsibilities

- Build proposal prompt
- Retrieve user profile
- Retrieve project context
- Generate proposal using Gemini

Output

```
Proposal
```

---

### PricingAgent

Responsibilities

- Estimate pricing
- Estimate delivery timeline
- Justify pricing

Output

```
Pricing Information
```

---

### ReviewAgent

Responsibilities

- Evaluate generated proposal
- Score proposal quality
- Generate improvement suggestions

Output

```
Proposal Review
```

---

## AI Infrastructure Layer

Location

```
services/ai/
```

Contains

```
GeminiService

PromptService

KnowledgeService

RetrievalService
```

Responsibilities

### GeminiService

- Connect to Gemini API
- Handle prompt execution
- Return LLM responses

---

### PromptService

- Generate prompts
- Centralize prompt templates

---

### KnowledgeService

- Load JSON knowledge base
- User profile
- Skills
- Projects

---

### RetrievalService

- Retrieve relevant projects
- Match technologies
- Score project similarity

---

# 4. Dependency Management

Dependency initialization has been centralized.

Location

```
api/dependencies.py
```

Responsibilities

- Create singleton instances
- Initialize Gemini service
- Initialize agents
- Initialize orchestrator
- Initialize application services

Current dependency graph

```
GeminiService

↓

ProposalAgent
PricingAgent
ReviewAgent

↓

AnalyzerAgent

↓

AgentOrchestrator

↓

Application Services

↓

Routes
```

Benefits

- Single initialization point
- Easy dependency replacement
- Reduced duplication
- Cleaner routes

---

# 5. Request Lifecycle

## Analysis

```
Client

↓

POST /analysis/analyze

↓

Analysis Route

↓

Analysis Service

↓

Agent Orchestrator

↓

Analyzer Agent

↓

Knowledge Service

↓

Retrieval Service

↓

Analysis Result

↓

JSON Response
```

---

## Proposal

```
Client

↓

POST /proposal/generate

↓

Proposal Route

↓

Proposal Service

↓

Agent Orchestrator

↓

Analyzer Agent

↓

Proposal Agent

↓

Gemini

↓

Proposal Result

↓

JSON Response
```

---

## Pricing

```
Client

↓

POST /pricing/generate

↓

Pricing Route

↓

Pricing Service

↓

Agent Orchestrator

↓

Analyzer Agent

↓

Proposal Agent

↓

Pricing Agent

↓

Gemini

↓

Pricing Result

↓

JSON Response
```

---

## Review

```
Client

↓

POST /review/generate

↓

Review Route

↓

Review Service

↓

Agent Orchestrator

↓

Analyzer Agent

↓

Proposal Agent

↓

Pricing Agent

↓

Review Agent

↓

Gemini

↓

Review Result

↓

JSON Response
```

---

# 6. API Endpoints

| Method | Endpoint | Description |
|----------|----------------------|--------------------------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/analysis/analyze` | Analyze job description |
| POST | `/proposal/generate` | Generate proposal |
| POST | `/pricing/generate` | Generate pricing |
| POST | `/review/generate` | Review proposal |

---

# 7. Request Models

Location

```
api/schemas/requests/
```

Contains

```
analysis.py

proposal.py

pricing.py

review.py
```

Each endpoint has its own request model.

Example

```python
class ProposalRequest(BaseModel):
    job_description: str
```

---

# 8. Response Models

Location

```
api/schemas/proposal_responses/
```

Contains

```
analysis.py

proposal.py

pricing.py

review.py
```

Each endpoint returns a dedicated response model.

Benefits

- Strong validation
- Better Swagger documentation
- Clear API contracts
- Type safety

---

# 9. Domain Model

Location

```
models/proposal_result.py
```

Purpose

The `ProposalResult` object represents the internal business result of the AI workflow.

Unlike API response models, it is not exposed directly to clients.

Responsibilities

- Store intermediate results
- Pass data between services
- Maintain workflow state

Fields

```
analysis

proposal

pricing

review
```

---

# 10. Design Principles

The backend follows several software engineering principles.

### Separation of Concerns

Each layer performs exactly one responsibility.

---

### Single Responsibility Principle

Each service is responsible for one application use case.

---

### Thin Controllers

Routes contain no business logic.

---

### Layered Architecture

Communication flows only downward.

```
Routes

↓

Services

↓

Orchestrator

↓

Agents

↓

Infrastructure

↓

Repositories
```

---

### Dependency Injection

All major components are initialized centrally and injected into dependent layers.

---

### Reusability

Services and orchestrator methods can be reused across future APIs, scheduled jobs, CLI tools, or background workers.

---

# 11. Benefits of the Day 24 Refactor

Before

```
Route

↓

AgentOrchestrator

↓

Agents
```

Problems

- Tight coupling
- Hard to extend
- Business logic exposed to API layer
- Difficult testing

---

After

```
Route

↓

Application Service

↓

Agent Orchestrator

↓

Agents

↓

Infrastructure
```

Advantages

- Cleaner architecture
- Better maintainability
- Easier testing
- Better scalability
- Reusable services
- Production-style backend design

---

# 12. Future Improvements

Planned enhancements

- Native FastAPI Dependency Injection (`Depends`)
- Authentication (JWT)
- User Management
- Background Task Queue
- Caching Layer
- Logging Middleware
- Rate Limiting
- Docker Deployment
- CI/CD Pipeline
- Cloud Deployment
- Monitoring & Observability

---

# 13. Conclusion

The Day 24 backend refactor transforms the AI Freelancer Proposal Assistant from a functional API into a layered backend application with production-inspired architecture.

By introducing an application service layer, centralized dependency management, dedicated request/response models, and an orchestrator-driven workflow, the backend is now modular, extensible, and ready for future enhancements such as authentication, deployment, frontend integration, and retrieval-augmented generation (RAG).

This architecture emphasizes maintainability, scalability, and clean separation of concerns while providing a solid foundation for enterprise-grade backend development.