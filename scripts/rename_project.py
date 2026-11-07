"""Rename the neutral starter package after cloning TechnoDev."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PACKAGE_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


def replace_text(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    updated = text.replace(old, new)
    if updated != text:
        path.write_text(updated)


def replace_distribution_name(path: Path, new_name: str) -> bool:
    lines = path.read_text().splitlines(keepends=True)
    in_project_table = False
    for index, line in enumerate(lines):
        table = line.strip()
        if table.startswith("[") and table.endswith("]"):
            in_project_table = table == "[project]"
            continue
        if not in_project_table or not re.match(r"^[ \t]*name[ \t]*=", line):
            continue

        match = re.fullmatch(
            r"([ \t]*name[ \t]*=[ \t]*)(['\"])project\2"
            r"([ \t]*(?:#.*)?)(\r?\n?)",
            line,
        )
        if match is None:
            return False
        lines[index] = (
            f"{match.group(1)}{match.group(2)}{new_name}{match.group(2)}"
            f"{match.group(3)}{match.group(4)}"
        )
        path.write_text("".join(lines))
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename the starter distribution and import package."
    )
    parser.add_argument("name", help="New Python import/package name (snake_case).")
    args = parser.parse_args()

    if not PACKAGE_NAME.fullmatch(args.name):
        parser.error("name must be a valid lowercase snake_case Python package name")
    if args.name == "project":
        parser.error("name is already 'project'")

    root = Path(__file__).resolve().parents[1]
    source = root / "src" / "project"
    target = root / "src" / args.name
    if not source.is_dir():
        parser.error("src/project was not found; this starter may already be renamed")
    if target.exists():
        parser.error(f"{target.relative_to(root)} already exists")

    manifest = root / "pyproject.toml"
    if not replace_distribution_name(manifest, args.name):
        parser.error('pyproject.toml must declare [project].name = "project"')

    for path in (
        root / "scripts" / "example.py",
        root / "tests" / "test_example.py",
        root / "tests" / "test_starter.py",
        root / "notebooks" / "example.ipynb",
        root / ".github" / "workflows" / "checks.yml",
    ):
        replace_text(path, "project", args.name)

    source.rename(target)
    print(f"Renamed starter package to {args.name}.")
    print("Run 'uv lock' and then the project checks.")


if __name__ == "__main__":
    main()
