"""Pydantic models for Skillstore API responses."""

from pydantic import BaseModel


class SkillstoreResponse(BaseModel):
    """Response from GET /skillstore endpoint."""

    site: str
    skills: dict[str, str]  # skill_id -> description


class Skill(BaseModel):
    """Internal representation of a skill loaded from disk."""

    id: str
    description: str
    content: str
