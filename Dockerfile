FROM alchemyst-base:cached

COPY --chown=flask-app:flask-app ./alchemyst /app/alchemyst
COPY --chown=flask-app:flask-app ./app-config.yaml /app/
COPY --chown=flask-app:flask-app ./gunicorn_logging.conf /app/
COPY --chown=flask-app:flask-app ./gunicorn_config.py /app/

USER flask-app
WORKDIR /app
ENV FLASK_APP=alchemyst

CMD ["pipenv", "run", "gunicorn", "--log-config=gunicorn_logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]



# ARG PYTHON_VERSION=3.7.7-alpine3.11
# ARG APP_NAME=alchemyst

# FROM python:$PYTHON_VERSION AS requirements
# ADD . /app
# WORKDIR /app
# RUN pip install pipenv=='2018.11.26'
# RUN pipenv lock -r > requirements.txt
# RUN pipenv lock --dev -r > requirements-dev.txt

# FROM python:$PYTHON_VERSION AS runtime-pips
# COPY --from=requirements /app /app
# WORKDIR /app
# RUN apk update --no-cache \
#     && apk upgrade \
#     && apk add gcc g++ musl-dev libffi-dev openssl-dev
# RUN pip install -r requirements.txt --no-use-pep517

# FROM python:$PYTHON_VERSION AS pytest
# COPY --from=runtime-pips /app /app
# COPY --from=runtime-pips /usr/local /usr/local
# WORKDIR /app
# RUN pip install -r requirements-dev.txt
# RUN /usr/local/bin/pytest -v --cov-report=term-missing --cov=.

# FROM python:$PYTHON_VERSION
# RUN adduser -D flask-app flask-app
# COPY --from=runtime-pips --chown=flask-app:flask-app /app/$APP_NAME /app/$APP_NAME
# COPY --from=runtime-pips --chown=flask-app:flask-app /app/gunicorn_logging.conf /app/
# COPY --from=runtime-pips --chown=flask-app:flask-app /app/gunicorn_config.py /app/
# COPY --from=runtime-pips --chown=flask-app:flask-app /usr/local /usr/local
# USER flask-app
# WORKDIR /app
# ENV FLASK_APP=$APP_NAME
# CMD ["/usr/local/bin/gunicorn", "--log-config=gunicorn_logging.conf",  "--config=gunicorn_config.py", "$APP_NAME:app"]

#######