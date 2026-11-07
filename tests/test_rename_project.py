"""Tests for the one-time starter package rename."""

import json
import subprocess
import sys
import tomllib
from pathlib import Path


def test_rename_updates_package_references_and_preserves_manifest(
    tmp_path: Path,
) -> None:
    root = tmp_path / "starter"
    helper = Path(__file__).resolve().parents[1] / "scripts" / "rename_project.py"
    (root / "src" / "project").mkdir(parents=True)
    for directory in ("scripts", "tests", "notebooks", ".github/workflows"):
        (root / directory).mkdir(parents=True, exist_ok=True)

    (root / "scripts" / "rename_project.py").write_text(helper.read_text())
    (root / "pyproject.toml").write_text(
        '[build-system]\nrequires = ["setuptools>=68"]\n'
        'build-backend = "setuptools.build_meta"\n\n'
        '[project]\nname = "project"\nversion = "0.1.0"\n'
        'description = "A project starter"\nrequires-python = ">=3.12"\n'
        'dependencies = []\n\n[tool.example]\nname = "project"\n'
    )
    (root / "scripts" / "example.py").write_text("from project import mean\n")
    (root / "tests" / "test_example.py").write_text("from project import mean\n")
    (root / "tests" / "test_starter.py").write_text(
        'import project\nassert "src/project" in project.__file__\n'
    )
    (root / "notebooks" / "example.ipynb").write_text(
        json.dumps({"cells": [{"source": ["from project import mean\n"]}]})
    )
    (root / ".github" / "workflows" / "checks.yml").write_text(
        'run: python -c "import project"\n'
    )

    subprocess.run(
        [sys.executable, str(root / "scripts" / "rename_project.py"), "my_project"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = tomllib.loads((root / "pyproject.toml").read_text())
    assert manifest["project"]["name"] == "my_project"
    assert manifest["project"]["description"] == "A project starter"
    assert manifest["tool"]["example"]["name"] == "project"
    assert (root / "src" / "my_project").is_dir()

    for relative_path in (
        "scripts/example.py",
        "tests/test_example.py",
        "tests/test_starter.py",
        "notebooks/example.ipynb",
        ".github/workflows/checks.yml",
    ):
        content = (root / relative_path).read_text()
        assert "from project import" not in content
        assert "import project" not in content
        assert "src/project" not in content
