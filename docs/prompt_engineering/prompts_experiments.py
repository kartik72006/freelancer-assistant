ZERO_SHOT_PROMPT = """
Write a professional proposal.

Job Description:
{job_description}
"""

ROLE_PROMPT = """
You are a Top Rated Upwork freelancer.

Write a proposal.

Job Description:
{job_description}
"""

STRUCTURED_PROMPT = """
You are an expert proposal writer.

Skills:
{skills}

Experience:
{experience}

Job Description:
{job_description}

Rules:
1. Professional tone.
2. Maximum 250 words.
3. Do not invent skills.
"""

PERSONALIZED_PROMPT = """
You are an expert proposal writer.

Freelancer Name:
{name}

Skills:
{skills}

Past Projects:
{projects}

Job Description:
{job_description}

Write a personalized proposal explaining why the freelancer is a good fit.
"""

JSON_PROMPT = """
Return:

{{
"proposal":"",
"key_skills":"",
"client_problem":"",
"call_to_action":""
}}

Job Description:
{job_description}
"""