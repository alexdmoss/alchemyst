FROM al3xos/python-builder:3.9-debian11 AS builder

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# ---------------------------------------------------------------------

FROM al3xos/python-distroless:3.9-debian11

COPY . /app
COPY --from=builder /home/monty/.venv /home/monty/.venv

ENV PYTHONPATH=/home/monty/.venv/lib/python3.9/site-packages

WORKDIR /app

ENTRYPOINT ["python", "run.py", "--log-config=logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]
