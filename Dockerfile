FROM eu.gcr.io/moss-work/alchemyst-base:cached

COPY --chown=flask-app:flask-app ./alchemyst /app/alchemyst
COPY --chown=flask-app:flask-app ./app-config.yaml /app/
COPY --chown=flask-app:flask-app ./logging.conf /app/
COPY --chown=flask-app:flask-app ./gunicorn_config.py /app/

USER flask-app
WORKDIR /app
ENV FLASK_APP=alchemyst

CMD ["pipenv", "run", "gunicorn", "--log-config=logging.conf",  "--config=gunicorn_config.py", "alchemyst:app"]
