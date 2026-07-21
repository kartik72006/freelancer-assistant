from typing import Any

class PromptService:
            
    @staticmethod
    def proposal_prompt(
                profile: dict[str, Any],
                context: str,
                job_description: str,
                version: str ="v1"
            ) -> str:

            if  version=="v1":
                return f"""
        You are an expert freelance proposal writer.

        Your goal is to create a highly personalized and professional proposal that maximizes the freelancer's chances of winning the project.

        You have access to:

        1. The freelancer's profile.
        2. Relevant past projects retrieved from the freelancer's portfolio.
        3. The client's job description.

        Use these carefully.

        =========================
        FREELANCER PROFILE
        =========================

        {profile}

        =========================
        RELEVANT PROJECTS
        =========================

        {context}

        =========================
        CLIENT JOB DESCRIPTION
        =========================

        {job_description}

        =========================
        CONTACT INFORMATION
        =========================

        Email:
        {profile['email']}

        LinkedIn:
        {profile['linkedin']}

        --------------------------------------------------

        Important Instructions

        • Carefully analyze the client's requirements before writing.

        • Use ONLY the retrieved projects that are genuinely relevant to the client's needs.

        • Mention specific technologies, architectures, features, or outcomes from the retrieved projects whenever they strengthen the proposal.

        • Do NOT invent projects, technologies, achievements, or experience that are not present in the freelancer profile or retrieved context.

        • Do NOT mention unrelated projects simply because they were retrieved.

        • Instead of listing projects, naturally incorporate them as evidence of relevant experience.

        • Make the proposal sound human, confident, and tailored to this specific client.

        • Focus on explaining HOW the freelancer's previous work prepares them for this project.

        • Keep the proposal concise, professional, and client-focused.

        --------------------------------------------------

        Return ONLY valid JSON.

        Do NOT use markdown.

        Do NOT wrap the response inside ```json.

        Use exactly this schema:

        {{
            "introduction": "",
            "relevantExperience": "",
            "approach": "",
            "timeline": "",
            "pricing": ""
        }}

        --------------------------------------------------

        Writing Guidelines

        Introduction
        - Greet the client professionally.
        - Show understanding of the client's requirements.
        - Explain briefly why you are a strong fit.
        - Maximum 150 words.

        Relevant Experience
        - Mention only the most relevant retrieved projects.
        - Explain why each project is relevant.
        - Mention technologies, features, or measurable outcomes whenever appropriate.
        - Avoid generic statements.

        Approach
        - Provide a clear implementation plan.
        - Use numbered steps.
        - Focus on solving the client's problem rather than listing technologies.
        - Keep it concise.

        Timeline
        - Suggest a realistic delivery timeline.
        - Base it on the project complexity.

        Pricing
        - Recommend a realistic fixed price.
        - Keep the pricing in/near the client's budget (if provided)
        - Briefly justify the estimate.

        Return ONLY valid JSON.
        """
            
            elif version=="v2":
                  return f"""
        You are an expert freelance proposal writer.

        Your goal is to create a highly personalized and professional proposal that maximizes the freelancer's chances of winning the project.

        You have access to:

        1. The freelancer's profile.
        2. Relevant past projects retrieved from the freelancer's portfolio.
        3. The client's job description.

        Use these carefully.

        =========================
        FREELANCER PROFILE
        =========================

        {profile}

        =========================
        RELEVANT PROJECTS
        =========================

        {context}

        =========================
        CLIENT JOB DESCRIPTION
        =========================

        {job_description}

        =========================
        CONTACT INFORMATION
        =========================

        Email:
        {profile['email']}

        LinkedIn:
        {profile['linkedin']}

        --------------------------------------------------

        Important Instructions

        • Carefully analyze the client's requirements before writing.

        • Use ONLY the retrieved projects that are genuinely relevant to the client's needs.

        • Mention specific technologies, architectures, features, or outcomes from the retrieved projects whenever they strengthen the proposal.

        • Do NOT invent projects, technologies, achievements, or experience that are not present in the freelancer profile or retrieved context.

        • Do NOT mention unrelated projects simply because they were retrieved.

        • Instead of listing projects, naturally incorporate them as evidence of relevant experience.

        • Make the proposal sound human, confident, and tailored to this specific client.

        • Focus on explaining HOW the freelancer's previous work prepares them for this project.

        • Keep the proposal concise, professional, and client-focused.

        --------------------------------------------------

        Return ONLY valid JSON.

        Do NOT use markdown.

        Do NOT wrap the response inside ```json.

        Use exactly this schema:

        {{
            "introduction": "",
            "relevantExperience": "",
            "approach": "",
            "timeline": "",
            "pricing": ""
        }}

        --------------------------------------------------

        Writing Guidelines

        Introduction
        - Greet the client professionally.
        - Show understanding of the client's requirements.
        - Explain briefly why you are a strong fit.
        - Maximum 150 words.

        Relevant Experience

        For every retrieved project:

        1. Describe the business problem that project solved.

        2. Explain the solution that was built.

        3. Mention the measurable outcome or business value whenever available.

        4. Explain exactly why this experience reduces risk for THIS client.

        5. Mention technologies only when they strengthen the argument.

        Avoid listing projects.

        Instead, build a story connecting previous success to the client's current problem.
        - Explain why each project is relevant.
        - Mention technologies, features, or measurable outcomes whenever appropriate.
        - Avoid generic statements.

        Approach
        - Provide a clear implementation plan.
        - Use numbered steps.
        - Focus on solving the client's problem rather than listing technologies.
        - Keep it concise.

        Timeline
        - Suggest a realistic delivery timeline.
        - Base it on the project complexity.

        Pricing
        - Recommend a realistic fixed price.
        - Keep the pricing in/near the client's budget (if provided)
        - Briefly justify the estimate.
        

        Return ONLY valid JSON.
        """
            
            raise ValueError(f"Unknown prompt version: {version}")

    
    @staticmethod
    def review_prompt(
        proposal: str
        ) -> str:

        return f"""
    You are an expert proposal reviewer.

    Review the following freelancer proposal.

    Proposal:

    {proposal}

    Evaluate it on the following metrics:

    1. Professionalism
    2. Personalization
    3. Clarity
    4. Tone

    Return ONLY valid JSON.

    Example:

    {{
        "overallScore": 92,
        "verdict": "Excellent Proposal",
        "metrics": {{
            "professionalism": 95,
            "personalization": 90,
            "clarity": 94,
            "tone": 88
        }},
        "strengths": [
            "Strong personalization",
            "Professional tone",
            "Clear project understanding"
        ],
        "improvements": [
            "Mention post-launch support",
            "Reduce paragraph length"
        ]
    }}

    Do not return markdown.
    Return only JSON.
    """