
import json
import os
from config.settings import SKILLS_FILE
class KnowledgeService:

   
    @staticmethod
    def load_json(path):

        with open(path, "r", encoding="utf-8") as f:
            ...

            return json.load(f)

    @staticmethod
    def load_profile():

        return KnowledgeService.load_json(
            "knowledge_base/profile.json"
        )

    @staticmethod
    def load_skills():

        return KnowledgeService.load_json(
            "knowledge_base/skills.json"
        )

    @staticmethod
    def load_projects():

        return KnowledgeService.load_json(
            "knowledge_base/projects.json"
        )

    @staticmethod
    def load_past_proposals():

        return KnowledgeService.load_json(
            "knowledge_base/past_proposals.json"
        )