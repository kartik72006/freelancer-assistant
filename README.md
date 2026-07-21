# 🚀 AI Freelancer Proposal Assistant

An AI-powered web application that helps freelancers generate highly personalized, professional proposals in minutes using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and a multi-agent architecture.

Instead of writing every proposal from scratch, users can analyze a job post, generate a tailored proposal, review AI quality, edit the final output, and manage proposal history—all from a single dashboard.

---

## ✨ Features

### 🤖 AI Proposal Generation
- Personalized proposals from job descriptions
- Context-aware proposal generation
- Professional proposal formatting
- AI-generated timelines
- Integrated pricing recommendations
- One-click proposal editing

---

### 🧠 Multi-Agent AI Pipeline

The application uses specialized AI agents for different tasks.

- **Analyzer Agent**
  - Extracts project requirements
  - Detects technologies
  - Estimates project complexity
  - Identifies client priorities

- **Proposal Agent**
  - Generates personalized proposals
  - Uses retrieved portfolio context
  - Creates structured proposal sections

- **Review Agent**
  - Evaluates proposal quality
  - AI scoring
  - Strengths & improvement suggestions
  - Professionalism analysis

---

### 📚 Retrieval-Augmented Generation (RAG)

Instead of relying only on the language model, proposals are enhanced using a semantic knowledge base.

Features include:

- Persistent ChromaDB Vector Database
- SentenceTransformer Embeddings
- Semantic Search
- Portfolio Retrieval
- Similarity Filtering
- Context Formatting

Knowledge Base:

- Professional Profile
- Skills
- Portfolio Projects

---

### 📊 Analytics Dashboard

Track proposal performance through interactive analytics.

Includes:

- Total Proposals
- Proposal Acceptance Rate
- Average AI Score
- Proposal Funnel
- Feature Usage
- Proposal Trends
- AI Score Trends
- Client Insights
- Product Health Metrics

---

### 🧪 Prompt Engineering & Evaluation

The project includes an experimentation framework for comparing prompt strategies.

Implemented experiments:

- Standard Prompt
- Client-First Prompt
- Portfolio-First Prompt
- Outcome-Oriented Prompt
- Reviewer Checklist Prompt

Evaluation includes:

- AI Score
- Latency
- Benchmark Reports
- Automated Comparison
- Experiment Reports

---

## 🏗️ Architecture

```
                    React + Vite Frontend
                             │
                             ▼
                      FastAPI Backend
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
          ▼                                     ▼
     Analytics Service                  Proposal Service
          │                                     │
          └──────────────┬──────────────────────┘
                         ▼
                  Agent Orchestrator
                         │
 ┌──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼
Analyzer     Proposal       Review
 Agent         Agent          Agent
                         │
                         ▼
                 Retrieval Service
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     ChromaDB                    Knowledge Base
     Vector Store      (Projects • Skills • Profile)
```

---

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Material UI
- Radix UI
- Recharts

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Python

### AI & Machine Learning

- Google Gemini
- OpenRouter
- Sentence Transformers
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Database

- SQLite
- ChromaDB Vector Store

---

## 📂 Project Structure

```
Freelancer-Assistant/

├── agents/
├── api/
├── app/
├── config/
├── data/
├── database/
├── docs/
├── evaluation/
├── frontend/
├── knowledge_base/
├── models/
├── scripts/
├── services/
├── tests/
├── utils/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/kartik72006/freelancer-assistant.git

cd freelancer-assistant
```

---

### 2. Create Virtual Environment

Windows

```bash
py -3.13 -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Frontend Dependencies

```bash
cd frontend

npm install
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_key_here

OPENROUTER_API_KEY=your_key_here
```

---

## ▶️ Running the Application

### Backend

```bash
uvicorn api.main:app --reload
```

Backend:

```
http://localhost:8000
```

API Docs:

```
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## 📸 Screenshots

### Dashboard

> *(Add screenshot here)*

---

### Proposal Generator

> *(Add screenshot here)*

---

### Analytics

> *(Add screenshot here)*

---

### Proposal Review

> *(Add screenshot here)*

---

## 📈 Product Metrics

Current product tracks:

- Total Proposals
- Accepted Proposals
- Proposal Acceptance Rate
- Average AI Score
- Feature Usage
- Proposal Funnel
- Proposal Trends
- Weekly Activity
- Top Clients

---

## 🧪 Future Improvements

- User Authentication
- Cloud Database (PostgreSQL)
- Proposal Templates
- Proposal Export (PDF/DOCX)
- Stripe Subscription Plans
- Email Integration
- Team Collaboration
- Proposal Version History

---

## 📖 Documentation

Additional documentation can be found in the `docs/` directory.

Topics include:

- Architecture
- Product Decisions
- RAG Implementation
- Analytics
- Experiment Reports

---

## 👨‍💻 Author

**Kartik Bansal**

AI Product Engineer | Product Management Enthusiast

GitHub:
https://github.com/kartik72006

LinkedIn:
https://www.linkedin.com/in/kartik-bansal-bb49802b0

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.