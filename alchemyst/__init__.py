# flake8: noqa
from os import getenv
from flask import Flask
# see README if setting gunicorn workers > 1
from prometheus_flask_exporter.multiprocess import PrometheusMetrics
from flask_compress import Compress
from flask_caching import Cache

from alchemyst.ui.note import EnhancedJSONEncoder
from alchemyst.cache import cache


def configure_cache(_app):
    cache.init_app(_app)


def configure_compression(_app):
    _app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript', 'application/pdf']
    Compress(_app)


def configure_json(_app):
    _app.json_encoder = EnhancedJSONEncoder
    _app.config['JSON_SORT_KEYS'] = False


def configure_metrics(_app):
    metrics = PrometheusMetrics(_app, static_labels={'app': 'alchemyst'})


def create_app():
    _app = Flask(__name__)
    _app.url_map.strict_slashes = False
    configure_cache(_app)
    configure_compression(_app)
    configure_json(_app)
    configure_metrics(_app)
    if getenv('USE_MOCKS') == 'True':
        _app.logger.info('Exporting USE_MOCKS - Mock Data ENABLED')
    return _app


app = create_app()

from alchemyst.ui import routes, errors, redirects
