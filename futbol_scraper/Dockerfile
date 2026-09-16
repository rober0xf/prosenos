FROM python:3.12-slim-trixie

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./

# install dependencies only (project will be installed after source is copied)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-install-project

COPY . .

# now install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

EXPOSE 8001

CMD ["uv", "run", "--no-sync", "python", "-m", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8001"]
