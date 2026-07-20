"""Legacy keyword retrieval for the pre-semantic-retrieval baseline."""

from services.ai.knowledge_service import KnowledgeService


class RetrievalService:

    @staticmethod
    def retrieve_projects(job_description):
        """Match projects only by their technology stack.

        Older portfolio records used ``tech_stack``. The current portfolio schema
        calls the equivalent field ``technologies``; no title or description
        keywords are used in this baseline retriever.
        """
        job_text = job_description.lower()
        known_skills = KnowledgeService.load_skills()
        relevant_skills = [
            skill for skill in known_skills if skill.lower() in job_text
        ]
        relevant_projects = []

        for project in KnowledgeService.load_projects():
            tech_stack = project.get("technologies", [])
            matched_skills = [
                skill for skill in relevant_skills
                if any(skill.lower() == tech.lower() for tech in tech_stack)
            ]
            if not matched_skills:
                continue

            relevant_projects.append({
                "title": project["title"],
                "description": project["description"],
                # Keep the legacy response key for callers that expect it.
                "tech_stack": tech_stack,
                "score": len(matched_skills) * 5,
            })

        relevant_projects.sort(key=lambda project: project["score"], reverse=True)
        return {
            "skills": relevant_skills,
            "projects": relevant_projects[:3],
        }
