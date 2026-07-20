# Database Design Document

## Project

**AI Freelancer Proposal Assistant**

**Version:** 1.0
**Phase:** Week 4 – Day 22
**Author:** Kartik Bansal

---

# 1. Purpose

This document defines the database architecture for the AI Freelancer Proposal Assistant. It explains the reasoning behind the database design, the chosen technologies, entity relationships, and how the persistence layer integrates with the rest of the application.

The database is responsible for storing all dynamic application data generated during proposal creation and evaluation while keeping the AI knowledge base independent.

---

# 2. Objectives

The database layer has been designed to achieve the following objectives:

* Persist freelancer information
* Store job descriptions
* Store generated proposals
* Store AI evaluation results
* Maintain proposal history
* Support future analytics
* Enable future authentication
* Prepare for PostgreSQL migration

---

# 3. Technology Stack

| Component            | Technology         |
| -------------------- | ------------------ |
| Database             | SQLite             |
| ORM                  | SQLAlchemy         |
| Design Pattern       | Repository Pattern |
| Programming Language | Python             |

---

# 4. Why SQLite?

SQLite was selected for the initial version because it provides several advantages during early-stage development.

### Advantages

* Zero configuration
* Lightweight
* File-based database
* No separate database server required
* Cross-platform
* Excellent SQLAlchemy support
* Perfect for local development

SQLite allows rapid development while maintaining compatibility with larger relational databases.

---

# 5. Why SQLAlchemy?

Instead of writing raw SQL queries, SQLAlchemy was selected as the Object Relational Mapper (ORM).

### Benefits

* Object-oriented database interaction
* Cleaner code
* Better maintainability
* Database abstraction
* Automatic relationship handling
* Easy migration to PostgreSQL

Example:

Instead of writing SQL such as:

```sql
SELECT * FROM users;
```

The application simply performs:

```python
user_repository.get_all(db)
```

---

# 6. Why Repository Pattern?

Direct database queries scattered throughout the application quickly become difficult to maintain.

The Repository Pattern isolates persistence logic from business logic.

## Architecture

```text
Application

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy ORM

↓

SQLite
```

### Advantages

* Separation of concerns
* Easier testing
* Better scalability
* Reusable CRUD operations
* Cleaner service layer
* Database independence

---

# 7. Database Schema

The system consists of four primary entities.

## Users

Stores freelancer profile information.

### Fields

| Column     | Type     | Description         |
| ---------- | -------- | ------------------- |
| id         | Integer  | Primary Key         |
| name       | String   | Freelancer Name     |
| email      | String   | Unique Email        |
| title      | String   | Professional Title  |
| bio        | Text     | User Bio            |
| experience | Integer  | Years of Experience |
| created_at | DateTime | Creation Timestamp  |

---

## Jobs

Stores job descriptions submitted by users.

### Fields

| Column      | Type     | Description                     |
| ----------- | -------- | ------------------------------- |
| id          | Integer  | Primary Key                     |
| user_id     | Integer  | Foreign Key → Users             |
| title       | String   | Job Title                       |
| description | Text     | Job Description                 |
| client_name | String   | Client Name                     |
| budget      | String   | Expected Budget                 |
| deadline    | String   | Project Deadline                |
| source      | String   | Platform (Upwork, Fiverr, etc.) |
| created_at  | DateTime | Creation Timestamp              |

---

## Proposals

Stores AI-generated proposals.

### Fields

| Column         | Type     | Description         |
| -------------- | -------- | ------------------- |
| id             | Integer  | Primary Key         |
| job_id         | Integer  | Foreign Key → Jobs  |
| user_id        | Integer  | Foreign Key → Users |
| proposal       | Text     | Generated Proposal  |
| pricing        | Text     | Suggested Pricing   |
| timeline       | String   | Estimated Timeline  |
| review         | Text     | AI Review           |
| model          | String   | LLM Used            |
| prompt_version | String   | Prompt Version      |
| created_at     | DateTime | Creation Timestamp  |

---

## Evaluations

Stores proposal evaluation metrics.

### Fields

| Column             | Type     | Description            |
| ------------------ | -------- | ---------------------- |
| id                 | Integer  | Primary Key            |
| proposal_id        | Integer  | Foreign Key → Proposal |
| relevance          | Float    | Relevance Score        |
| accuracy           | Float    | Accuracy Score         |
| personalization    | Float    | Personalization Score  |
| completeness       | Float    | Completeness Score     |
| tone               | Float    | Tone Score             |
| hallucination      | Float    | Hallucination Score    |
| overall_score      | Float    | Final Score            |
| evaluator_feedback | Text     | AI Feedback            |
| created_at         | DateTime | Creation Timestamp     |

---

# 8. Entity Relationships

The relationships between entities are illustrated below.

```text
                    USERS
                       │
                       │ 1
                       │
                       ▼
                    JOBS
                       │
                       │ 1
                       │
                       ▼
                 PROPOSALS
                       │
                       │ 1
                       │
                       ▼
                EVALUATIONS
```

## Relationship Explanation

### User → Jobs

One freelancer can submit multiple job descriptions.

Relationship:

```
One User → Many Jobs
```

---

### Job → Proposals

A single job may generate multiple proposal versions.

Relationship:

```
One Job → Many Proposals
```

---

### Proposal → Evaluation

Each generated proposal currently has one AI evaluation.

Relationship:

```
One Proposal → One Evaluation
```

Future versions may support multiple evaluations, including AI, human reviewers, and client feedback.

---

# 9. Current Architecture

```text
                  User
                    │
                    ▼
          Agent Orchestrator
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Analyzer     Proposal     Pricing
        │
        ▼
 Retrieval Service
        │
        ▼
 Knowledge Base
        │
        ▼
 Repository Layer
        │
        ▼
 SQLAlchemy ORM
        │
        ▼
 SQLite Database
```

---

# 10. Separation of Responsibilities

## Knowledge Base

Responsible for static information.

Examples:

* Skills
* Portfolio Projects
* Resume
* Prompt Templates
* Company Information

---

## Database

Responsible for dynamic information.

Examples:

* Users
* Jobs
* Generated Proposals
* Evaluations
* Future Analytics

---

# 11. Repository Layer

The database is accessed exclusively through repositories.

```
BaseRepository

├── UserRepository
├── JobRepository
├── ProposalRepository
└── EvaluationRepository
```

The BaseRepository provides reusable CRUD functionality while each repository implements entity-specific queries.

---

# 12. Current Limitations

The current implementation intentionally focuses on simplicity.

Current limitations include:

* Single-user system
* No authentication
* No authorization
* SQLite only
* No migrations
* No soft deletes
* No audit logging
* No indexing optimization
* No transaction management beyond SQLAlchemy defaults

These limitations are acceptable for the MVP and educational goals of the project.

---

# 13. Future Improvements

The database layer is designed to evolve without requiring major architectural changes.

Planned enhancements include:

* PostgreSQL migration
* Alembic database migrations
* User authentication
* Role-based access control
* Proposal versioning
* Analytics tables
* Saved prompts
* Prompt history
* User preferences
* Activity logs
* Full-text search
* Performance indexing

---

# 14. Migration Plan

The transition from SQLite to PostgreSQL is expected to require minimal code changes.

Current:

```
SQLite
```

↓

Future:

```
PostgreSQL
```

↓

Future:

```
Cloud Hosted PostgreSQL
```

↓

Optional:

```
Read Replicas
```

The Repository Pattern and SQLAlchemy ORM abstract database operations, making the migration largely a configuration change rather than a complete rewrite.

---

# 15. Testing Strategy

The persistence layer has been validated through integration tests.

Verified operations include:

* Database initialization
* Record creation
* Record retrieval
* Record updates
* Record deletion
* Filtering
* Counting
* Relationship validation

The successful execution of these tests confirms that the repository layer and ORM mappings function correctly.

---

# 16. Design Decisions

| Decision               | Reason                             |
| ---------------------- | ---------------------------------- |
| SQLite                 | Lightweight local development      |
| SQLAlchemy             | ORM abstraction                    |
| Repository Pattern     | Separation of concerns             |
| Four primary entities  | Simplicity and scalability         |
| Generic BaseRepository | Code reuse                         |
| Foreign keys           | Data integrity                     |
| ORM Relationships      | Easier navigation between entities |

---

# 17. Conclusion

The database architecture provides a clean, modular, and extensible persistence layer for the AI Freelancer Proposal Assistant. By separating application logic from database access through the Repository Pattern and leveraging SQLAlchemy ORM, the design remains maintainable while preparing the project for future enhancements such as PostgreSQL migration, authentication, analytics, and production deployment.

This database layer serves as the foundation for the upcoming FastAPI backend and supports the long-term evolution of the application without requiring significant architectural changes.
