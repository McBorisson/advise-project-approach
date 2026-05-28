#!/usr/bin/env python3
"""Validate source and packaged skill structure."""

from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "advise-project-approach"
SOURCE_DIR = ROOT / "skills" / SKILL_NAME
SKILL_FILE = SOURCE_DIR / "SKILL.md"
AGENT_FILE = SOURCE_DIR / "agents" / "openai.yaml"
PACKAGE_FILE = ROOT / "dist" / f"{SKILL_NAME}.skill"
EXPECTED_PACKAGE_FILES = {
    f"{SKILL_NAME}/SKILL.md",
    f"{SKILL_NAME}/agents/openai.yaml",
}


def fail(message: str) -> None:
    raise SystemExit(f"Validation failed: {message}")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")

    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            fail(f"Invalid frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_source() -> None:
    if not SOURCE_DIR.is_dir():
        fail(f"Missing source directory: {SOURCE_DIR.relative_to(ROOT)}")
    if not SKILL_FILE.is_file():
        fail("Missing skills/advise-project-approach/SKILL.md")
    if not AGENT_FILE.is_file():
        fail("Missing skills/advise-project-approach/agents/openai.yaml")

    extra_skill_files = {
        path.relative_to(SOURCE_DIR).as_posix()
        for path in SOURCE_DIR.rglob("*")
        if path.is_file()
    } - {"SKILL.md", "agents/openai.yaml"}
    if extra_skill_files:
        fail(f"Unexpected files inside skill package: {sorted(extra_skill_files)}")

    text = SKILL_FILE.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    allowed_fields = {"name", "description"}
    extra_fields = set(fields) - allowed_fields
    missing_fields = allowed_fields - set(fields)
    if missing_fields:
        fail(f"Missing frontmatter fields: {sorted(missing_fields)}")
    if extra_fields:
        fail(f"Unexpected frontmatter fields: {sorted(extra_fields)}")
    if fields["name"] != SKILL_NAME:
        fail("Frontmatter name must match skill folder name")
    if len(fields["description"]) > 1024:
        fail("Frontmatter description must be 1024 characters or fewer")


def validate_package() -> None:
    if not PACKAGE_FILE.is_file():
        fail(f"Missing package: {PACKAGE_FILE.relative_to(ROOT)}")
    with ZipFile(PACKAGE_FILE) as archive:
        names = {name for name in archive.namelist() if not name.endswith("/")}
    if names != EXPECTED_PACKAGE_FILES:
        fail(
            "Package contents differ from expected files: "
            f"expected {sorted(EXPECTED_PACKAGE_FILES)}, got {sorted(names)}"
        )


def main() -> None:
    validate_source()
    validate_package()
    print("Skill package is valid.")


if __name__ == "__main__":
    main()
