import yaml
from datetime import datetime
from flask import render_template

from alchemyst import app


with open('app-config.yaml') as app_cfg_file:
    app_cfg = yaml.load(app_cfg_file, Loader=yaml.FullLoader)
    layout = app_cfg['layout']
    layout['year'] = datetime.now().year


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', layout=layout), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', layout=layout), 500
