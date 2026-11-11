"""
Wrapper for skill_gap logic in src/
"""
from skill_gap import (
    ROLE_REQUIREMENTS,
    SKILL_RESOURCES,
    get_available_roles,
    get_all_unique_skills,
    get_required_skills,
    analyze_skill_gap,
    generate_personalized_recommendations,
)

__all__ = [
    "ROLE_REQUIREMENTS",
    "SKILL_RESOURCES",
    "get_available_roles",
    "get_all_unique_skills",
    "get_required_skills",
    "analyze_skill_gap",
    "generate_personalized_recommendations",
]
