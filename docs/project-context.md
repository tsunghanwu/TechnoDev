# Project Context

## Purpose

TechnoDev is a repository to clone for independent Python
scripting, modeling, and Jupyter notebook analytics projects, with an AI agent as
a pair programmer.

## Current state

The starter is implemented. The old generator has been removed. The repository
contains a setuptools package, uv manifest and lockfile, example script and
notebook, pytest/Ruff checks, GitHub Actions workflow, and optional Docker and
Dev Container configuration.

The layout and conventions are described in
[the development design](python-development-design.md). The [README](../README.md)
contains the current setup and run commands.

## Repository map

- `README.md`: entry point and current status.
- `AGENTS.md`: shared engineering and modeling instructions for agents.
- `pyproject.toml`, `uv.lock`, `.python-version`: package, dependency, and Python setup.
- `src/project/`: reusable package logic.
- `scripts/`, `tests/`, `notebooks/`: example entry point, optional rename helper, starter checks, and analytics example.
- `Dockerfile`, `.dockerignore`, `.devcontainer/`: optional container development.
- `.github/workflows/checks.yml`: locked CI checks including a built-wheel smoke test.\n- `.github/dependabot.yml`: monthly GitHub Actions update checks.
- `docs/python-development-design.md`: intended starter layout and workflow.
- `docs/tutorial.md`: hands-on guide to local development, notebooks, and Docker.
- `docs/project-context.md`: purpose, current structure, and constraints.
- `docs/task-template.md`: optional brief for substantial tasks.

## Decisions and constraints

- Each clone is independent; no project generator or TechnoDev runtime is needed. The optional rename helper only edits the freshly cloned starter in place.
- The baseline uses uv, pytest, Ruff, and a small installable Python package.
- Local development is the default. Optional Docker development shares dependency
  metadata and the lockfile while keeping its environment separate from the host.
  VS Code Dev Containers integration uses the same development image.
- The selectable `notebook` group includes JupyterLab and
  ipykernel, plus a small example notebook. Scientific libraries are chosen per
  project; notebook execution uses the same environment as scripts and tests.
- Modeling includes simulation, statistics, optimization, and machine learning;
  the starter does not assume a specific framework.
- Keep setup small and avoid adding abstractions for hypothetical future needs.
- GPU images, multi-service orchestration, and deployment setup remain specific
  to individual projects.

## Maintaining this document

After cloning, replace this context with the new project's purpose, actual code
map, implemented validation commands, and relevant modeling assumptions. Update
it as those facts change. Record meaningful design decisions here or link to a
separate decision document when detail is needed.
