# Cloneable Python Development Starter

## Direction and status

TechnoDev should be the repository you clone to begin an independent Python
project, primarily for scripting, modeling, and notebook-based data analytics.
The previous project generator and multi-language design have been removed.
The baseline, notebook workflow, optional container setup, and CI are implemented
in this repository. Commands and limitations are documented in the README.

The reusable product is the development setup: environment, dependency workflow,
code layout, checks, and concise instructions. Each clone evolves independently.

## Baseline

- Use `pyproject.toml` for package metadata, runtime dependencies, development
  dependencies, and tool configuration.
- Use uv for environment setup and dependency locking. Commit `uv.lock`; keep
  `.venv/` local. A `dev` dependency group contains pytest and Ruff.
- Record Python 3.12 in `.python-version`. Keep the Python requirement, Ruff target,
  and CI interpreter consistent when changing the baseline.
- Keep an installable package under `src/project/`, using the existing setuptools
  backend. Editable installation lets scripts, tests, and notebooks share imports
  without modifying `sys.path` or setting `PYTHONPATH`.
- Start with no scientific runtime dependencies. Add the libraries actually used
  by each project; modeling may mean numerical simulation, statistics, optimization,
  or machine learning, and does not imply one particular framework.
- Include JupyterLab and ipykernel in a selectable `notebook` dependency group,
  sharing the project's environment and lockfile. Script-only projects can omit
  installation of this group.
- Keep local uv development as the default. Include optional Docker development
  using the same dependency metadata and lockfile, with VS Code Dev Containers
  integration for users of that editor.

uv's [project guide](https://docs.astral.sh/uv/guides/projects/) describes the
committed lockfile workflow. Its
[dependency documentation](https://docs.astral.sh/uv/concepts/dependencies/)
describes development groups and explicitly selected optional groups.

## Layout

```text
project/
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── .dockerignore
├── Dockerfile
├── .devcontainer/
│   └── devcontainer.json
├── README.md
├── AGENTS.md
├── docs/
│   ├── project-context.md
│   └── task-template.md
├── .github/workflows/checks.yml
├── src/project/
│   └── __init__.py
├── scripts/
│   └── example.py
├── notebooks/
│   └── example.ipynb
└── tests/
    └── test_example.py
```

Container files support an optional workflow; local development does not require
Docker or VS Code. This tree describes the current starter layout.

`project` is a neutral starter package name. The README explains how to rename the
distribution and import package, update imports, and refresh the lockfile. No
generator or custom initialization command is necessary.

Scripts are thin entry points with a main guard. Shared transformations,
calculations, and model logic belong in the package. Start with one small runnable
example and a meaningful test, rather than creating speculative modules.

Add these directories when a project needs them:

| Directory | Purpose | Version control |
| --- | --- | --- |
| `data/` | Local input data and intermediate datasets | Ignore contents by default |
| `outputs/` | Generated figures, results, and model artifacts | Ignore contents by default |
| `configs/` | Experiment or script parameters | Commit nonsecret configuration |

Small test fixtures belong under `tests/fixtures/` and can be committed. Document
how real input data is obtained instead of including it in the starter. Deliberately
add selected final figures or reports when they are useful project deliverables.

## Daily workflow

Run the implemented local workflow with:

```bash
uv sync --locked
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

Use `uv add <library>` for runtime dependencies and `uv add --dev <tool>` for
development tools. Dependency changes update both metadata and the lockfile.
Use `uv run ruff format .` to apply formatting intentionally.

CI installs the recorded uv tool version, uses `uv sync --locked`, and runs the
same three checks as local development. Begin with the default interpreter;
expand the matrix only if the project needs compatibility across Python versions.

## Jupyter notebook workflow

Include `notebooks/example.ipynb` with a small, dependency-light analytics example
using synthetic data and a function imported from the project package. Keep its
outputs empty in Git. This demonstrates shared imports without requiring a
download or a private dataset. JupyterLab is the interface for editing
standard `.ipynb` notebooks.

The notebook dependency group is declared in `pyproject.toml` and included in
`uv.lock`:

```bash
uv add --group notebook jupyterlab ipykernel
```

Launch from the repository root:

```bash
uv sync --locked --group notebook
uv run --locked --group notebook jupyter lab
```

Select the kernel from the project's `.venv` and verify its interpreter if imports
fail. Do not use a global kernel or install packages inside notebook cells. Add
analytics dependencies through the project dependency workflow; keep the choice
of dataframe, plotting, and numerical libraries specific to the project.
See the [uv Jupyter guide](https://docs.astral.sh/uv/guides/integration/jupyter/)
for environment and kernel integration details.

Notebook conventions:

- Begin with the analytical question, input provenance, assumptions, and parameters.
- Keep cells runnable in order from a fresh kernel. Move reusable cleaning,
  calculations, and modeling functions into `src/project/` and test them there.
- State the notebook's working-directory convention and resolve data paths
  explicitly; do not hard-code a developer's filesystem paths.
- Keep local inputs in ignored `data/` and generated artifacts in ignored
  `outputs/`. Ignore `.ipynb_checkpoints/`, but track notebook source files.
- Clear outputs and execution counts before committing by default. For an
  intentional report, review retained outputs and explain any exception.

Validate a changed notebook using JupyterLab's
[restart kernel and run all cells](https://jupyterlab.readthedocs.io/en/stable/user/commands_list.html)
command with small approved inputs. Review plots and conclusions explicitly;
passing pytest or Ruff does not prove that a notebook executed successfully.
Baseline CI runs package checks. The example notebook can be executed locally with
`uv run --locked --group notebook jupyter nbconvert --to notebook --execute notebooks/example.ipynb`;
data-dependent
or expensive notebooks need separate validation rather than automatic execution
of every notebook.

## Optional container development

Provide one development `Dockerfile` and `.dockerignore`. Use a versioned Linux
Python base image matching the default interpreter, a pinned uv version, and a
non-root development user. Use the existing `pyproject.toml` and `uv.lock` with
locked synchronization; include the `notebook` group for the notebook workflow.
Follow the [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/)
for dependency installation and environment placement.

Keep the container environment outside the mounted source tree, for example at
`/opt/venv`, and configure uv to use it. Do not mount or copy the host `.venv` into
the container. Synchronize after mounting the repository so editable package
imports reference the active workspace. Document rebuilding for system dependency
changes and resynchronizing for lockfile changes.

Mount the repository at a documented workspace path so source edits, notebooks,
local data, and generated outputs persist on the host. Support host-compatible
file ownership on Linux. Exclude Git metadata, environments, credentials, notebook
checkpoints, datasets, and generated artifacts from the image build context.
Document optional mounts for input data kept outside the repository.

Provide documented Docker build/run examples for an interactive shell, package
checks, and JupyterLab. Jupyter listens on the container interface at port 8888;
publish that port only on the host loopback address and retain token authentication.
Use the container environment as the notebook kernel. Explain where to find the
Jupyter URL/token and how to stop the container without losing mounted work.
Finalize and test exact commands when the Dockerfile exists.

Add `.devcontainer/devcontainer.json` referencing the same Dockerfile and environment,
with the Python and Jupyter editor extensions and port 8888 forwarding. It should
select the container interpreter and synchronize locked dependencies after the
workspace is mounted. Docker CLI usage must remain available independently of
VS Code. See [Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers).

Agents can run authorized checks inside the development container. Repository
mounts remain writable host files; container use does not authorize additional
filesystem access. Keep agent authentication local to the chosen tool and out of
the image. Do not mount the Docker socket or broad home directories by default.
[Docker's bind-mount documentation](https://docs.docker.com/engine/storage/bind-mounts/)
explains host filesystem access through mounts.

Keep GPU/CUDA images, external services, Compose orchestration, deployment images,
and container-specific CI jobs as project-specific additions. The baseline CI
continues running the native locked checks; validate the development container
separately when its configuration changes.

## Modeling conventions

- Pass input paths and parameters explicitly rather than embedding machine-specific
  paths in code. State whether relative paths resolve from the working directory.
- Record parameters, input provenance, dependency lock revision, and random seeds
  for experiments that need to be repeatable. A seed alone does not guarantee
  identical results across hardware and libraries.
- Test small deterministic calculations, shape and unit assumptions, and important
  numerical edge cases. Use justified tolerances for floating-point assertions.
- Keep long training runs, large datasets, and GPU requirements outside baseline
  tests. Add separate integration or experiment checks when needed.
- Document required native tools or hardware in the individual project's README.

## AI pair-programming setup

Commit shared guidance in `AGENTS.md`, a concise project map and constraints in
`docs/project-context.md`, and an optional task brief in `docs/task-template.md`.
These files are already present; revise them for each new clone. Keep instructions
independent of the agent provider. If an agent does not automatically load
`AGENTS.md`, explicitly direct it to read the file. Add provider-specific settings
only when needed and refer back to the shared guidance instead of duplicating it.

Keep the existing engineering principles in `AGENTS.md`. As the starter is
implemented, add the actual code locations, uv workflow, and modeling conventions.
README covers cloning, creating an independent Git remote, renaming, setup,
running scripts, checks, notebooks, and optional container development.
Avoid duplicating a large architecture document
in every future project.

An ordinary session starts with the agent reading instructions and context, then
inspecting relevant files. Give it a goal and acceptance criteria; use the task
brief for substantial changes. The agent presents a proportional plan, implements
focused changes, runs applicable checks, and reports the diff and actual results.
Human review evaluates the outcome, including scientific assumptions and model
quality that passing code checks alone cannot establish.

For modeling tasks, identify input provenance, units, parameters, random seeds,
evaluation splits, and expected numerical tolerances where applicable. Use small
fixtures for routine checks. Agree on compute budgets before expensive experiments;
report experiment results separately from tests and linting. Keep credentials and
private data out of external uploads unless explicitly authorized.

The starter does not require an AI SDK or API key. Authentication belongs to the
chosen agent's local setup. Do not commit credentials or machine-specific agent
settings. Add reusable agent skills or integrations only for a demonstrated need.

Upstream starter improvements are adopted through small reviewed changes. Clones
do not automatically synchronize files or require TechnoDev as a dependency.

## Implementation plan and acceptance criteria

1. **Python baseline:** choose the default Python version, create the neutral
   package and example script, configure uv, pytest, and Ruff, and generate a real
   lockfile. Add a meaningful test of shared logic. Accept when a fresh copy can
   synchronize locked dependencies, run the script, import the package without
   path workarounds, and pass tests, lint, and formatting checks.
2. **Notebook analytics:** configure the `notebook` group and create a small
   synthetic-data notebook sharing package logic. Accept when Jupyter launches
   with the project kernel and the example runs in order from a fresh kernel.
   Review outputs and execution counts and verify checkpoint/data/artifact ignores.
3. **Optional containers:** add the development Dockerfile, build exclusions,
   and Dev Container configuration. Accept when a clean build can run the script,
   package checks, and example notebook; host edits and outputs survive container
   recreation; the host environment is not reused; and generated files have usable
   ownership. Verify loopback-only Jupyter access and token authentication. Check
   VS Code opening and interpreter selection where that tooling is available.
4. **CI and documentation:** add native locked checks to CI and rewrite README,
   project context, and agent guidance around the implemented commands. Document
   clone/rename steps, prerequisites, environment selection, notebook setup, and
   Docker build/run/rebuild instructions. Accept when local and CI commands agree
   and documentation describes actual files and tested workflows.
5. **Pair-programming validation:** exercise a small scripting or numerical
   change with an agent. Accept when it can find shared logic, make a focused
   change, run applicable checks in the selected environment, and accurately
   report assumptions, results, and unrun checks. Review a notebook edit for
   unrelated cell or metadata changes.

Report unavailable Docker, editor, notebook, or agent integration checks explicitly
rather than marking them passed. Do not add scientific dependencies or execute
expensive experiments just to validate the starter.

Success means a fresh clone supports scripts and notebook analytics with useful
agent guidance, offers a validated optional container environment, and can add
modeling dependencies without restructuring or depending on the old generator.
