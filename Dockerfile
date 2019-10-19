# pipenv venv install and create requirements files
FROM python:3.7.4-alpine AS requirements
COPY . /app/
WORKDIR /app
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pipenv lock --dev -r > requirements-dev.txt

# download & install packages
FROM python:3.7.4-alpine AS runtime-pips
COPY --from=requirements /app /app
WORKDIR /app
RUN apk update && \
    apk upgrade && \
    pip install -r requirements.txt

# run unit tests
FROM python:3.7.4-alpine AS pytest
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
RUN pip install -r requirements-dev.txt
RUN /usr/local/bin/pytest -s -v --disable-pytest-warnings --junit-xml junit-report.xml  

# create runtime image
FROM python:3.7.4-alpine
COPY --from=runtime-pips /app /app
COPY --from=runtime-pips /usr/local /usr/local
WORKDIR /app
RUN adduser -D alchemyst alchemyst
RUN chown alchemyst:alchemyst /app
USER alchemyst
ENV FLASK_APP=alchemyst
ENTRYPOINT [ "pipenv", "run", "flask", "run", "--host=0.0.0.0"]

