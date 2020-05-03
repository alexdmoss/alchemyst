# flake8: noqa
from flask import Flask
from healthcheck import HealthCheck
# see README if setting gunicorn workers > 1
from prometheus_flask_exporter.multiprocess import PrometheusMetrics

from datetime import datetime
from os import getenv

from alchemyst.ui.note import EnhancedJSONEncoder

app = Flask(__name__)

health = HealthCheck(app, "/healthz")

app.json_encoder = EnhancedJSONEncoder
app.url_map.strict_slashes = False

if getenv('USE_MOCKS') == 'True':
    app.logger.info('Exporting USE_MOCKS - Mock Data ENABLED')


from alchemyst.ui import routes, errors, redirects

metrics = PrometheusMetrics(app, static_labels={'app': 'alchemyst'})
