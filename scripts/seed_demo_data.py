"""
seed_demo_data.py

Production Demo Data Seeder
AI Freelancer Proposal Assistant

This script generates realistic demo data for:

- Users
- Jobs
- Proposals
- Evaluations
- Analytics Events

Author: Kartik Bansal
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

from sqlalchemy.orm import Session

from database.db import SessionLocal

from database.models import User
from database.models import Job
from database.models import Proposal
from database.models import Evaluation
from database.models import AnalyticsEvent



# ==========================================================
# CONFIGURATION
# ==========================================================

RANDOM_SEED = 42

TOTAL_PROPOSALS = 120

TOTAL_CLIENTS = 35

DAYS_OF_HISTORY = 180

COMMIT_BATCH_SIZE = 20

random.seed(RANDOM_SEED)

# ==========================================================
# DEMO USER
# ==========================================================

DEMO_USER = {
    "name": "Demo User",
    "email": "demo@example.com",
    "title": "AI Product Engineer",
    "bio": (
        "Experienced AI Product Engineer specializing in "
        "FastAPI, React, Python, RAG Systems, "
        "LLMs, Product Analytics and SaaS applications."
    ),
    "experience": 4,
}

# ==========================================================
# MODEL INFORMATION
# ==========================================================

AI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

PROMPT_VERSION = "v1.0"

# ==========================================================
# PROPOSAL STATUS DISTRIBUTION
# ==========================================================

STATUS_WEIGHTS = {
    "Accepted": 35,
    "Sent": 35,
    "Draft": 25,
    "Rejected": 5,
}

# ==========================================================
# PROJECT CATEGORIES
# ==========================================================

PROJECT_CATEGORIES = [
    "Artificial Intelligence",
    "Machine Learning",
    "Web Development",
    "Backend Development",
    "Frontend Development",
    "Full Stack Development",
    "Automation",
    "Data Science",
    "Computer Vision",
    "NLP",
    "Analytics",
    "Dashboard",
    "API Development",
    "SaaS",
]

# ==========================================================
# JOB SOURCES
# ==========================================================

JOB_SOURCES = [
    "Upwork",
    "Freelancer",
    "PeoplePerHour",
    "Toptal",
    "LinkedIn",
]

# ==========================================================
# EVENT NAMES
# (Must exactly match AnalyticsService)
# ==========================================================

EVENT_NAMES = {
    "generated": "proposal_generated",
    "sent": "proposal_sent",
    "accepted": "proposal_accepted",
    "rejected": "proposal_rejected",
    "edited": "proposal_edited",
    "duplicated": "proposal_duplicated",
    "deleted": "proposal_deleted",
    "exported": "proposal_exported",
}

# ==========================================================
# SCORE RANGES
# ==========================================================

AI_SCORE_RANGES = {
    "Accepted": (94, 99),
    "Sent": (88, 93),
    "Draft": (82, 87),
    "Rejected": (70, 81),
}

# ==========================================================
# CLIENT WEIGHTS
#
# Higher weight = more proposals from that client
# Makes dashboard analytics look realistic.
# ==========================================================

CLIENT_WEIGHTS = {
    "BlueOrbit Technologies": 12,
    "TechNova Solutions": 11,
    "ScaleLabs": 10,
    "NextGen AI": 10,
    "VisionCraft": 9,
    "CloudSphere": 9,
    "BrightStack": 8,
    "DataForge": 8,
    "Quantum Apps": 8,
    "PixelWorks": 7,
    "CodeBridge": 7,
    "Innovexa": 7,
    "SmartCore": 6,
    "Insight Systems": 6,
    "Elevate Digital": 6,
    "NovaLogic": 5,
    "Vertex Labs": 5,
    "LaunchGrid": 5,
    "HyperTech": 5,
    "AppNest": 5,
    "Apex Dynamics": 4,
    "AI Foundry": 4,
    "CloudNest": 4,
    "BrightMind": 4,
    "RocketSoft": 4,
    "CoreWave": 3,
    "Skyline Labs": 3,
    "PrimeStack": 3,
    "FutureWorks": 3,
    "DeepLogic": 3,
    "VisionEdge": 2,
    "Alpha Systems": 2,
    "Zenith Digital": 2,
    "Fusion AI": 2,
    "Orbit Technologies": 2,
}

# ==========================================================
# DATE RANGE
# ==========================================================

END_DATE = datetime.utcnow()

START_DATE = END_DATE - timedelta(days=DAYS_OF_HISTORY)

# ==========================================================
# RANDOM TEXT HELPERS
# ==========================================================

VERDICTS = [
    "Excellent proposal with strong client alignment.",
    "Highly personalized proposal.",
    "Professional and technically sound proposal.",
    "Very competitive proposal.",
    "Well structured proposal with clear value proposition.",
]

STRENGTHS = [
    "Strong technical alignment.",
    "Excellent personalization.",
    "Professional writing style.",
    "Clear implementation approach.",
    "Realistic timeline.",
    "Competitive pricing.",
    "Good understanding of client requirements.",
]

IMPROVEMENTS = [
    "Add more quantified achievements.",
    "Improve project personalization.",
    "Include stronger business outcomes.",
    "Provide more implementation details.",
    "Highlight relevant technologies.",
    "Improve closing statement.",
]

# ==========================================================
# TECHNOLOGY STACKS
# ==========================================================

TECH_STACKS = {
    "Artificial Intelligence": [
        "Python",
        "FastAPI",
        "LangChain",
        "OpenAI",
        "Gemini",
        "ChromaDB",
        "FAISS",
        "SentenceTransformers",
        "PostgreSQL",
    ],
    "Machine Learning": [
        "Python",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
    ],
    "Web Development": [
        "React",
        "TypeScript",
        "Node.js",
        "FastAPI",
        "Tailwind CSS",
        "PostgreSQL",
    ],
    "Backend Development": [
        "Python",
        "FastAPI",
        "Django",
        "SQLAlchemy",
        "PostgreSQL",
        "Redis",
    ],
    "Frontend Development": [
        "React",
        "Next.js",
        "TypeScript",
        "Tailwind CSS",
        "Material UI",
    ],
    "Full Stack Development": [
        "React",
        "FastAPI",
        "TypeScript",
        "PostgreSQL",
        "Docker",
    ],
    "Automation": [
        "Python",
        "Selenium",
        "Playwright",
        "BeautifulSoup",
    ],
    "Data Science": [
        "Python",
        "Pandas",
        "NumPy",
        "Power BI",
        "Matplotlib",
    ],
    "Computer Vision": [
        "OpenCV",
        "PyTorch",
        "YOLO",
        "TensorFlow",
    ],
    "NLP": [
        "Transformers",
        "spaCy",
        "Gemini",
        "OpenAI",
        "Python",
    ],
    "Analytics": [
        "SQL",
        "Power BI",
        "Python",
        "Pandas",
    ],
    "Dashboard": [
        "React",
        "Recharts",
        "Chart.js",
        "FastAPI",
    ],
    "API Development": [
        "FastAPI",
        "REST",
        "JWT",
        "PostgreSQL",
    ],
    "SaaS": [
        "React",
        "FastAPI",
        "Stripe",
        "Docker",
        "AWS",
    ],
}

# ==========================================================
# PROJECT TITLES
# ==========================================================

PROJECT_TITLES = {
    "Artificial Intelligence": [
        "Build AI Resume Analyzer",
        "Develop AI Chatbot",
        "Create RAG Knowledge Assistant",
        "LLM-powered Customer Support System",
        "AI Proposal Generator",
    ],
    "Machine Learning": [
        "Sales Prediction Model",
        "Fraud Detection Pipeline",
        "Demand Forecasting",
        "Recommendation Engine",
        "Customer Churn Prediction",
    ],
    "Backend Development": [
        "FastAPI Backend",
        "REST API Development",
        "Microservice Backend",
        "Authentication Service",
        "Payment API",
    ],
    "Frontend Development": [
        "React Dashboard",
        "Admin Panel",
        "Analytics Dashboard",
        "Landing Page",
        "Portfolio Website",
    ],
    "Full Stack Development": [
        "Task Management SaaS",
        "CRM Platform",
        "Property Rental Platform",
        "Healthcare Portal",
        "E-commerce Platform",
    ],
    "Automation": [
        "Web Scraping Bot",
        "Invoice Automation",
        "Excel Automation",
        "Workflow Automation",
    ],
    "Analytics": [
        "Business Dashboard",
        "Product Analytics Dashboard",
        "Sales Dashboard",
        "Executive Dashboard",
    ],
    "Dashboard": [
        "KPI Dashboard",
        "Marketing Dashboard",
        "Finance Dashboard",
        "Operations Dashboard",
    ],
    "Computer Vision": [
        "Face Recognition System",
        "Object Detection",
        "License Plate Detection",
    ],
    "NLP": [
        "Sentiment Analysis",
        "Document Summarizer",
        "Email Classification",
    ],
    "API Development": [
        "API Gateway",
        "Inventory API",
        "Booking API",
    ],
    "SaaS": [
        "Subscription Platform",
        "Project Management SaaS",
        "HR SaaS",
    ],
}

# ==========================================================
# CLIENT REQUIREMENTS
# ==========================================================

CLIENT_REQUIREMENTS = [
    "Clean, maintainable production-quality code.",
    "Well documented architecture.",
    "Strong communication throughout the project.",
    "Experience with similar projects.",
    "Daily progress updates.",
    "Scalable architecture.",
    "Responsive UI.",
    "Well-tested implementation.",
    "Deployment support.",
    "Long-term maintenance.",
]

# ==========================================================
# BUDGET RANGES
# ==========================================================

BUDGET_RANGES = [
    (300, 600),
    (600, 1000),
    (1000, 2000),
    (2000, 3500),
    (3500, 5000),
    (5000, 8000),
]

# ==========================================================
# TIMELINE OPTIONS
# ==========================================================

TIMELINES = [
    "3 Days",
    "5 Days",
    "1 Week",
    "2 Weeks",
    "3 Weeks",
    "1 Month",
]

# ==========================================================
# EXPERIENCE LEVELS
# ==========================================================

EXPERIENCE_LEVELS = [
    "Entry Level",
    "Intermediate",
    "Expert",
]

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def weighted_random_status():
    return random.choices(
        population=list(STATUS_WEIGHTS.keys()),
        weights=list(STATUS_WEIGHTS.values()),
        k=1,
    )[0]


def weighted_random_client():
    return random.choices(
        population=list(CLIENT_WEIGHTS.keys()),
        weights=list(CLIENT_WEIGHTS.values()),
        k=1,
    )[0]


def random_category():
    return random.choice(PROJECT_CATEGORIES)


def random_budget():
    low, high = random.choice(BUDGET_RANGES)
    return random.randint(low, high)


def random_created_at():
    seconds = random.randint(
        0,
        int((END_DATE - START_DATE).total_seconds()),
    )
    return START_DATE + timedelta(seconds=seconds)


def random_deadline(created_at: datetime):
    return created_at + timedelta(
        days=random.randint(5, 45)
    )


def random_technologies(category: str):
    technologies = TECH_STACKS.get(category, ["Python"])
    count = min(
        len(technologies),
        random.randint(3, 6),
    )
    return random.sample(technologies, count)


def random_project_title(category: str):
    titles = PROJECT_TITLES.get(
        category,
        ["Software Development Project"],
    )
    return random.choice(titles)


def random_experience_level():
    return random.choice(EXPERIENCE_LEVELS)


def random_source():
    return random.choice(JOB_SOURCES)


def random_timeline():
    return random.choice(TIMELINES)

# ==========================================================
# JOB DESCRIPTION BUILDING BLOCKS
# ==========================================================

PROJECT_OBJECTIVES = [
    "build a scalable production-ready application",
    "modernize an existing platform",
    "develop a new MVP",
    "improve application performance",
    "replace legacy architecture",
    "develop an AI-powered workflow",
    "build an analytics platform",
    "create a customer-facing SaaS product",
    "automate repetitive business processes",
    "integrate multiple third-party services",
]

RESPONSIBILITIES = [
    "design scalable architecture",
    "develop clean production-ready code",
    "integrate REST APIs",
    "optimize database performance",
    "write reusable components",
    "implement authentication",
    "deploy the application",
    "perform testing and debugging",
    "document the implementation",
    "collaborate during the development cycle",
]

BONUS_SKILLS = [
    "Docker",
    "AWS",
    "Azure",
    "CI/CD",
    "Redis",
    "Celery",
    "GraphQL",
    "Microservices",
    "Prompt Engineering",
    "RAG",
    "LLMs",
    "ChromaDB",
    "FAISS",
]

CLIENT_DESCRIPTIONS = [
    "We are an early-stage startup building AI-powered products.",
    "We are a rapidly growing SaaS company.",
    "We are looking for a long-term technical partner.",
    "Our company is expanding our engineering team.",
    "We need an experienced freelancer for a high-impact project.",
    "We are building the first version of our platform.",
    "We need to improve an existing production system.",
]

# ==========================================================
# GENERIC HELPERS
# ==========================================================

def random_date_between(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def weighted_choice(weight_dict: dict):
    return random.choices(
        population=list(weight_dict.keys()),
        weights=list(weight_dict.values()),
        k=1,
    )[0]


def random_score(minimum: int, maximum: int):
    return random.randint(minimum, maximum)


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


# ==========================================================
# JOB DESCRIPTION GENERATOR
# ==========================================================

def generate_job_description(category: str):

    technologies = random_technologies(category)

    responsibilities = random.sample(
        RESPONSIBILITIES,
        random.randint(4, 6),
    )

    bonus = random.sample(
        BONUS_SKILLS,
        random.randint(2, 4),
    )

    description = f"""
{random.choice(CLIENT_DESCRIPTIONS)}

Project Objective

We want to {random.choice(PROJECT_OBJECTIVES)}.

Responsibilities

"""

    for item in responsibilities:
        description += f"- {item}\n"

    description += "\nRequired Skills\n\n"

    for tech in technologies:
        description += f"- {tech}\n"

    description += "\nNice To Have\n\n"

    for skill in bonus:
        description += f"- {skill}\n"

    description += f"""

Experience Level

{random_experience_level()}

Timeline

{random_timeline()}

Additional Notes

{random.choice(CLIENT_REQUIREMENTS)}
"""

    return description.strip()


# ==========================================================
# JOB DATA GENERATOR
# ==========================================================

def generate_job():

    category = random_category()

    created_at = random_created_at()

    return {
        "title": random_project_title(category),
        "description": generate_job_description(category),
        "client_name": weighted_random_client(),
        "budget": random_budget(),
        "deadline": random_deadline(created_at),
        "source": random_source(),
        "category": category,
        "created_at": created_at,
    }


# ==========================================================
# PRICE GENERATOR
# ==========================================================

def generate_price(budget: int):

    multiplier = random.uniform(0.9, 1.15)

    price = int(budget * multiplier)

    return f"${price:,} Fixed Price"


# ==========================================================
# TIMELINE GENERATOR
# ==========================================================

def generate_delivery_timeline():

    return random.choice(
        [
            "3-5 Days",
            "1 Week",
            "2 Weeks",
            "3 Weeks",
            "1 Month",
        ]
    )


# ==========================================================
# AI SCORE GENERATOR
# ==========================================================

def generate_ai_score(status: str):

    low, high = AI_SCORE_RANGES[status]

    return random.randint(low, high)


# ==========================================================
# STATUS FROM SCORE
# (Fallback if needed)
# ==========================================================

def score_to_status(score: int):

    if score >= 92:
        return "Accepted"

    if score >= 86:
        return "Sent"

    if score >= 78:
        return "Draft"

    return "Rejected"

# ==========================================================
# ANALYSIS GENERATOR
# (Matches AnalyzerAgent Output)
# ==========================================================

def generate_analysis(job: dict):

    category = job["category"]

    technologies = random_technologies(category)

    estimated_budget = job["budget"]

    timeline = random_timeline()

    complexity = random.choice(
        [
            "Low",
            "Medium",
            "High",
        ]
    )

    return {
        "summary": (
            f"This project involves {category.lower()} "
            f"with a focus on scalable implementation."
        ),
        "requiredSkills": technologies,
        "matchingSkills": random.sample(
            technologies,
            max(2, min(len(technologies), 4)),
        ),
        "missingSkills": [],
        "complexity": complexity,
        "estimatedTimeline": timeline,
        "estimatedBudget": estimated_budget,
        "recommendation": random.choice(
            [
                "Strong Match",
                "Very Good Match",
                "Recommended",
            ]
        ),
    }


# ==========================================================
# PROPOSAL GENERATOR
# (Matches ProposalAgent Output)
# ==========================================================

INTRODUCTIONS = [
    "Hello! I would love to help you with this project.",
    "After reviewing your requirements, I believe I can deliver an excellent solution.",
    "Your project closely aligns with my experience building AI-powered applications.",
    "I have successfully delivered several projects with similar technical requirements.",
]

EXPERIENCE_PARAGRAPHS = [
    (
        "I have developed multiple production-grade applications "
        "using Python, FastAPI, React and modern AI technologies."
    ),
    (
        "My recent projects include scalable SaaS products, "
        "analytics dashboards and Retrieval-Augmented Generation systems."
    ),
    (
        "I specialize in backend architecture, AI integrations, "
        "database design and production deployments."
    ),
]

APPROACH_PARAGRAPHS = [
    (
        "I will begin by understanding your requirements, "
        "designing the architecture, implementing the backend, "
        "building the frontend, thoroughly testing the solution "
        "and providing deployment support."
    ),
    (
        "The implementation will follow clean architecture principles "
        "with modular code, proper documentation and scalability."
    ),
    (
        "Throughout development I will maintain regular communication "
        "and provide progress updates."
    ),
]

CLOSING_LINES = [
    "I look forward to discussing your project.",
    "Let's build something great together.",
    "Thank you for considering my proposal.",
]


def generate_proposal(job: dict):

    pricing = generate_price(job["budget"])

    timeline = generate_delivery_timeline()

    return {
        "introduction": random.choice(INTRODUCTIONS),

        "relevantExperience": random.choice(
            EXPERIENCE_PARAGRAPHS
        ),

        "approach": random.choice(
            APPROACH_PARAGRAPHS
        ),

        "timeline": timeline,

        "pricing": pricing,
    }


# ==========================================================
# FINAL PROPOSAL
#
# IMPORTANT
# Stored as JSON.
#
# ProposalService expects:
#
# json.loads(final_proposal)
#
# NOT plain text.
# ==========================================================

def generate_final_proposal(
    proposal: dict,
):

    final_intro = (
        proposal["introduction"]
        + "\n\n"
        + "I have carefully reviewed your requirements "
          "and believe my previous experience makes me "
          "an excellent fit for this project."
    )

    final_approach = (
        proposal["approach"]
        + "\n\n"
        + "I will also ensure proper documentation, "
          "testing and long-term maintainability."
    )

    return {
        "introduction": final_intro,
        "relevantExperience": proposal[
            "relevantExperience"
        ],
        "approach": final_approach,
        "timeline": proposal["timeline"],
        "pricing": proposal["pricing"],
    }


# ==========================================================
# REVIEW GENERATOR
#
# MUST MATCH ReviewAgent EXACTLY
# ==========================================================

def generate_review_from_score(overall):

    professionalism = clamp(
        overall + random.randint(-3, 2),
        60,
        100,
    )

    personalization = clamp(
        overall + random.randint(-4, 3),
        60,
        100,
    )

    clarity = clamp(
        overall + random.randint(-2, 3),
        60,
        100,
    )

    tone = clamp(
        overall + random.randint(-3, 3),
        60,
        100,
    )

    return {
        "overallScore": overall,
        "verdict": random.choice(VERDICTS),
        "metrics": {
            "professionalism": professionalism,
            "personalization": personalization,
            "clarity": clarity,
            "tone": tone,
        },
        "strengths": random.sample(
            STRENGTHS,
            random.randint(3, 5),
        ),
        "improvements": random.sample(
            IMPROVEMENTS,
            random.randint(2, 3),
        ),
    }


def generate_review(status):
    low, high = AI_SCORE_RANGES[status]
    score = random.randint(low, high)
    return generate_review_from_score(score)

# ==========================================================
# FEEDBACK GENERATOR
#
# Used in Evaluation table.
# ==========================================================

def generate_feedback(score: int):

    if score >= 92:
        return (
            "Excellent proposal with strong personalization "
            "and clear technical communication."
        )

    if score >= 86:
        return (
            "Strong proposal. Minor improvements could make "
            "it even more competitive."
        )

    if score >= 78:
        return (
            "Good proposal but needs stronger personalization "
            "and clearer business value."
        )

    return (
        "Proposal requires significant improvements in "
        "clarity and client alignment."
    )

# ==========================================================
# EVALUATION GENERATOR
# ==========================================================

def generate_evaluation(review: dict):

    overall = review["overallScore"]

    relevance = clamp(
        overall + random.uniform(-2.0, 2.0),
        60,
        100,
    )

    accuracy = clamp(
        overall + random.uniform(-2.5, 2.5),
        60,
        100,
    )

    personalization = clamp(
        review["metrics"]["personalization"]
        + random.uniform(-1.5, 1.5),
        60,
        100,
    )

    completeness = clamp(
        overall + random.uniform(-2.0, 2.0),
        60,
        100,
    )

    tone = clamp(
        review["metrics"]["tone"]
        + random.uniform(-1.5, 1.5),
        60,
        100,
    )

    hallucination = round(
        random.uniform(0.0, 2.0),
        2,
    )

    overall_score = round(
        (
            relevance
            + accuracy
            + personalization
            + completeness
            + tone
            - hallucination
        )
        / 5,
        2,
    )

    return {
        "relevance": round(relevance, 2),
        "accuracy": round(accuracy, 2),
        "personalization": round(personalization, 2),
        "completeness": round(completeness, 2),
        "tone": round(tone, 2),
        "hallucination": hallucination,
        "overall_score": overall_score,
        "evaluator_feedback": generate_feedback(
            int(overall_score)
        ),
    }


# ==========================================================
# ANALYTICS EVENT GENERATOR
# ==========================================================

def create_event(
    event_name: str,
    proposal_id: int,
    created_at: datetime,
):

    return {
        "event_name": event_name,
        "proposal_id": proposal_id,
        "created_at": created_at,
        "properties": {
            "source": "demo_seed",
            "version": "1.0",
        },
    }


# ==========================================================
# ANALYTICS LIFECYCLE
#
# MUST MATCH AnalyticsService
# ==========================================================

def generate_event_sequence(
    status: str,
    proposal_id: int,
    created_at: datetime,
):

    events = []

    current_time = created_at

    def add(event):

        nonlocal current_time

        current_time += timedelta(
            minutes=random.randint(3, 45)
        )

        events.append(
            create_event(
                event,
                proposal_id,
                current_time,
            )
        )

    add(EVENT_NAMES["generated"])

    if random.random() < 0.85:
        add(EVENT_NAMES["edited"])

    if status in [
        "Sent",
        "Accepted",
        "Rejected",
    ]:
        add(EVENT_NAMES["sent"])

    if status == "Accepted":
        add(EVENT_NAMES["accepted"])

        if random.random() < 0.70:
            add(EVENT_NAMES["exported"])

    elif status == "Rejected":
        add(EVENT_NAMES["rejected"])

    if random.random() < 0.08:
        add(EVENT_NAMES["duplicated"])

    if random.random() < 0.03:
        add(EVENT_NAMES["deleted"])

    return events


# ==========================================================
# ACTIVITY LABELS
# ==========================================================

ACTIVITY_MESSAGES = {
    EVENT_NAMES["generated"]:
        "Generated proposal",

    EVENT_NAMES["edited"]:
        "Edited proposal",

    EVENT_NAMES["sent"]:
        "Sent proposal",

    EVENT_NAMES["accepted"]:
        "Proposal accepted",

    EVENT_NAMES["rejected"]:
        "Proposal rejected",

    EVENT_NAMES["duplicated"]:
        "Duplicated proposal",

    EVENT_NAMES["deleted"]:
        "Deleted proposal",

    EVENT_NAMES["exported"]:
        "Exported proposal",
}


# ==========================================================
# RANDOM MODEL
# ==========================================================

def random_model():

    return random.choice(AI_MODELS)


# ==========================================================
# PROMPT VERSION
# ==========================================================

def random_prompt_version():

    return PROMPT_VERSION


# ==========================================================
# JSON SERIALIZER
# ==========================================================

def to_json(data):

    return json.dumps(data)


# ==========================================================
# DEBUG VALIDATION
# ==========================================================

def validate_json(data):

    try:
        json.loads(
            json.dumps(data)
        )
        return True
    except Exception:
        return False
    

# ==========================================================
# DATABASE HELPERS
# ==========================================================

def get_demo_user(db: Session) -> User:
    """
    Fetch the demo user if it exists,
    otherwise create it.
    """

    user = (
        db.query(User)
        .filter(
            User.email == DEMO_USER["email"]
        )
        .first()
    )

    if user:
        return user

    user = User(
        name=DEMO_USER["name"],
        email=DEMO_USER["email"],
        title=DEMO_USER["title"],
        bio=DEMO_USER["bio"],
        experience=DEMO_USER["experience"],
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✓ Created demo user (ID={user.id})")

    return user


# ==========================================================
# CLEAR EXISTING DEMO DATA
# ==========================================================

def clear_demo_data(db: Session, user_id: int):
    """
    Deletes all demo data for the demo user.
    """

    print("Removing previous demo data...")

    proposal_ids = [
        proposal.id
        for proposal in db.query(Proposal.id)
        .filter(
            Proposal.user_id == user_id
        )
        .all()
    ]

    if proposal_ids:

        (
            db.query(AnalyticsEvent)
            .filter(
                AnalyticsEvent.proposal_id.in_(proposal_ids)
            )
            .delete(synchronize_session=False)
        )

        (
            db.query(Evaluation)
            .filter(
                Evaluation.proposal_id.in_(proposal_ids)
            )
            .delete(synchronize_session=False)
        )

        (
            db.query(Proposal)
            .filter(
                Proposal.id.in_(proposal_ids)
            )
            .delete(synchronize_session=False)
        )

    (
        db.query(Job)
        .filter(
            Job.user_id == user_id
        )
        .delete(synchronize_session=False)
    )

    db.commit()

    print("✓ Previous demo data removed.")


# ==========================================================
# CREATE JOB
# ==========================================================

def create_job(
    db: Session,
    user_id: int,
):

    data = generate_job()

    job = Job(
        user_id=user_id,
        title=data["title"],
        description=data["description"],
        client_name=data["client_name"],
        budget=str(data["budget"]),
        deadline=data["deadline"].strftime("%d %b %Y"),
        source=data["source"],
        created_at=data["created_at"],
    )

    db.add(job)
    db.flush()

    return job, data


# ==========================================================
# CREATE PROPOSAL
# ==========================================================

def create_proposal(
    job: Job,
    job_data: dict,
    user_id: int,
):

    analysis = generate_analysis(
        {
            "category": job_data["category"],
            "budget": int(job.budget),
        }
    )

    proposal_json = generate_proposal(
        {
            "budget": int(job.budget),
        }
    )

    final_json = generate_final_proposal(
        proposal_json
    )

    # Generate a realistic AI score first
    overall_score = random.choices(
    population=[
        random.randint(94, 99),   # Excellent
        random.randint(88, 93),   # Very Good
        random.randint(82, 87),   # Good
        random.randint(70, 81),   # Average
    ],
    weights=[30, 35, 25, 10],
    k=1,
)[0]

    review_json = generate_review_from_score(
        overall_score
    )

    status = score_to_status(
        overall_score
    )

    proposal = Proposal(

        user_id=user_id,

        job_id=job.id,

        analysis=to_json(
            analysis
        ),

        proposal=to_json(
            proposal_json
        ),

        pricing=proposal_json["pricing"],

        timeline=proposal_json["timeline"],

        review=to_json(
            review_json
        ),

        final_proposal=to_json(
            final_json
        ),

        status=status,

        category=job_data["category"],

        model=random_model(),

        prompt_version=random_prompt_version(),

        created_at=job.created_at,

    )

    return (
        proposal,
        review_json,
    )


# ==========================================================
# CREATE EVALUATION
# ==========================================================

def create_evaluation(
    proposal: Proposal,
    review: dict,
):

    evaluation_data = generate_evaluation(
        review
    )

    evaluation = Evaluation(

        proposal=proposal,

        relevance=evaluation_data[
            "relevance"
        ],

        accuracy=evaluation_data[
            "accuracy"
        ],

        personalization=evaluation_data[
            "personalization"
        ],

        completeness=evaluation_data[
            "completeness"
        ],

        tone=evaluation_data[
            "tone"
        ],

        hallucination=evaluation_data[
            "hallucination"
        ],

        overall_score=evaluation_data[
            "overall_score"
        ],

        evaluator_feedback=evaluation_data[
            "evaluator_feedback"
        ],

        created_at=proposal.created_at,

    )

    return evaluation


# ==========================================================
# CREATE ANALYTICS EVENTS
# ==========================================================

def create_analytics_events(
    proposal: Proposal,
):

    sequence = generate_event_sequence(
        proposal.status,
        proposal.id,
        proposal.created_at,
    )

    events = []

    for event in sequence:

        events.append(
            AnalyticsEvent(
                event_name=event["event_name"],
                user_id=proposal.user_id,
                proposal_id=proposal.id,
                properties=event["properties"],
                created_at=event["created_at"],
            )
        )

    return events


# ==========================================================
# BATCH COMMIT
# ==========================================================

def batch_commit(
    db: Session,
    index: int,
):

    if index % COMMIT_BATCH_SIZE == 0:

        db.commit()

        print(
            f"Committed {index} proposals..."
        )

# ==========================================================
# MAIN SEEDING LOOP
# ==========================================================

def seed_demo_data():

    db = SessionLocal()

    try:

        print("=" * 60)
        print("Starting Demo Data Seeder...")
        print("=" * 60)

        user = get_demo_user(db)

        clear_demo_data(
            db,
            user.id,
        )

        proposal_count = 0
        evaluation_count = 0
        analytics_count = 0

        for i in range(TOTAL_PROPOSALS):

            # -----------------------------
            # Create Job
            # -----------------------------

            job, job_data = create_job(
                db,
                user.id,
            )

            # -----------------------------
            # Create Proposal
            # -----------------------------

            proposal, review = create_proposal(
                job,
                job_data,
                user.id,
            )

            db.add(proposal)

            db.flush()

            proposal_count += 1

            # -----------------------------
            # Evaluation
            # -----------------------------

            evaluation = create_evaluation(
                proposal,
                review,
            )

            db.add(evaluation)

            evaluation_count += 1

            # -----------------------------
            # Analytics
            # -----------------------------

            events = create_analytics_events(
                proposal
            )

            for event in events:
                db.add(event)

            analytics_count += len(events)

            # -----------------------------
            # Batch Commit
            # -----------------------------

            batch_commit(
                db,
                proposal_count,
            )

            if (i + 1) % 10 == 0:

                print(
                    f"Generated "
                    f"{i + 1}/{TOTAL_PROPOSALS} proposals..."
                )

        db.commit()

        validate_seed_data(
            db,
            user.id,
        )

        print_summary(
            db,
            user.id,
        )

        print()

        print("=" * 60)

        print("Demo data created successfully.")

        print(f"Jobs        : {proposal_count}")

        print(f"Proposals   : {proposal_count}")

        print(f"Evaluations : {evaluation_count}")

        print(f"Events       : {analytics_count}")

        print("=" * 60)

    except Exception as e:

        db.rollback()

        print()

        print("=" * 60)
        print("Seeder Failed")
        print("=" * 60)

        raise e

    finally:

        db.close()

# ==========================================================
# VALIDATION
# ==========================================================

def validate_seed_data(db: Session, user_id: int):
    """
    Validate generated demo data.
    """

    print("\nRunning validation...")

    proposal_count = (
        db.query(Proposal)
        .filter(Proposal.user_id == user_id)
        .count()
    )

    job_count = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .count()
    )

    evaluation_count = db.query(Evaluation).count()

    analytics_count = (
        db.query(AnalyticsEvent)
        .filter(AnalyticsEvent.user_id == user_id)
        .count()
    )

    print(f"Jobs         : {job_count}")
    print(f"Proposals    : {proposal_count}")
    print(f"Evaluations  : {evaluation_count}")
    print(f"Events       : {analytics_count}")

    assert proposal_count == TOTAL_PROPOSALS, (
        f"Expected {TOTAL_PROPOSALS} proposals, "
        f"found {proposal_count}"
    )

    assert evaluation_count >= TOTAL_PROPOSALS

    print("✓ Record count validation passed")

    # --------------------------------------
    # Validate JSON columns
    # --------------------------------------

    proposals = (
        db.query(Proposal)
        .filter(Proposal.user_id == user_id)
        .all()
    )

    json_errors = 0

    for proposal in proposals:

        try:
            json.loads(proposal.analysis)
            json.loads(proposal.proposal)
            json.loads(proposal.review)

            if proposal.final_proposal:
                json.loads(proposal.final_proposal)

        except Exception:
            json_errors += 1

    if json_errors > 0:
        raise Exception(
            f"{json_errors} proposals contain invalid JSON."
        )

    print("✓ JSON validation passed")

    # --------------------------------------
    # Validate evaluations
    # --------------------------------------

    missing_eval = 0

    for proposal in proposals:
        if proposal.evaluation is None:
            missing_eval += 1

    if missing_eval > 0:
        raise Exception(
            f"{missing_eval} proposals have no evaluation."
        )

    print("✓ Evaluation validation passed")

    # --------------------------------------
    # Validate analytics events
    # --------------------------------------

    valid_events = {
        "proposal_generated",
        "proposal_sent",
        "proposal_accepted",
        "proposal_rejected",
        "proposal_edited",
        "proposal_duplicated",
        "proposal_deleted",
        "proposal_exported",
    }

    invalid_events = (
        db.query(AnalyticsEvent)
        .filter(AnalyticsEvent.user_id == user_id)
        .all()
    )

    bad = [
        event.event_name
        for event in invalid_events
        if event.event_name not in valid_events
    ]

    if bad:
        raise Exception(
            f"Invalid analytics events found: {set(bad)}"
        )

    print("✓ Analytics validation passed")

    print("\nAll validations passed successfully.")

# ==========================================================
# SUMMARY REPORT
# ==========================================================

def print_summary(db: Session, user_id: int):

    print("\n")
    print("=" * 70)
    print("DEMO DATA SUMMARY")
    print("=" * 70)

    proposals = (
        db.query(Proposal)
        .filter(Proposal.user_id == user_id)
        .all()
    )

    jobs = (
        db.query(Job)
        .filter(Job.user_id == user_id)
        .all()
    )

    events = (
        db.query(AnalyticsEvent)
        .filter(AnalyticsEvent.user_id == user_id)
        .all()
    )

    evaluations = db.query(Evaluation).all()

    print(f"Users            : 1")
    print(f"Jobs             : {len(jobs)}")
    print(f"Proposals        : {len(proposals)}")
    print(f"Evaluations      : {len(evaluations)}")
    print(f"Analytics Events : {len(events)}")

    print()

    # -----------------------------------------------------
    # Status Distribution
    # -----------------------------------------------------

    status_counts = {}

    for proposal in proposals:
        status_counts[proposal.status] = (
            status_counts.get(proposal.status, 0) + 1
        )

    print("Proposal Status Distribution")

    for status, count in sorted(status_counts.items()):
        percentage = round(
            (count / len(proposals)) * 100,
            1,
        )

        print(
            f"  {status:<12} {count:>3} "
            f"({percentage:>5}%)"
        )

    print()

    # -----------------------------------------------------
    # Average AI Score
    # -----------------------------------------------------

    if evaluations:

        average_score = round(
            sum(
                evaluation.overall_score
                for evaluation in evaluations
            )
            / len(evaluations),
            2,
        )

        print(
            f"Average AI Score : {average_score}"
        )

    print()

    # -----------------------------------------------------
    # Acceptance Rate
    # -----------------------------------------------------

    accepted = status_counts.get(
        "Accepted",
        0,
    )

    acceptance_rate = round(
        accepted * 100 / len(proposals),
        2,
    )

    print(
        f"Acceptance Rate  : {acceptance_rate}%"
    )

    print()

    # -----------------------------------------------------
    # Top Clients
    # -----------------------------------------------------

    client_stats = {}

    for job in jobs:

        client_stats[job.client_name] = (
            client_stats.get(
                job.client_name,
                0,
            )
            + 1
        )

    top_clients = sorted(
        client_stats.items(),
        key=lambda x: x[1],
        reverse=True,
    )[:10]

    print("Top Clients")

    for client, count in top_clients:

        print(
            f"  {client:<30} {count}"
        )

    print()

    # -----------------------------------------------------
    # Event Distribution
    # -----------------------------------------------------

    event_counts = {}

    for event in events:

        event_counts[event.event_name] = (
            event_counts.get(
                event.event_name,
                0,
            )
            + 1
        )

    print("Analytics Events")

    for event, count in sorted(
        event_counts.items()
    ):

        print(
            f"  {event:<25} {count}"
        )

    print()

    # -----------------------------------------------------
    # AI Model Usage
    # -----------------------------------------------------

    model_usage = {}

    for proposal in proposals:

        model_usage[proposal.model] = (
            model_usage.get(
                proposal.model,
                0,
            )
            + 1
        )

    print("AI Model Usage")

    for model, count in model_usage.items():

        print(
            f"  {model:<20} {count}"
        )

    print()

    # -----------------------------------------------------
    # Proposal Categories
    # -----------------------------------------------------

    category_counts = {}

    for proposal in proposals:

        category_counts[proposal.category] = (
            category_counts.get(
                proposal.category,
                0,
            )
            + 1
        )

    print("Proposal Categories")

    for category, count in sorted(
        category_counts.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        print(
            f"  {category:<30} {count}"
        )

    print()

    print("=" * 70)
    print("Demo database seeded successfully.")
    print("=" * 70)

# ==========================================================
# MAIN
# ==========================================================

def main():

    print()
    print("=" * 70)
    print("AI Freelancer Proposal Assistant")
    print("Production Demo Data Seeder")
    print("=" * 70)
    print()

    start_time = datetime.now()

    try:

        seed_demo_data()

        elapsed = datetime.now() - start_time

        print()
        print("=" * 70)
        print("SEEDING COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print(
            f"Execution Time : {elapsed.total_seconds():.2f} seconds"
        )
        print("=" * 70)

    except KeyboardInterrupt:

        print()
        print("=" * 70)
        print("Seeder interrupted by user.")
        print("=" * 70)

    except Exception as e:

        print()
        print("=" * 70)
        print("SEEDING FAILED")
        print("=" * 70)
        print(f"Error : {e}")
        print("=" * 70)
        raise


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()