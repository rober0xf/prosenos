FROM python:3.12-slim-trixie

# we need make
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

# install deps creating an .env
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["make", "run"]
