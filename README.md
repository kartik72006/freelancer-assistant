# 🚀 AI Freelancer Proposal Assistant

> Generate personalized, high-quality freelance proposals in seconds using AI, Retrieval-Augmented Generation (RAG), and Product Analytics.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript" />
  <img src="https://img.shields.io/badge/ChromaDB-RAG-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Gemini-AI-red?style=for-the-badge&logo=google" />
</p>

---

# 🌐 Live Demo

### Frontend
**https://freelancer-assistant.vercel.app/**

### Backend API
**https://freelancer-assistant-production.up.railway.app/**

### API Documentation
**https://freelancer-assistant-production.up.railway.app/docs**

---

# 📌 Overview

Writing personalized freelance proposals is repetitive and time-consuming. Generic AI-generated proposals often fail because they lack personalization and relevant project experience.

The AI Freelancer Proposal Assistant solves this problem by combining:

- AI-powered proposal generation
- Retrieval-Augmented Generation (RAG)
- Personalized project retrieval
- AI proposal review
- Product Analytics Dashboard

Instead of producing generic proposals, the application retrieves the user's most relevant past projects before generating the proposal, making responses significantly more personalized.

---

# ✨ Features

## 🤖 AI Proposal Generation

- Generate complete freelance proposals
- Personalized introductions
- Relevant experience
- Technical approach
- Timeline generation
- Pricing recommendations

---

## 🧠 Retrieval-Augmented Generation (RAG)

Instead of relying only on prompting, the application retrieves relevant portfolio projects before proposal generation.

Features include:

- ChromaDB vector database
- Sentence Transformers embeddings
- Semantic similarity search
- Context formatting
- Intelligent project retrieval

---

## 📊 AI Proposal Review

Every generated proposal is evaluated using AI.

Metrics include:

- Overall AI Score
- Personalization
- Professionalism
- Clarity
- Tone
- Strengths
- Suggested Improvements

---

## 📈 Product Analytics Dashboard

Track product performance using analytics such as:

- Total proposals
- Proposal funnel
- Acceptance rate
- AI score trends
- Proposal trends
- Client insights
- Feature usage
- Product health metrics
- Recent activity

---

## 📁 Proposal Management

- Save proposals
- Duplicate proposals
- Delete proposals
- Search proposal history
- Edit proposals
- Export proposals

---

# 🛠 Tech Stack

## Frontend

- React
- TypeScript
- Vite
- TailwindCSS
- Radix UI
- Lucide Icons

---

## Backend

- FastAPI
- Python
- SQLAlchemy
- SQLite
- Repository Pattern
- Service Layer Architecture

---

## AI Stack

- Google Gemini
- OpenRouter
- Sentence Transformers
- ChromaDB
- RAG Pipeline

---

## Deployment

Frontend

- Vercel

Backend

- Railway

---

# 🏗 System Architecture

```
                User
                  │
                  ▼
          React Frontend
                  │
                  ▼
            FastAPI Backend
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
 Analyzer     Proposal      Review
   Agent        Agent         Agent
                  │
                  ▼
          Retrieval Service
                  │
      ┌───────────┼────────────┐
      ▼                        ▼
Sentence Transformers     ChromaDB
      │                        │
      └────────────┬───────────┘
                   ▼
         Relevant Projects
                   │
                   ▼
          Personalized Proposal
```

---

# 📂 Project Structure

```
Freelancer-Assistant/

├── agents/
│   ├── analyzer_agent.py
│   ├── proposal_agent.py
│   └── review_agent.py
│
├── api/
│   ├── routes/
│   ├── dependencies.py
│   └── main.py
│
├── database/
│   ├── models.py
│   ├── repositories/
│   └── db.py
│
├── services/
│   ├── ai/
│   ├── application/
│   └── retrieval/
│
├── knowledge_base/
│
├── frontend/
│
├── scripts/
│
└── docs/
```

---

# ⚙️ AI Workflow

```
Paste Job Description

        │

        ▼

Analyze Job

        │

        ▼

Retrieve Relevant Projects

        │

        ▼

Generate Proposal

        │

        ▼

Review Proposal

        │

        ▼

Save Proposal

        │

        ▼

Analytics Updated
```

---

# 📊 Product Metrics

The application tracks:

- Proposal Generation Funnel
- Proposal Success Rate
- AI Quality Score
- User Activity
- Client Insights
- Feature Usage
- Proposal Trends
- Acceptance Trends

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/kartik72006/freelancer-assistant.git

cd freelancer-assistant
```

---

## Backend Setup

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY

OPENROUTER_API_KEY=YOUR_API_KEY

OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

ENVIRONMENT=development

ENABLE_RETRIEVAL_LOGGING=True
```

---

## Initialize Database

```bash
python database/init_db.py
```

---

## Build Vector Database

```bash
python scripts/build_embeddings.py
```

---

## Seed Demo Data (Optional)

```bash
python scripts/seed_demo_data.py
```

---

## Run Backend

```bash
uvicorn api.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install
```

Create `.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Run

```bash
npm run dev
```

---

# 📚 API Endpoints

## Analysis

```
POST /analysis/analyze
```

---

## Proposal

```
POST /proposal/generate

POST /proposal/save

GET /proposal/history

GET /proposal/stats

GET /proposal/{id}

PUT /proposal/{id}/status

PUT /proposal/{id}/final

POST /proposal/{id}/duplicate

DELETE /proposal/{id}
```

---

## Review

```
POST /review/generate
```

---

## Analytics

```
GET /analytics/dashboard

GET /analytics/top-clients

GET /analytics/proposal-trend

GET /analytics/ai-score-trend

GET /analytics/status-distribution

GET /analytics/product-health

GET /analytics/proposal-funnel

GET /analytics/recent-activity

GET /analytics/feature-usage

GET /analytics/acceptance-trend
```

---

# 🎯 Future Improvements

- User Authentication
- Multi-user Support
- PDF Proposal Export
- Stripe Subscription
- Proposal Templates
- Team Workspaces
- A/B Prompt Testing
- Email Integration
- Proposal Version History
- Real Freelancer Profile Import

---

# 📸 Screenshots

> Add screenshots of:

- Home Page
- Proposal Generator
- AI Review
- Proposal History
- Analytics Dashboard

---

# 📈 Learning Outcomes

This project demonstrates:

- Product Thinking
- AI Product Engineering
- Retrieval-Augmented Generation
- Prompt Engineering
- FastAPI Development
- React + TypeScript
- REST API Design
- Repository Pattern
- Service Layer Architecture
- Product Analytics
- Deployment using Railway & Vercel

---

# 👨‍💻 Author

**Kartik Bansal**

LinkedIn

https://www.linkedin.com/in/kartik-bansal-bb49802b0/

GitHub

https://github.com/kartik72006

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork it

🛠️ Contribute improvements

---

# 📄 License

This project is licensed under the MIT License.