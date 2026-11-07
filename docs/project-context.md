# Project Context

## Purpose and status

TechnoDev is a public, cloneable Python 3.12 starter for scripting, numerical
modeling, and notebook-based analytics. Each copy becomes a standalone project;
the removed generator is not required at runtime. Local development uses uv,
pytest, and Ruff. JupyterLab and container development are optional.

## Repository map

- `pyproject.toml`, `uv.lock`, `.python-version`: package metadata, dependencies,
  lockfile, and Python baseline.
- `src/project/`: reusable package logic.
- `scripts/`: runnable examples and the one-time package rename helper.
- `tests/`: package and starter workflow checks.
- `notebooks/`: optional synthetic-data analytics example.
- `README.md`: project introduction, quick start, and links to guides.
- `AGENTS.md`: concise, provider-independent engineering guidance.
- `docs/tutorial.md`: first-project setup, validation, and optional environments.
- `docs/python-development-design.md`: architecture and workflow decisions.
- `docs/task-template.md`: optional task brief.
- `Dockerfile`, `.dockerignore`, `.devcontainer/`: optional container setup.
- `.github/workflows/checks.yml`: locked checks and a built-wheel smoke test.
- `.github/dependabot.yml`: monthly GitHub Actions dependency update checks.

## Constraints

- Treat each clone as an independent project. Do not add a TechnoDev runtime,
  private service dependency, or AI-provider-specific setup.
- Use `pyproject.toml` and `uv.lock` for dependencies; avoid adding libraries to
  the starter without a current project need.
- Keep native local development as the default. The optional container shares the
  lockfile and uses `/opt/venv`; it does not reuse the host `.venv`.
- Keep notebooks optional and in the same project environment. Scientific and
  modeling libraries are chosen by each downstream project.
- Keep setup small; GPU, cloud deployment, and multi-service infrastructure are
  project-specific additions.

## Keeping this context current

When this repository is cloned into a real project, replace the purpose and map
with that project's actual structure, commands, inputs, and important constraints.
Record only facts that help future contributors understand or safely change it.
