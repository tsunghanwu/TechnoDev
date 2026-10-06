# Project Agent Instructions

## Project Context
- Read `README.md` and `docs/project-context.md` before starting work. Read the relevant design or code next.
- This repository implements the cloneable Python starter described in `docs/python-development-design.md`.
- Use the actual uv commands in `README.md`; report checks as passed only when they have run successfully in the selected environment.
- Update project context when the purpose, structure, or workflow changes. Keep task-specific discussion out of permanent instructions.

## TechnoDev Design
- TechnoDev is a **cloneable Python starter**, not a runtime framework, generator service, or dependency that downstream projects keep using.
- A fresh clone becomes an independent Python project. The one-time rename helper may rename the neutral `project` package, after which the clone should evolve around its own domain and requirements.
- Reusable code belongs under the installable package in `src/<package>/`. Keep `scripts/` as thin entry points, `notebooks/` for exploration and analysis, and `tests/` for focused automated validation.
- Keep local development as the default. Docker and Dev Containers are optional environments that consume the same project metadata and lockfile rather than defining a second dependency workflow.
- Do not add scientific or framework dependencies to the starter by assumption. Add only what the actual project needs.
- After turning the starter into a real project, update `README.md`, `docs/project-context.md`, and this file so they describe the project that now exists rather than TechnoDev starter behavior.

## uv Project Flow
- Treat `pyproject.toml` as the source of declared project metadata and dependencies, and commit `uv.lock` as the reproducible resolved environment. Do not introduce a parallel `requirements.txt` workflow unless the project explicitly requires one.
- Use the committed Python baseline from `.python-version`; keep it consistent with `requires-python`, Ruff configuration, CI, and container configuration when changing Python versions.
- Synchronize a clone or changed lockfile with `uv sync --locked`. uv manages the local `.venv`; activation is optional because project commands should normally run through `uv run`.
- Run project commands through the locked environment, for example `uv run --locked pytest`, `uv run --locked ruff check .`, and `uv run --locked python <script>`.
- Add runtime dependencies with `uv add <package>`; add development-only tools with `uv add --dev <package>`; add notebook-only dependencies to the notebook group when appropriate. Commit the resulting `pyproject.toml` and `uv.lock` changes together.
- Do not use `pip install` directly into the project environment for persistent dependencies, and do not hand-edit `uv.lock`.
- When intentionally changing dependency constraints or project metadata, refresh the lockfile with uv and then validate with locked commands. When only consuming the committed environment, prefer `--locked` so unexpected lockfile drift fails visibly.
- Building a wheel is not required for normal development: uv installs the package in editable form during sync, so changes under `src/` are immediately available to scripts and tests. Build/package validation is a release or CI boundary check, not a prerequisite for editing code.
- For notebooks, install/select the notebook dependency group and use the same project environment; do not create a separate notebook dependency file or install packages from notebook cells.

## Core Principles
- Work as a careful software engineer: understand the request and the existing project before making changes.
- Prefer the smallest change that fully solves the requested problem. Avoid unrelated refactors and feature creep.
- Follow existing project conventions, dependencies, and architecture unless there is a clear reason to change them.
- Preserve user changes. Do not overwrite or revert unrelated work.

## Workflow

### 1. Understand and plan
- Inspect relevant files and project conventions before proposing an implementation.
- For non-trivial work, present a concise `### Proposed Plan` with the key steps and design decisions before editing.
- Keep the plan proportional to the task; routine, narrowly scoped changes do not need an elaborate design.
- Ask clarifying questions when requirements are materially ambiguous or proceeding could cause a consequential or irreversible change.
- Do not require approval for routine implementation after presenting a plan unless the user or the available interface explicitly requires it. If confirmation is needed, wait before editing.

### 2. Implement
- Make changes consistent with the approved plan and the surrounding code.
- Keep edits focused. Update related tests, documentation, configuration, and call sites when they are necessary for the requested change.
- Add comments only when they explain non-obvious intent or constraints.

### 3. Validate
- Choose validation appropriate to the change and the project: run focused tests first, then broader checks when useful.
- Use the project’s existing test and build workflows. Do not introduce a Python virtual environment or add dependencies unless required by the project or specific test.
- For documentation-only or otherwise non-executable changes, review the result for accuracy, clarity, and consistency instead of inventing an irrelevant test.
- If a test or command fails, inspect and explain the failure before retrying; fix issues introduced by the change when practical.
- Report what validation was run and any checks that could not be run.
- Ask the user whether additional testing is needed when appropriate validation is unclear or requires a meaningful tradeoff.

## Communication
- Be concise, direct, and transparent about assumptions and uncertainty.
- Use bullets for plans or multi-step explanations; avoid dense paragraphs.
- Explain consequential behavior changes, risks, and required follow-up.
- Do not claim a build, test, or other check passed unless it was actually run and passed.

## Scripting and Modeling
- Keep reusable calculations and transformations in the project package; keep scripts and notebooks focused on orchestration and exploration.
- Make assumptions about units, shapes, missing values, numerical tolerances, and model parameters explicit. Ask when an ambiguity would change the scientific meaning of a result.
- Use small synthetic or approved test fixtures for validation. Do not upload private datasets, credentials, or model artifacts to external services without explicit authorization.
- Do not silently change datasets, evaluation splits, objectives, or baselines to make checks pass. Explain changes to model behavior and evaluation separately from code quality checks.
- Record seeds, parameters, and input provenance when reproducibility matters. Distinguish tested results from expected results.
- Run small checks first. Ask before expensive training, paid compute, or lengthy experiments unless already authorized by the task.
- Follow the project's dependency and environment workflow once implemented; do not create a parallel environment or dependency file.

## Jupyter Notebooks
- Keep exploratory analytics in `notebooks/` and reusable logic in the project package. Use the project's environment as the notebook kernel.
- Preserve unrelated cells, cell IDs, and metadata. Prefer focused cell edits through notebook-aware tools; avoid rewriting the whole notebook for a small change.
- Keep imports, input paths, and parameters near the beginning. Do not depend on cells having been run out of order or install packages inside notebook cells.
- Validate changed notebooks by restarting the kernel and running all cells in order with small approved inputs when practical. Report when execution is blocked by missing data or compute requirements.
- Clear outputs and execution counts before committing by default. Retain outputs only when requested for a report, after reviewing their contents. Do not erase unrelated saved results without agreement.
- Review plots and data conclusions separately from automated code checks. Do not claim notebook execution or analytical correctness based only on linting.

## Optional Containers
- Use the environment selected for the task: local development or the documented development container. State where checks ran; do not imply both environments were validated.
- Share dependency metadata and the lockfile across environments. Keep the container environment separate from the host `.venv`.
- Preserve mounted source files and data; container recreation must not discard user work. Do not broaden mounts or copy local credentials into images without authorization.
- Keep notebook kernels aligned with the selected environment. Preserve Jupyter authentication and local-only host access in the development setup.
- Report unavailable Docker or Dev Container checks explicitly.
