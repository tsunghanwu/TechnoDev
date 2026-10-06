# TechnoDev

TechnoDev is a cloneable Python starter for scripting, modeling, and Jupyter
notebook analytics. Each clone is an independent project; there is no generator
runtime. Local development uses uv, with an optional Docker and VS Code Dev
Containers workflow.

## Start a project

TechnoDev is the **starter repository**. After you clone it and begin a real Python
project, this README should be rewritten to describe that project's purpose,
setup, inputs, commands, and outputs. Do not keep the starter README as the
long-term project README simply because the code originated from TechnoDev.

Install Python 3.12 and [uv](https://docs.astral.sh/uv/), then synchronize the
locked development dependencies and run the example:

```bash
uv sync --locked
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The installable package lives in `src/project/`; scripts, tests, and notebooks
import it directly. Add runtime libraries with `uv add <library>` and development
tools with `uv add --dev <tool>`. Both update `pyproject.toml` and `uv.lock`.

After cloning, optionally rename the neutral starter package with:

```bash
uv run python scripts/rename_project.py my_project
uv lock
uv sync --locked
uv run --locked pytest
```

The helper accepts a lowercase snake_case Python package name and updates the
distribution name, package directory, example script, and tests. It is a one-time
clone convenience, not a TechnoDev runtime or project generator.

For a hands-on walkthrough of local setup, package logic, checks, notebooks, and
optional Docker development, see the [starter tutorial](docs/tutorial.md).

## Notebooks

Install JupyterLab and ipykernel into the same project environment and launch from
the repository root:

```bash
uv sync --locked --group notebook
uv run --locked --group notebook jupyter lab
```

Use the project's `.venv` kernel. The example notebook uses synthetic data and
shared package logic. Keep local inputs in ignored `data/`, generated results in
ignored `outputs/`, and clear notebook outputs before committing by default.

## Optional Docker development

Docker and VS Code are optional; native uv development does not require them. On
Linux, pass your host user and group IDs when building to keep created files
editable on the host:

```bash
docker build --build-arg USER_ID="$(id -u)" --build-arg GROUP_ID="$(id -g)" -t technodev .
docker run --rm -it -v "$PWD:/workspace" -w /workspace technodev
```

After mounting the repository, synchronize so the editable install points to the
mounted source. Run checks in the container with:

```bash
docker run --rm -v "$PWD:/workspace" -w /workspace technodev uv sync --locked --group dev --group notebook
docker run --rm -v "$PWD:/workspace" -w /workspace technodev uv run --locked pytest
docker run --rm -v "$PWD:/workspace" -w /workspace technodev uv run --locked ruff check .
docker run --rm -v "$PWD:/workspace" -w /workspace technodev uv run --locked ruff format --check .
```

Launch Jupyter on the container interface and publish it only on host loopback;
token authentication remains enabled:

```bash
docker run --rm -it -p 127.0.0.1:8888:8888 -v "$PWD:/workspace" -w /workspace technodev \
  uv run --locked --group notebook jupyter lab --ip=0.0.0.0 --no-browser
```

Open the URL and token printed in the container logs, then press Ctrl-C to stop
the container. The mounted source and outputs remain on the host. Rebuild after
system dependency or Dockerfile changes; synchronize after dependency or lockfile
changes. Add `-v /path/to/data:/workspace/data:ro` to mount external input data.
The environment lives in `/opt/venv`, outside the source mount.

VS Code users can reopen the repository in a Dev Container; it uses the same
Dockerfile, selects `/opt/venv/bin/python`, forwards port 8888, and synchronizes
locked dependencies after creation.

## Maintenance

GitHub Dependabot checks GitHub Actions monthly. The uv version is deliberately
pinned in both `.github/workflows/checks.yml` and `Dockerfile`; update those two
pins together when upgrading uv. CI also builds the package and installs the
wheel into a clean temporary environment to catch packaging-boundary failures.

## AI pair programming

Read [AGENTS.md](AGENTS.md) and [project context](docs/project-context.md) before
making changes. Give an agent the goal, constraints, and expected result; use the
optional [task brief](docs/task-template.md) for substantial work. Review the
changes and reported validation. Shared guidance is provider-independent and
does not require an AI SDK or API key.

After cloning and starting the real project, replace the starter-facing parts of
README with project-facing documentation: what the project does, how to set it
up with uv, its main workflows, inputs/outputs, and project-specific validation.
Also update agent guidance and project context. The
[development design](docs/python-development-design.md) records the layout and
modeling conventions behind this starter and can remain as historical/reference
documentation unless the clone's design intentionally diverges.
