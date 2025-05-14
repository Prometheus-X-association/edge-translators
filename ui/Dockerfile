# syntax = docker/dockerfile:1

ARG PYTHON_IMAGE_VERSION=3.12.3-slim

FROM python:${PYTHON_IMAGE_VERSION} AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT="/app/.venv"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# DEVELOPMENT
FROM python:${PYTHON_IMAGE_VERSION} AS runtime_dev

ENV APP_ENV=dev \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
	    curl \
    && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

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


COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /bin /bin

COPY --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]

HEALTHCHECK --start-period=60s CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

USER appuser

CMD ["streamlit", "run", "src/app.py"]

# PRODUCTION
FROM python:${PYTHON_IMAGE_VERSION} AS runtime_prod

ENV APP_ENV=dev \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
	    curl \
    && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

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

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /bin /bin

COPY --chown=appuser:appuser .streamlit .streamlit
COPY --chown=appuser:appuser data data
COPY --chown=appuser:appuser src src

COPY --chmod=775 docker/entrypoint.sh /usr/local/bin/docker-entrypoint
ENTRYPOINT ["docker-entrypoint"]

HEALTHCHECK --start-period=60s CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

USER appuser

CMD ["streamlit", "run", "src/app.py"]


