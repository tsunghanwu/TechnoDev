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

    for path in (
        root / "pyproject.toml",
        root / "scripts" / "example.py",
        root / "tests" / "test_example.py",
    ):
        replace_text(path, "project", args.name)

    source.rename(target)
    print(f"Renamed starter package to {args.name}.")
    print("Run 'uv lock' and then the project checks.")


if __name__ == "__main__":
    main()
