"""
Database Layer Integration Test

Tests:
- User Repository
- Job Repository
- Proposal Repository
- Evaluation Repository

Author: Kartik Bansal
"""

from database.db import SessionLocal

from database.repositories import (
    UserRepository,
    JobRepository,
    ProposalRepository,
    EvaluationRepository,
)


def main():

    db = SessionLocal()

    user_repo = UserRepository()
    job_repo = JobRepository()
    proposal_repo = ProposalRepository()
    evaluation_repo = EvaluationRepository()

    try:

        print("=" * 60)
        print("DATABASE TEST")
        print("=" * 60)

        # --------------------------------------------------
        # CREATE USER
        # --------------------------------------------------

        print("\nCreating User...")

        user = user_repo.create(
            db=db,
            name="Kartik Bansal",
            email="kartik@test.com",
            title="AI Product Engineer",
            bio="Building AI Freelancer Proposal Assistant",
            experience=2,
        )

        print("User Created:", user.id)

        # --------------------------------------------------
        # CREATE JOB
        # --------------------------------------------------

        print("\nCreating Job...")

        job = job_repo.create(
            db=db,
            user_id=user.id,
            title="React Dashboard",
            description="Need React Developer",
            client_name="ABC Ltd",
            budget="$1000",
            deadline="7 Days",
            source="Upwork",
        )

        print("Job Created:", job.id)

        # --------------------------------------------------
        # CREATE PROPOSAL
        # --------------------------------------------------

        print("\nCreating Proposal...")

        proposal = proposal_repo.create(
            db=db,
            job_id=job.id,
            user_id=user.id,
            proposal="Hello, I can build your dashboard.",
            pricing="$900",
            timeline="5 Days",
            review="Looks Good",
            model="Gemini",
            prompt_version="v1",
        )

        print("Proposal Created:", proposal.id)

        # --------------------------------------------------
        # CREATE EVALUATION
        # --------------------------------------------------

        print("\nCreating Evaluation...")

        evaluation = evaluation_repo.create(
            db=db,
            proposal_id=proposal.id,
            relevance=9.5,
            accuracy=9.8,
            personalization=9.7,
            completeness=9.3,
            tone=9.4,
            hallucination=0.1,
            overall_score=9.54,
            evaluator_feedback="Excellent proposal",
        )

        print("Evaluation Created:", evaluation.id)

        # --------------------------------------------------
        # READ TESTS
        # --------------------------------------------------

        print("\nTesting Reads...")

        print(user_repo.get_by_id(db, user.id))
        print(job_repo.get_by_id(db, job.id))
        print(proposal_repo.get_by_id(db, proposal.id))
        print(evaluation_repo.get_by_id(db, evaluation.id))

        # --------------------------------------------------
        # FILTER TESTS
        # --------------------------------------------------

        print("\nTesting Filters...")

        print(
            proposal_repo.get_proposals_by_user(
                db,
                user.id,
            )
        )

        print(
            job_repo.get_jobs_by_user(
                db,
                user.id,
            )
        )

        # --------------------------------------------------
        # UPDATE TEST
        # --------------------------------------------------

        print("\nTesting Update...")

        proposal_repo.update(
            db,
            proposal,
            pricing="$950",
        )

        proposal = proposal_repo.get_by_id(
            db,
            proposal.id,
        )

        print("Updated Pricing:", proposal.pricing)

        # --------------------------------------------------
        # COUNT
        # --------------------------------------------------

        print("\nTesting Count...")

        print(
            "Users:",
            user_repo.count(db),
        )

        print(
            "Jobs:",
            job_repo.count(db),
        )

        print(
            "Proposals:",
            proposal_repo.count(db),
        )

        print(
            "Evaluations:",
            evaluation_repo.count(db),
        )

        print("\nSUCCESS!")

    finally:

        db.close()


if __name__ == "__main__":
    main()