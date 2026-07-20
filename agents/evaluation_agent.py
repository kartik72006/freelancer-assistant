import time

from utils.json_parser import parse_json


class EvaluationAgent:

    def __init__(self, llm):

        self.llm = llm

    def evaluate(
        self,
        job_description,
        proposal
    ):

        prompt = f"""
You are an expert AI evaluator for freelancer proposals.

Evaluate the proposal ONLY using the given job description.

Score the proposal on the following criteria.

1. Relevance
2. Accuracy
3. Personalization
4. Completeness
5. Tone
6. Hallucination

Scoring Rules:
- Every score must be an integer from 0 to 10.
- Hallucination:
    10 = No fabricated information.
    0 = Completely fabricated proposal.

Also provide ONE concise sentence explaining each score.

Use the full range from 0 to 10.

Do not avoid low scores.

A professional but generic proposal should score around 5–7.

Reserve scores of 9–10 for proposals that are exceptionally tailored and evidence-based.

Be a strict evaluator.

Return ONLY valid JSON.

Job Description:
----------------
{job_description}

Proposal:
----------------
{proposal}

Return exactly in this format:

{{
    "relevance": 0,
    "accuracy": 0,
    "personalization": 0,
    "completeness": 0,
    "tone": 0,
    "hallucination": 0,
    "feedback": {{
        "relevance": "",
        "accuracy": "",
        "personalization": "",
        "completeness": "",
        "tone": "",
        "hallucination": ""
    }}
}}
"""

        required_keys = [
            "relevance",
            "accuracy",
            "personalization",
            "completeness",
            "tone",
            "hallucination",
            "feedback"
        ]

        retries = 3

        for attempt in range(retries):

            try:

                print(
                    f"Evaluation Attempt {attempt + 1}"
                )

                response = self.llm.generate(
                    prompt
                )

                result = parse_json(
                    response
                )

                if result is None:

                    print(
                        "Invalid JSON received."
                    )

                    continue

                missing = [
                    key
                    for key in required_keys
                    if key not in result
                ]

                if missing:

                    print(
                        f"Missing Keys: {missing}"
                    )

                    continue

                result["overall"] = (

                    result["relevance"]

                    + result["accuracy"]

                    + result["personalization"]

                    + result["completeness"]

                    + result["tone"]

                    + result["hallucination"]

                )

                return result

            except Exception as e:

                print(
                    f"Evaluation Attempt {attempt + 1} Failed"
                )

                print(e)

                time.sleep(2)

        return {

            "success": False,

            "error": "Evaluation Failed"

        }