from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from datetime import datetime

from database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True)

    title = Column(String)

    bio = Column(Text)

    experience = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="user")

    proposals = relationship("Proposal", back_populates="user")


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String)

    description = Column(Text)

    client_name = Column(String)

    budget = Column(String)

    deadline = Column(String)

    source = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="jobs")

    proposals = relationship("Proposal", back_populates="job")


class Proposal(Base):

    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(Integer, ForeignKey("jobs.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    analysis = Column(Text)

    proposal = Column(Text)

    pricing = Column(Text)

    timeline = Column(String)

    review = Column(Text)

    model = Column(String)

    prompt_version = Column(String)

    status = Column(String, default="Saved")

    category = Column(String)

    final_proposal = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="proposals")

    user = relationship("User", back_populates="proposals")

    evaluation = relationship(
        "Evaluation",
        back_populates="proposal",
        uselist=False
    )


class Evaluation(Base):

    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)

    proposal_id = Column(
        Integer,
        ForeignKey("proposals.id")
    )

    relevance = Column(Float)

    accuracy = Column(Float)

    personalization = Column(Float)

    completeness = Column(Float)

    tone = Column(Float)

    hallucination = Column(Float)

    overall_score = Column(Float)

    evaluator_feedback = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    proposal = relationship(
        "Proposal",
        back_populates="evaluation"
    )

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String, nullable=False, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    proposal_id = Column(
        Integer,
        ForeignKey("proposals.id"),
        nullable=True,
        index=True
    )

    properties = Column(JSON, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )