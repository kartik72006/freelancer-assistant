from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health, proposal, analysis, review, analytics
from contextlib import asynccontextmanager

from api.dependencies import retrieval_service
from api.startup import initialize_retrieval
from database.init_db import initialize_database
from scripts.seed_demo_data import seed_database_if_empty


@asynccontextmanager
async def lifespan(app):
    initialize_database()   
    seed_database_if_empty()
    initialize_retrieval(retrieval_service)
    yield

app = FastAPI(
    title="AI Freelancer Proposal Assistant API",
    description="Backend API for generating AI-powered freelancer proposals.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(health.router)
app.include_router(analysis.router)
app.include_router(proposal.router)
app.include_router(review.router)
app.include_router(analytics.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to AI Freelancer Proposal Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }