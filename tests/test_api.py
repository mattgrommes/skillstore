"""Tests for Skillstore API endpoints."""

from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from skillstore.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def skills_dir(tmp_path: Path) -> Path:
    """Create a temporary skills directory with test skills."""
    skills = tmp_path / "skills"
    skills.mkdir()

    (skills / "class-schedule.md").write_text(
        """---
description: View the class schedule
---

# Class Schedule

Call GET /api/classes to see available classes.
"""
    )

    (skills / "book-appointment.md").write_text(
        """---
description: Book gym appointments
---

# Book Appointment

Call POST /api/bookings to book a class.
"""
    )

    return skills


class TestListSkills:
    """Tests for GET /skillstore endpoint."""

    def test_list_skills_returns_all_skills(
        self, client: TestClient, skills_dir: Path
    ) -> None:
        """Listing skills returns all available skills."""
        with patch("skillstore.main.SKILLS_DIR", skills_dir):
            response = client.get("/skillstore")

        assert response.status_code == 200
        data = response.json()

        assert "site" in data
        assert "skills" in data
        assert "class-schedule" in data["skills"]
        assert "book-appointment" in data["skills"]
        assert data["skills"]["class-schedule"] == "View the class schedule"

    def test_list_skills_empty_directory(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        """Listing skills from empty directory returns empty skills dict."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        with patch("skillstore.main.SKILLS_DIR", empty_dir):
            response = client.get("/skillstore")

        assert response.status_code == 200
        data = response.json()
        assert data["skills"] == {}


class TestGetSkill:
    """Tests for GET /skillstore/skill/{skill_id} endpoint."""

    def test_get_skill_returns_content(
        self, client: TestClient, skills_dir: Path
    ) -> None:
        """Getting a skill returns its markdown content."""
        with patch("skillstore.main.SKILLS_DIR", skills_dir):
            response = client.get("/skillstore/skill/class-schedule")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert "# Class Schedule" in response.text
        assert "GET /api/classes" in response.text

    def test_get_skill_not_found(
        self, client: TestClient, skills_dir: Path
    ) -> None:
        """Getting nonexistent skill returns 404."""
        with patch("skillstore.main.SKILLS_DIR", skills_dir):
            response = client.get("/skillstore/skill/nonexistent")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_skill_strips_frontmatter(
        self, client: TestClient, skills_dir: Path
    ) -> None:
        """Skill content should not include YAML frontmatter."""
        with patch("skillstore.main.SKILLS_DIR", skills_dir):
            response = client.get("/skillstore/skill/class-schedule")

        assert response.status_code == 200
        # Frontmatter should be stripped
        assert "---" not in response.text
        assert "description:" not in response.text
