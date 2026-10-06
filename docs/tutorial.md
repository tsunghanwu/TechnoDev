# TechnoDev starter tutorial

This tutorial walks through the starter from a fresh checkout: install its tools,
run the example, follow the package logic into a test, open the notebook, and
optionally use Docker. Commands below run from the repository root unless stated
otherwise.

## 1. Set up the local environment

Install Python 3.12 and [uv](https://docs.astral.sh/uv/). In the repository,
create the project environment and install the locked development dependencies:

```bash
uv sync --locked
```

uv creates `.venv/` and installs the package in editable mode. Editable mode means
changes under `src/project/` are immediately available to scripts, tests, and
notebooks. The environment directory is ignored by Git.

Run the example script:

```bash
uv run --locked python scripts/example.py
```

It prints the mean of three sample values. `uv run` uses this repository's
environment, so there is no need to activate `.venv` manually.

## 2. Turn TechnoDev into your project

A fresh clone still uses the neutral `project` package name. If you want a
project-specific package name, run the one-time rename helper before building out
the project:

```bash
uv run python scripts/rename_project.py my_project
uv lock
uv sync --locked
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

Use a lowercase snake_case package name. The helper updates the distribution
name, package directory, example script, and tests. Review the resulting diff,
then update `README.md` and `docs/project-context.md` with the real project's
purpose, structure, inputs, and constraints. Review `AGENTS.md` too, adding
project-specific engineering or modeling guidance only when it is genuinely
shared across tasks.

## 3. Find the shared project logic

The script imports `mean` from `src/project/__init__.py`. This package is where
reusable calculations and transformations belong. Keep scripts as small entry
points that gather inputs, call package functions, and present results.

The `mean` function accepts any iterable of numbers, counts values as it reads
them, and raises `ValueError` when the input is empty. Those details are tested
in `tests/test_example.py`. Run the test suite with:

```bash
uv run --locked pytest
```

When adding package behavior, put its test beside the related tests. For scientific
work, make units, assumptions, parameters, and tolerances explicit; use small,
deterministic examples for routine tests.

## 4. Run the project checks

The development group contains pytest and Ruff. Run the same checks used by CI:

```bash
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

If Ruff reports formatting changes, apply them with `uv run ruff format .`, then
review the diff. CI runs these checks after installing the committed lockfile.

## 5. Add a dependency

Add a runtime library to the project with:

```bash
uv add <library-name>
```

For a tool used only during development, use:

```bash
uv add --dev <tool-name>
```

uv updates both `pyproject.toml` and `uv.lock`. Commit both files together so
other developers and CI can reproduce the environment. The starter has no
scientific runtime dependencies; select numerical, plotting, data, or machine
learning libraries based on the actual project.

## 6. Work with the example notebook

Install the optional notebook dependencies and launch JupyterLab from the root:

```bash
uv sync --locked --group notebook
uv run --locked --group notebook jupyter lab
```

Open `notebooks/example.ipynb` and select the Python kernel from this project's
`.venv`. Its measurements are synthetic, and its code imports the same `mean`
function used by the script. Keep reusable logic in `src/project/`, not only in
notebook cells. Run cells in order from a fresh kernel and clear outputs before
committing by default.

The notebook group is optional. A script-only checkout can use `uv sync --locked`
without installing JupyterLab and ipykernel.

## 7. Keep local files out of Git

Put local input data under `data/` and generated figures, results, and model
artifacts under `outputs/`. Their contents are ignored by default. Commit small,
approved test fixtures under `tests/fixtures/` when a test needs them. Do not put
credentials or private datasets in the repository.

## 8. Work with an AI coding agent

TechnoDev keeps agent guidance in the repository so the same workflow can be
used with different coding agents. Before a substantial task, have the agent
read `AGENTS.md`, `docs/project-context.md`, and the relevant implementation
or design files.

A useful first task is a small numerical change, for example:

```text
Add an RMSE function for measured and predicted values. Follow AGENTS.md,
make numerical assumptions explicit, add focused tests, run the applicable
project checks, and report the validation that actually ran.
```

For non-trivial work, the intended loop is: understand the existing project,
present a concise plan, implement a focused change, validate it, and report the
changed behavior, assumptions, checks, and remaining risks. Use
`docs/task-template.md` when a task needs explicit goals, constraints, or
acceptance criteria.

Keep provider-specific authentication and machine settings outside the
repository. The committed guidance should remain useful whether the agent runs
locally, in an editor, or through another development environment.

## 9. Use Docker instead (optional)

Docker uses the same `pyproject.toml` and `uv.lock`; its environment lives at
`/opt/venv`, outside the mounted repository. On Linux, build with your user and
group IDs so files created in the mount remain editable by your account:

```bash
docker build --build-arg USER_ID="$(id -u)" --build-arg GROUP_ID="$(id -g)" -t technodev .
docker run --rm -it -v "$PWD:/workspace" -w /workspace technodev
```

Inside the container, synchronize after the repository is mounted. This installs
the package from the mounted workspace:

```bash
uv sync --locked --group dev --group notebook
uv run --locked python scripts/example.py
uv run --locked pytest
```

To run JupyterLab, start a separate container and publish the port only on local
loopback:

```bash
docker run --rm -it -p 127.0.0.1:8888:8888 -v "$PWD:/workspace" -w /workspace technodev \
  uv run --locked --group notebook jupyter lab --ip=0.0.0.0 --no-browser
```

Use the URL and token printed in the logs. Stop with Ctrl-C; the container is
removed, while repository files remain on the host. Rebuild after Dockerfile or
system dependency changes, and synchronize after dependency or lockfile changes.
For VS Code, open the repository and choose **Reopen in Container**.

## 8. Start an independent project

Clone this repository, then give the clone its own Git remote and project name.
Rename the neutral `project` distribution in `pyproject.toml` and the Python
package directory under `src/`; update imports and tests, then run `uv lock` to
refresh the lockfile. Update `README.md`, `AGENTS.md`, and
`docs/project-context.md` so they describe the new project's purpose and actual
commands. Use the [task brief](task-template.md) when an agent needs more context
for a substantial change.


## 10. Recommended daily workflow

Start work by synchronizing the committed environment when dependencies may have
changed:

```bash
uv sync --locked
```

During development, run the relevant script, focused test, or notebook first.
Before committing a normal code change, run the project checks:

```bash
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

Add dependencies through uv rather than installing them directly into the
environment. Keep reusable logic under the package, use scripts and notebooks
for orchestration and exploration, and update project context when the project's
purpose, structure, workflow, or important modeling assumptions change.
