# Freelancer Assistant 🚀

An AI-powered freelancer proposal generator that helps freelancers create professional and personalized project proposals using Google's Gemini API.

---

## 📌 Problem Statement

Freelancers spend a significant amount of time writing proposals for similar job postings. Despite investing hours in creating proposals, many applications receive little or no response.

This project aims to reduce the time spent on proposal writing by using Large Language Models (LLMs) to generate professional proposals based on a client's job description and the freelancer's profile.

---

## 🎯 Objective

Build an AI assistant that can:

* Analyze a job description.
* Generate professional freelancer proposals.
* Personalize proposals based on freelancer information.
* Reduce repetitive work and improve productivity.

---

## ⚙️ Current Features

### ✅ Proposal Generation

* Accepts a job description as input.
* Uses Gemini API to generate a professional proposal.
* Produces structured and professional outputs.

### ✅ Professional Tone

* Generates proposals in a client-friendly format.
* Includes introduction, expertise, and call-to-action sections.

---

## 🏗️ Project Structure

```text
freelancer-assistant/
│
├── main.py
├── prompts.py
├── .env
├── README.md
└── venv/
```

---

## 🛠️ Tech Stack

* Python
* Gemini API
* Google GenAI SDK
* python-dotenv
* VS Code

---

## 🔄 Application Workflow

```text
Job Description
        ↓
     Prompt
        ↓
   Gemini API
        ↓
Generated Proposal
```

Future workflow:

```text
Freelancer Profile
        +
Past Projects
        +
Job Description
        ↓
     Gemini API
        ↓
Personalized Proposal
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone <repository-link>
cd freelancer-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install google-genai
pip install python-dotenv
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Running the Project

```bash
python main.py
```

Enter the job description when prompted.

Example:

```text
Need a Python Developer to build a SaaS dashboard with authentication and payment integration.
```

The application will generate a professional proposal using Gemini.

---

## 📈 Future Improvements

* Freelancer profile management
* Skills and portfolio integration
* Proposal personalization
* Pricing estimation
* Timeline estimation
* Proposal history
* Proposal analytics dashboard
* Retrieval-Augmented Generation (RAG)
* AI learning engine based on proposal outcomes
* Web application with React frontend
* Database integration

---

## ⚠️ Current Limitations

* May generate generic proposals.
* May hallucinate experience or skills if freelancer information is not provided.
* No proposal evaluation mechanism yet.
* No proposal performance tracking.

---

## 🎓 Learning Goals

This project is part of an 8-week roadmap to learn:

* AI Product Management
* Prompt Engineering
* Python Development
* Backend Engineering
* RAG Systems
* Product Analytics
* Full-Stack Development

---

## 👨‍💻 Author

Kartik Bansal

B.Tech Electronics and Computer Engineering

Aspiring AI Product Manager | Technical Product Manager | Product Engineer
