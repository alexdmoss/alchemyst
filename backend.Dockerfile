FROM al3xos/python-builder:3.12-debian12 AS builder

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# ---------------------------------------------------------------------

FROM al3xos/python-distroless:3.12-debian12-debug

COPY alchemyst/ /app/alchemyst
COPY logging.conf run.py app-config.yaml /app/
COPY --from=builder /home/monty/.venv /home/monty/.venv

WORKDIR /app

ENTRYPOINT ["/home/monty/.venv/bin/python", "run.py"]
