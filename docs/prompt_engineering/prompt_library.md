# Prompt Library V1

## Proposal Prompts
### Prompt 1 – Zero Shot

```text
Write a professional proposal for the following job.

Job Description:
{job_description}
```

Purpose:
Baseline proposal generation.
### Prompt 2 – Role Prompt

```text
You are a Top Rated Upwork freelancer.

Write a professional proposal for the following job.

Job Description:
{job_description}
```

Purpose:
Improve professionalism and tone.
### Prompt 3 – Structured Prompt
You are an expert freelancer proposal writer.

Freelancer Skills:
{skills}

Experience:
{experience}

Job Description:
{job_description}

Instructions:
1. Professional tone
2. Maximum 250 words
3. Mention only provided skills
4. Do not invent experience.

Purpose:
Reduce hallucinations.
### Prompt 4 – Personalized Proposal Prompt
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

Purpose:
Increase personalization.
### Prompt 5 – JSON Proposal Prompt
Generate the following JSON:

{
 "proposal":"",
 "key_skills":"",
 "client_problem":"",
 "call_to_action":""
}

Job Description:
{job_description}

Purpose:
Structured outputs for frontend.

## Pricing Prompts

### Prompt 6 – Basic Pricing
Estimate the price for the following project.

Job Description:
{job_description}
### Prompt 7 – Detailed Pricing
You are an experienced freelancer.

Estimate:

1. Minimum price
2. Recommended price
3. Premium price

Job Description:
{job_description}
### Prompt 8 – Pricing Explanation
Estimate project pricing and explain why the estimate was chosen.

Job Description:
{job_description}
### Prompt 9 – Hourly Pricing
Estimate:

Hours Required:
Hourly Rate:
Total Cost:

Job Description:
{job_description}
### Prompt 10 – JSON Pricing
Return:

{
 "minimum_price":"",
 "recommended_price":"",
 "premium_price":"",
 "reasoning":""
}

Job Description:
{job_description}

## Timeline Prompts
### Prompt 11 – Basic Timeline
Estimate the project timeline.

Job Description:
{job_description}
### Prompt 12 – Timeline with Milestones
Break the project into milestones.

Job Description:
{job_description}
### Prompt 13 – Detailed Timeline
Estimate:

1. Development Time
2. Testing Time
3. Deployment Time

Job Description:
{job_description}
### Prompt 14 – Timeline with Risks
Estimate the timeline and identify risks that could delay the project.

Job Description:
{job_description}
### Prompt 15 – JSON Timeline
Return:

{
 "timeline":"",
 "milestones":"",
 "risks":""
}

Job Description:
{job_description}

## Job Analysis Prompts
### Prompt 16 – Skill Extraction
Extract all required skills.

Job Description:
{job_description}
### Prompt 17 – Project Complexity
Classify this project as:

Easy
Medium
Hard

Explain why.

Job Description:
{job_description}
### Prompt 18 – Technology Extraction
List all technologies mentioned in the job description.

Job Description:
{job_description}
### Prompt 19 – Client Requirements
Summarize:

1. Client requirements
2. Deliverables
3. Constraints

Job Description:
{job_description}
### Prompt 20 – Complete Job Analysis
Analyze this job and return:

{
 "skills":"",
 "technologies":"",
 "project_type":"",
 "complexity":"",
 "estimated_budget":"",
 "estimated_timeline":""
}

Job Description:
{job_description}