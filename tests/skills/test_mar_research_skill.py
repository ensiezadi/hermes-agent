"""Smoke tests for the mar-research optional skill.

These tests keep the new workflow skeleton aligned with Hermes skill
conventions without exercising any networked or model-backed behavior.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


SKILL_DIR = Path(__file__).resolve().parents[2] / "optional-skills" / "autonomous-ai-agents" / "mar-research"


@pytest.fixture(scope="module")
def frontmatter() -> dict:
    src = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", src, re.DOTALL)
    assert m, "SKILL.md missing YAML frontmatter"
    return yaml.safe_load(m.group(1))


def test_skill_dir_exists() -> None:
    assert SKILL_DIR.is_dir(), f"missing skill dir: {SKILL_DIR}"


def test_skill_md_present() -> None:
    assert (SKILL_DIR / "SKILL.md").is_file()


def test_description_under_60_chars(frontmatter) -> None:
    desc = frontmatter["description"]
    assert len(desc) <= 60, f"description is {len(desc)} chars (hardline ≤60): {desc!r}"


def test_name_matches_dir(frontmatter) -> None:
    assert frontmatter["name"] == "mar-research"


def test_skill_mentions_controller_and_judge() -> None:
    src = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "Judge" in src
    assert "state/research_state.yaml" in src
    assert "decision_log.md" in src


def test_prompt_files_exist() -> None:
    assert (SKILL_DIR / "prompts" / "controller.md").is_file()
    assert (SKILL_DIR / "prompts" / "judge.md").is_file()


def test_state_templates_exist() -> None:
    assert (SKILL_DIR / "state" / "research_state.yaml").is_file()
    assert (SKILL_DIR / "state" / "current_task.md").is_file()
    assert (SKILL_DIR / "state" / "decision_log.md").is_file()
