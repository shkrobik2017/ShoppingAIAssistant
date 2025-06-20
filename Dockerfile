# Stage 1: Builder
FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

COPY . .

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8501
EXPOSE 8000

CMD ["sh", "-c", "streamlit run src/streamlit_main.py --server.port=8501 --server.address=0.0.0.0 & uvicorn src.app:app --host 0.0.0.0 --port 8000 --loop uvloop"]
