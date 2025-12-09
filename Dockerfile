# # Stage 1: build + install deps with uv
# FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# WORKDIR /app

# COPY pyproject.toml uv.lock* ./
# RUN uv sync --frozen --no-dev

# # Stage 2: runtime image
# FROM python:3.12-slim

# WORKDIR /app

# COPY --from=builder /app/.venv /app/.venv

# ENV PATH="/app/.venv/bin:$PATH"

# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY . /app

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY . /app

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]