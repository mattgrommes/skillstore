"""Tests for skill loader."""

from pathlib import Path

from skillstore.skill_loader import SkillLoader


class TestSkillLoader:
    """Tests for SkillLoader class."""

    def test_load_all_empty_directory(self, tmp_path: Path) -> None:
        """Loading from empty directory returns empty dict."""
        loader = SkillLoader(tmp_path)
        skills = loader.load_all()
        assert skills == {}

    def test_load_all_nonexistent_directory(self, tmp_path: Path) -> None:
        """Loading from nonexistent directory returns empty dict."""
        loader = SkillLoader(tmp_path / "nonexistent")
        skills = loader.load_all()
        assert skills == {}

    def test_load_all_with_valid_skill(self, tmp_path: Path) -> None:
        """Loading directory with valid skill file returns the skill."""
        skill_file = tmp_path / "test-skill.md"
        skill_file.write_text(
            """---
description: A test skill for testing
---

# Test Skill

This is the content.
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.load_all()

        assert "test-skill" in skills
        assert skills["test-skill"].description == "A test skill for testing"
        assert "# Test Skill" in skills["test-skill"].content

    def test_load_all_skips_files_without_description(self, tmp_path: Path) -> None:
        """Files without description frontmatter are skipped."""
        skill_file = tmp_path / "no-desc.md"
        skill_file.write_text(
            """---
title: Missing description
---

Content here.
"""
        )

        loader = SkillLoader(tmp_path)
        skills = loader.load_all()

        assert skills == {}

    def test_load_all_skips_non_markdown_files(self, tmp_path: Path) -> None:
        """Non-markdown files are ignored."""
        (tmp_path / "readme.txt").write_text("Not a skill")
        (tmp_path / "config.json").write_text("{}")

        loader = SkillLoader(tmp_path)
        skills = loader.load_all()

        assert skills == {}

    def test_load_one_valid_skill(self, tmp_path: Path) -> None:
        """Loading a single skill by ID works."""
        skill_file = tmp_path / "my-skill.md"
        skill_file.write_text(
            """---
description: My skill description
---

# My Skill

Instructions here.
"""
        )

        loader = SkillLoader(tmp_path)
        skill = loader.load_one("my-skill")

        assert skill is not None
        assert skill.id == "my-skill"
        assert skill.description == "My skill description"
        assert "# My Skill" in skill.content

    def test_load_one_nonexistent_skill(self, tmp_path: Path) -> None:
        """Loading nonexistent skill returns None."""
        loader = SkillLoader(tmp_path)
        skill = loader.load_one("does-not-exist")

        assert skill is None

    def test_load_one_invalid_frontmatter(self, tmp_path: Path) -> None:
        """Skill with invalid frontmatter returns None."""
        skill_file = tmp_path / "bad-skill.md"
        skill_file.write_text("Just content, no frontmatter")

        loader = SkillLoader(tmp_path)
        skill = loader.load_one("bad-skill")

        # No description means it's invalid
        assert skill is None
