from dataclasses import dataclass
from typing import List


@dataclass
class FreelancerProfile:
    name: str
    email: str
    linkedin: str
    bio: str
    skills: List[str]
    experience: str