FROM python:3.12-slim-trixie

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

# copy the whole project first so workspace members (futbol_scraper) exist
# when uv resolves/syncs the workspace
COPY . .

# install deps
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
