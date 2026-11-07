# Engineering Guidance

## Context

TechnoDev is a public Python 3.12 starter that becomes an independent project
when copied. Read `README.md` and `docs/project-context.md` first, then inspect
the relevant code and design notes. The starter has no generator runtime and
does not depend on private services or a specific AI coding provider.

## Engineering practices

- Make the smallest focused change that solves the stated problem. Preserve
  existing behavior and dependencies unless evidence calls for a change.
- Keep reusable logic in `src/<package>/`, scripts as thin entry points, tests
  focused, and notebooks for exploration.
- Use `pyproject.toml` and `uv.lock` as the dependency source of truth. Add
  dependencies with `uv add` or `uv add --dev`; do not hand-edit the lockfile or
  install persistent project dependencies with pip.
- Keep Python, `requires-python`, Ruff, CI, and container baselines aligned when
  changing the supported Python version.
- Keep agent guidance provider-independent. Do not add private integrations,
  provider-specific configuration, or orchestration without a demonstrated need.
- Update `README.md`, `AGENTS.md`, or project context when their documented facts
  change. Use `docs/task-template.md` only when a task benefits from a written brief.

## Implementation and validation

Inspect the existing implementation before planning a non-trivial change. Keep
plans proportional, preserve unrelated work, and explain assumptions that affect
behavior. Run relevant checks through uv and report the commands and actual
results; do not claim checks passed if they were not run.

The standard local checks are:

```bash
uv sync --locked
uv run --locked python scripts/example.py
uv run --locked pytest
uv run --locked ruff check .
uv run --locked ruff format --check .
```

## Scripting, modeling, and notebooks

- Make units, input provenance, parameters, shapes, and numerical tolerances
  explicit when they affect a result. Use small deterministic examples for routine
  tests; keep expensive runs and large datasets outside baseline checks.
- Keep paths and credentials out of machine-specific code and public commits.
- Use the optional `notebook` dependency group with the project environment.
  Keep notebooks runnable in order, put reusable logic in the package, and clear
  outputs and execution counts before committing by default.
- Docker and Dev Containers are optional. Preserve the shared lockfile and keep
  their environment separate from the host environment; see the README tutorial
  for setup details.
