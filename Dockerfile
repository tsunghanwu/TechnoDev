FROM ghcr.io/astral-sh/uv:0.5.9 AS uv
FROM python:3.12-slim

ARG USER_ID=1000
ARG GROUP_ID=1000

COPY --from=uv /uv /uvx /usr/local/bin/
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd --gid ${GROUP_ID} developer \
    && useradd --uid ${USER_ID} --gid developer --create-home --shell /bin/bash developer \
    && mkdir -p /workspace /opt/venv \
    && chown -R developer:developer /workspace /opt/venv

WORKDIR /workspace
COPY --chown=developer:developer pyproject.toml uv.lock README.md ./
USER developer
RUN uv sync --locked --group dev --group notebook --no-install-project

CMD ["bash"]
