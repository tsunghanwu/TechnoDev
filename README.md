# TechnoDev

TechnoDev is a lightweight Python starter for scripting, numerical modeling, and
Jupyter-based analytics. Each copy becomes a standalone project; it does not need
a TechnoDev runtime, private infrastructure, or a particular AI coding provider.

## What it includes

- Python 3.12 and a small installable package under `src/project/`.
- `uv` for environments and locked dependencies, with pytest and Ruff for checks.
- A runnable example, focused tests, and an optional JupyterLab dependency group.
- Optional Docker, VS Code Dev Containers, and GitHub Codespaces support.

## Get a copy and run it

This repository is not currently enabled as a GitHub template. Clone it, then
create a new empty remote repository and point the clone at that repository if
you want to publish your independent project. Cloning retains TechnoDev's Git
history:

```bash
git clone https://github.com/tsunghanwu/TechnoDev.git my_project
cd my_project
git remote set-url origin https://github.com/<your-user>/my_project.git
```

If the repository is enabled as a template in the future, **Use this template**
will create a new repository without TechnoDev's commit history. That option is
not available for this repository today.

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then run these commands
from the project root:

```bash
uv sync --locked
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

For the package rename, metadata and documentation updates, and optional notebook
or container setup, follow the [first-project tutorial](docs/tutorial.md).

## Documentation

- [Tutorial](docs/tutorial.md): ordered first-project setup and optional environments.
- [Project context](docs/project-context.md): current purpose, repository map, and constraints.
- [Development design](docs/python-development-design.md): architecture and workflow decisions.
- [AGENTS.md](AGENTS.md): concise provider-independent engineering guidance.
- [Task brief](docs/task-template.md): optional lightweight task specification.
