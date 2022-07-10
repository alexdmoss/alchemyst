FROM al3xos/python-builder:3.9-debian11 AS runtime

ADD . /app
WORKDIR /app

RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

RUN pip install -r requirements.txt

# ---------------------------------------------------------------------

FROM al3xos/python-builder:3.9-debian11 AS pytest

COPY --from=runtime /app /app
COPY --from=runtime /usr/local /usr/local

WORKDIR /app

RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest -v --cov-report=term-missing --cov=.

# ---------------------------------------------------------------------

FROM al3xos/python-distroless:3.9-debian11

RUN mkdir /app

COPY --from=runtime --chown=monty:monty /app/alchemyst /app/alchemyst
COPY --from=runtime --chown=monty:monty /app/app-config.yaml /app/
COPY --from=runtime --chown=monty:monty /app/logging.conf /app/
COPY --from=runtime --chown=monty:monty /app/gunicorn_config.py /app/
COPY --from=runtime --chown=monty:monty /usr/local /usr/local

USER monty
WORKDIR /app

ENV FLASK_APP=alchemyst
CMD ["/usr/local/bin/gunicorn", "--log-config=logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]
