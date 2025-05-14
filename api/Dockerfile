# syntax = docker/dockerfile:1

ARG PYTHON_IMAGE_VERSION=3.12.3-slim-bookworm

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM builder AS runtime_dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

ENV API_ENVIRONMENT=dev \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
	    curl \
    && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN addgroup \
    --gid 1001 \
    --system appuser \
    && adduser \
    --home /app \
    --shell /bin/false \
    --disabled-password \
    --uid 1001 \
    --system \
    --group appuser \
    && chown -R appuser:appuser /app


COPY --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]

HEALTHCHECK --start-period=60s CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "info", "--access-log", "--use-colors"]
    

FROM python:${PYTHON_IMAGE_VERSION} AS runtime_prod

COPY --from=builder --chown=app:app /app /app

WORKDIR /app

ENV API_ENVIRONMENT=prod \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
	    curl \
    && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN addgroup \
    --gid 1001 \
    --system appuser \
    && adduser \
    --home /app \
    --shell /bin/false \
    --disabled-password \
    --uid 1001 \
    --system \
    --group appuser \
    && chown -R appuser:appuser /app

COPY --link . .
COPY --link --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint

ENTRYPOINT ["docker-entrypoint"]

HEALTHCHECK --start-period=60s CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "error", "--access-log", "--use-colors"]
