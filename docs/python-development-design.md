# Python Development Design

## Purpose and status

TechnoDev is a cloneable Python starter for scripting, numerical modeling, and
Jupyter-based analytics. Its baseline is implemented. A copy becomes an
independent project; it does not keep TechnoDev as a runtime dependency. The
[README](../README.md) introduces the starter, and the [tutorial](tutorial.md)
covers onboarding commands. This document records the design choices behind the
repository.

## Package and repository layout

```text
project/
├── pyproject.toml
├── uv.lock
├── .python-version
├── README.md
├── AGENTS.md
├── docs/
├── .github/workflows/checks.yml
├── src/project/
├── scripts/
├── notebooks/
└── tests/
```

Reusable code lives in an installable package under `src/<package>/`. The
setuptools `src` layout keeps imports explicit and avoids modifying `sys.path` or
setting `PYTHONPATH`. uv installs the package in editable mode for development.
Scripts remain thin entry points, tests exercise shared behavior, and notebooks
are for exploration rather than the only home of reusable logic.

The starter begins with one example package and no scientific runtime
dependencies. The rename helper changes the neutral package name in a fresh copy;
it is a one-time convenience, not a generator or initialization framework.

## Python and dependency workflow

- Python 3.12 is the baseline in `.python-version`, `requires-python`, Ruff, CI,
  and the container image.
- `pyproject.toml` is the source for package metadata and dependency groups;
  `uv.lock` records the resolved environment. Commit changes to both when
  dependencies change.
- The default `dev` group contains pytest and Ruff. JupyterLab and ipykernel live
  in the optional `notebook` group, so script-only users can omit them.
- uv is pinned in both CI and the Docker image to keep those environments
  consistent. Update the pins together when changing uv versions.

This keeps one dependency workflow across local, CI, and container use. Project
specific libraries are added only when the downstream project needs them.

## Validation and packaging

CI synchronizes the committed lockfile, runs pytest and Ruff, builds a wheel, and
imports that wheel in a clean environment. The wheel smoke test checks the
packaging boundary; normal development uses uv's editable install and does not
need to build a wheel. The starter tests also check package import and example
script behavior.

## Optional notebook workflow

Notebook tools share the project's environment and lockfile. The example notebook
uses synthetic data and package functions, so it does not require private inputs
or scientific libraries. Keep notebooks runnable in order, clear outputs before
committing by default, and store local inputs and generated outputs in ignored
`data/` and `outputs/` directories. Add numerical, plotting, dataframe, and
machine-learning libraries to individual projects only as needed.

## Optional container workflow

Native uv development is the default. The Dockerfile uses a Python 3.12 image and
the pinned uv version, while `.devcontainer/devcontainer.json` reuses that image
for VS Code Dev Containers and GitHub Codespaces. All environments consume the
same `pyproject.toml` and lockfile.

The container keeps its environment at `/opt/venv`, outside the mounted source
tree. This prevents reuse of a host `.venv` and lets editable installs point to
the mounted copy. The development user and optional host UID/GID build arguments
help keep mounted files usable on the host. Jupyter retains token authentication;
Docker instructions publish port 8888 only on host loopback.

Container use remains optional and shares the native dependency workflow. GPU
images, service orchestration, deployment infrastructure, and container-specific
CI are outside the starter's current scope.

## Modeling and reproducibility

- Pass input paths and parameters explicitly; record units, provenance, and
  assumptions when they affect a result.
- Use small deterministic fixtures for ordinary tests, with justified numerical
  tolerances. Keep large data, long training jobs, and GPU workloads out of
  baseline checks.
- Record random seeds and relevant parameters for repeatable experiments; a seed
  alone may not ensure identical results across libraries or hardware.
- Treat agent guidance as shared documentation. `AGENTS.md` stays concise and
  provider-independent; no agent SDK, API key, or private integration is required.

These are defaults for a lightweight starter. Downstream projects should adapt
them to their actual scientific and operational needs.
