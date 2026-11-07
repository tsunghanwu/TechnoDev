# First-project tutorial

Follow these steps to turn a fresh TechnoDev copy into an independent Python
project. Run commands from the repository root unless stated otherwise.

## 1. Get a fresh copy

TechnoDev is not currently enabled as a GitHub template, so clone it:

```bash
git clone https://github.com/tsunghanwu/TechnoDev.git my_project
cd my_project
```

Cloning retains TechnoDev's commit history. To make this a separately hosted
project, first create an empty repository on your Git hosting service, then point
`origin` at it:

```bash
git remote set-url origin https://github.com/<your-user>/my_project.git
```

If GitHub's **Use this template** option is enabled for TechnoDev in the future,
it will create a new repository without the starter's commit history. That option
is not available for this repository today.

## 2. Install the local development environment

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then synchronize the
committed development dependencies:

```bash
uv sync --locked
```

uv creates `.venv/` and installs the package in editable mode. Scripts, tests,
and notebooks can import it without activating the environment or setting
`PYTHONPATH`.

## 3. Rename the starter package

The starter uses the neutral Python package name `project`. If you want a
project-specific package, run the existing one-time helper with a lowercase
snake_case name:

```bash
uv run --locked python scripts/rename_project.py my_project
uv lock
uv sync --locked
```

The helper updates the distribution name, package directory, example script, and
both starter tests. It edits only this copy; it is not a generator or runtime
dependency. If you keep the `project` name, skip this step.

## 4. Update project metadata and documentation

Review `pyproject.toml` and replace the generic project description with one for
your work. The helper has already changed the distribution and package names;
keep the Python 3.12 baseline unless the project has a concrete compatibility
requirement.

Rewrite `README.md` to explain the project's purpose, setup, inputs, outputs, and
main commands. Update `docs/project-context.md` and `AGENTS.md` to describe the
actual code and shared engineering constraints. Keep the guidance
provider-independent. The development design can remain as starter reference
unless the project's architecture intentionally changes; `docs/task-template.md`
is optional.

## 5. Run the example and checks

Run the example, tests, and formatting checks from the repository root:

```bash
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The example prints the mean of three values. Shared calculations belong in the
package, while scripts remain thin entry points. Add runtime dependencies with
`uv add <library>` and development tools with `uv add --dev <tool>`; uv updates
`pyproject.toml` and `uv.lock` together.

## 6. Optionally use JupyterLab

The notebook dependency group is optional. Install it and launch JupyterLab from
the repository root when you need notebooks:

```bash
uv sync --locked --group notebook
uv run --locked --group notebook jupyter lab
```

Select the Python kernel from this project's `.venv`. The example notebook uses
synthetic data and imports shared package logic. Keep local inputs under ignored
`data/`, generated results under ignored `outputs/`, and clear notebook outputs
before committing by default.

## Optional Docker, Dev Containers, and Codespaces

Local uv development is the default; containers are optional. On Linux, pass your
user and group IDs at build time so files created through the source mount remain
editable on the host:

```bash
docker build --build-arg USER_ID="$(id -u)" --build-arg GROUP_ID="$(id -g)" -t technodev .
docker run --rm -it -v "$PWD:/workspace" -w /workspace technodev
```

After starting the container, synchronize from the mounted repository root:

```bash
uv sync --locked --group dev --group notebook
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The container environment lives in `/opt/venv`, outside the source mount. To run
JupyterLab, publish its port only on host loopback; token authentication stays on:

```bash
docker run --rm -it -p 127.0.0.1:8888:8888 -v "$PWD:/workspace" -w /workspace technodev \
  uv run --locked --group notebook jupyter lab --ip=0.0.0.0 --no-browser
```

Open the URL and token printed in the logs. Stop with Ctrl-C; mounted files stay
on the host. Rebuild after Dockerfile or system dependency changes, and sync after
dependency or lockfile changes.

On GitHub, choose **Code → Codespaces → Create codespace on main**. Locally, use
**Dev Containers: Reopen in Container** in VS Code. Both use the same Dockerfile
and synchronize the locked development and notebook groups after creation. The
container environment is `/opt/venv`; use `/opt/venv/bin/python` for the editor
and notebook kernel. Verify the selected interpreter in the container with
`python -c "import sys; print(sys.executable)"`.

To launch JupyterLab in Codespaces, run this from the repository root, then open
the forwarded port 8888 and use the token printed in the terminal. Keep the port
visibility **Private**:

```bash
uv run --locked --group notebook jupyter lab --ip=0.0.0.0 --no-browser
```

If dependency setup failed, rerun `uv sync --locked --group dev --group notebook`
from the repository root. After container configuration changes, rebuild the
existing Codespace or Dev Container.
