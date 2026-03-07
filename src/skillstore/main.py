"""FastAPI application for Skillstore."""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from skillstore.fake_api import router as fake_api_router
from skillstore.models import SkillstoreResponse
from skillstore.skill_loader import SkillLoader

app = FastAPI(
    title="Skillstore",
    description="API for exposing discoverable LLM skills",
    version="0.1.0",
)

# Include fake gym API for testing/demo
app.include_router(fake_api_router)

# Skills directory - configurable via SKILLSTORE_SKILLS_DIR env var
# Defaults to ./skills relative to cwd for development
SKILLS_DIR = Path(os.environ.get("SKILLSTORE_SKILLS_DIR", "./skills"))

# Canonical site URL - configurable via SKILLSTORE_SITE_URL env var
# If not set, will use request.base_url (less secure but convenient for dev)
SITE_URL = os.environ.get("SKILLSTORE_SITE_URL", "")


def get_loader() -> SkillLoader:
    """Get the skill loader instance."""
    return SkillLoader(SKILLS_DIR)


@app.get("/skillstore", response_model=SkillstoreResponse)
async def list_skills(request: Request) -> SkillstoreResponse:
    """List all available skills for this site.

    Returns a dictionary of skill IDs to descriptions.
    """
    loader = get_loader()
    skills = loader.load_all()

    # Use configured site URL if set, otherwise fall back to request base_url
    # Production deployments should always set SKILLSTORE_SITE_URL
    if SITE_URL:
        site = SITE_URL.rstrip("/")
    else:
        site = str(request.base_url).rstrip("/")

    return SkillstoreResponse(
        site=site,
        skills={skill_id: skill.description for skill_id, skill in skills.items()},
    )


@app.get("/skillstore/skill/{skill_id}", response_class=PlainTextResponse)
async def get_skill(skill_id: str) -> str:
    """Download a specific skill by ID.

    Returns the full raw markdown content of the skill including frontmatter.
    """
    loader = get_loader()
    content = loader.load_raw(skill_id)

    if not content:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")

    return content
