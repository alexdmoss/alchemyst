FROM al3xos/python-builder:3.12-debian12 AS builder

WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# ---------------------------------------------------------------------

FROM al3xos/python-distroless:3.12-debian12

COPY alchemyst/ /app/alchemyst
COPY logging.conf run.py app-config.yaml gunicorn_config.py /app/
COPY --chown=1000:1000 --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
ENTRYPOINT ["python", "run.py", "--log-config=logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]
