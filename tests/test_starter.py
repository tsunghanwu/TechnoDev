"""Starter-level smoke tests."""

from pathlib import Path
import subprocess
import sys


def test_package_imports_from_installed_environment() -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import project; print(project.__file__)"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "src/project" in result.stdout.replace("\\", "/")


def test_example_script_runs() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "example.py")],
        check=True,
        capture_output=True,
        text=True,
        cwd=root,
    )
    assert result.stdout.strip() == "2.0"
