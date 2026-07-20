from services.ai.knowledge_service import KnowledgeService


class AnalyzerAgent:

    def __init__(self):
        self.skills_db = KnowledgeService.load_skills()

    def analyze(self, job_description):

        jd_normalized = (
            job_description
            .lower()
            .replace(".", "")
            .replace("-", " ")
        )

        detected_skills = []

        for skill in self.skills_db:
            if skill.lower() in jd_normalized:
                detected_skills.append(skill)

        complexity = self._estimate_complexity(
            detected_skills,
            jd_normalized
        )

        budget = self._estimate_budget(
            complexity
        )

        timeline = self._estimate_timeline(
            complexity
        )

        category = self._detect_category(
            detected_skills
        )

        return {
            "projectType": category,

            "skills": [
                {
                    "label": skill,
                    "reason": f"Detected because '{skill}' was mentioned in the job description.",
                    "confidence": 95
                }
                for skill in detected_skills
            ],

            "complexity": complexity,

            "estimatedBudget": budget,

            "timeline": timeline,

            "budgetConfidence": 85,

            "timelineConfidence": 90,

            "summary": self._generate_summary(
                category,
                complexity,
                detected_skills
            ),

            "clientGoal": self._detect_client_goal(
                job_description
            ),

            "toneSignals": self._detect_tone(
                job_description
            ),

            "redFlags": self._detect_red_flags(
                job_description
            )
        }

    def _estimate_complexity(
        self,
        skills,
        jd_normalized
    ):

        score = len(skills)

        hard_keywords = [
            "authentication",
            "payment",
            "dashboard",
            "real-time",
            "scalable",
            "ai",
            "machine learning",
            "rag",
            "chatbot"
        ]

        for keyword in hard_keywords:
            if keyword in jd_normalized:
                score += 1

        if score <= 2:
            return "Low"

        elif score <= 5:
            return "Medium"

        else:
            return "High"

    def _estimate_budget(
        self,
        complexity
    ):

        mapping = {
            "Low": "$100 - $300",
            "Medium": "$300 - $1000",
            "High": "$1000+"
        }

        return mapping[complexity]

    def _estimate_timeline(
        self,
        complexity
    ):

        mapping = {
            "Low": "2-5 Days",
            "Medium": "1-3 Weeks",
            "High": "1+ Months"
        }

        return mapping[complexity]

    def _detect_category(
        self,
        skills
    ):

        categories = {
            "Web Development": [
                "React",
                "JavaScript",
                "Node.js",
                "HTML",
                "CSS"
            ],
            "Backend Development": [
                "Python",
                "Django",
                "FastAPI"
            ],
            "AI Development": [
                "Machine Learning",
                "LLM",
                "LangChain"
            ],
            "Data Engineering": [
                "SQL",
                "Pandas"
            ]
        }

        scores = {}

        for category, techs in categories.items():

            score = sum(
                1 for skill in skills
                if skill in techs
            )

            scores[category] = score

        return max(scores, key=lambda x: scores[x])

    def _generate_summary(
        self,
        category,
        complexity,
        skills,
    ):

        return (
            f"{complexity} {category} project "
            f"requiring {', '.join(skills)}."
        )

    def _detect_client_goal(
        self,
        job_description,
    ):
        jd = job_description.lower()

        if "build" in jd:
            return "Build a new product"

        if "improve" in jd:
            return "Improve an existing product"

        if "fix" in jd:
            return "Bug fixing"

        return "General development"

    def _detect_tone(
        self,
        job_description,
    ):
        jd = job_description.lower()

        tones = []

        if "urgent" in jd:
            tones.append("Urgent")

        if "long term" in jd:
            tones.append("Long-Term")

        if "expert" in jd:
            tones.append("High Expectations")

        if not tones:
            tones.append("Professional")

        return tones

    def _detect_red_flags(
        self,
        job_description,
    ):
        jd = job_description.lower()

        flags = []

        keywords = [
            "cheap",
            "immediately",
            "unlimited revisions",
            "fixed budget",
            "tight deadline",
        ]

        for keyword in keywords:
            if keyword in jd:
                flags.append(keyword.title())

        return flags