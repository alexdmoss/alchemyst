# flake8: noqa
from flask import Flask
from datetime import datetime

from alchemyst.ui.note import EnhancedJSONEncoder

app = Flask(__name__)
app.json_encoder = EnhancedJSONEncoder
app.url_map.strict_slashes = False


from alchemyst.ui import routes, errors
