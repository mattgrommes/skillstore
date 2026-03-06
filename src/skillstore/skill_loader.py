"""Skill loader - reads skill files from disk and parses frontmatter."""

from pathlib import Path

import frontmatter

from skillstore.models import Skill


class SkillLoader:
    """Loads skills from a directory of markdown files with YAML frontmatter."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir

    def load_all(self) -> dict[str, Skill]:
        """Load all skills from the skills directory.

        Returns:
            Dictionary mapping skill_id to Skill object.
        """
        skills: dict[str, Skill] = {}

        if not self.skills_dir.exists():
            return skills

        for path in self.skills_dir.glob("*.md"):
            skill = self._load_skill(path)
            if skill:
                skills[skill.id] = skill

        return skills

    def load_one(self, skill_id: str) -> Skill | None:
        """Load a single skill by ID.

        Args:
            skill_id: The skill identifier (filename without extension).

        Returns:
            Skill object if found, None otherwise.
        """
        path = self.skills_dir / f"{skill_id}.md"
        if not path.exists():
            return None
        return self._load_skill(path)

    def _load_skill(self, path: Path) -> Skill | None:
        """Parse a skill file and extract frontmatter + content.

        Args:
            path: Path to the markdown file.

        Returns:
            Skill object if valid, None if parsing fails.
        """
        try:
            post = frontmatter.load(path)
            description = post.get("description", "")
            if not description:
                return None

            return Skill(
                id=path.stem,
                description=description,
                content=post.content,
            )
        except Exception:
            return None
