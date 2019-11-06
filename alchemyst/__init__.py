# flake8: noqa
from flask import Flask
from datetime import datetime
from os import getenv

from alchemyst.ui.note import EnhancedJSONEncoder

app = Flask(__name__)
app.json_encoder = EnhancedJSONEncoder
app.url_map.strict_slashes = False

if getenv('USE_MOCKS') == 'True':
    app.logger.info('Exporting USE_MOCKS - Mock Data ENABLED')


from alchemyst.ui import routes, errors, redirects
