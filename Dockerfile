ARG PYTHON_VERSION=3.9.5-slim-buster

FROM python:$PYTHON_VERSION AS runtime

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv

RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

RUN pip install -r requirements.txt

# ---------------------------------------------------------------------

FROM python:$PYTHON_VERSION AS pytest
COPY --from=runtime /app /app
COPY --from=runtime /usr/local /usr/local
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest -v --cov-report=term-missing --cov=.

# ---------------------------------------------------------------------

FROM python:$PYTHON_VERSION
RUN addgroup --gid=1000 flask-app
RUN adduser --uid=1000 --ingroup=flask-app flask-app
RUN mkdir /app
COPY --from=runtime --chown=flask-app:flask-app /app/alchemyst /app/alchemyst
COPY --from=runtime --chown=flask-app:flask-app /app/app-config.yaml /app/
COPY --from=runtime --chown=flask-app:flask-app /app/logging.conf /app/
COPY --from=runtime --chown=flask-app:flask-app /app/gunicorn_config.py /app/
COPY --from=runtime --chown=flask-app:flask-app /usr/local /usr/local
USER flask-app
WORKDIR /app
ENV FLASK_APP=alchemyst
CMD ["/usr/local/bin/gunicorn", "--log-config=logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]
