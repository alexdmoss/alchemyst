import yaml
import requests
from datetime import datetime

from flask import render_template, request, Response, send_from_directory, abort
from alchemyst import app, cache

from alchemyst.ui.note import note_view
from alchemyst.ui.safe import sanitise_path
from alchemyst.api.routes import note, notes, notes_by_category
from alchemyst.api.notes import note_from_dict, notes_from_dicts
from alchemyst.api.document import get_document


with open('app-config.yaml') as app_cfg_file:
    app_cfg = yaml.load(app_cfg_file, Loader=yaml.FullLoader)
    layout = app_cfg['layout']
    layout['year'] = datetime.now().year
    bucket = app_cfg['bucket']


@app.template_filter('display_document')
def fetch_note_from_doc_id(id):
    return get_document(id)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html', title='Home', layout=layout)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', title='Contact', layout=layout)


@app.route('/links', methods=['GET'])
def links():
    return render_template('links.html', title='Links', layout=layout)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About', layout=layout)


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html', title='Privacy Notice', layout=layout)


@app.route('/tags', methods=['GET'])
def tags():
    return render_template('tags.html', title='Tags', layout=layout)


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html', title='Search', layout=layout)


@app.route('/notes', methods=['GET'])
@cache.cached()
def display_notes():
    url_path = request.path
    notes_as_dict = notes().get_json()
    notes_list = notes_from_dicts(notes_as_dict["notes"])
    view = [note_view(note) for note in notes_list]
    return render_template('notes.html', notes=view, title='Notes', layout=layout, path=url_path)


@app.route('/notes/<category>', methods=['GET'])
@cache.cached()
def display_notes_by_category(category):
    url_path = request.path
    notes_as_dict = notes_by_category(category).get_json()
    notes_list = notes_from_dicts(notes_as_dict["notes"])
    view = [note_view(note) for note in notes_list]
    return render_template('notes.html', notes=view, title='Notes', layout=layout, path=url_path)


@app.route('/note/<note_name>', methods=['GET'])
@cache.cached()
def display_note(note_name):
    note_as_dict = note(note_name).get_json()
    note_obj = note_from_dict(note_as_dict)
    view = note_view(note_obj)
    return render_template('note.html', note=view, title='Note', layout=layout)


@app.route('/pdf/<category>/<pdf_file>', methods=['GET'])
@cache.cached()
def download_pdf(category, pdf_file):

    if not pdf_file.lower().endswith('.pdf'):
        abort(400, description="Invalid file type")

    safe_path = sanitise_path(f"{category}/{pdf_file}")
    target_url = f"https://storage.googleapis.com/{bucket}/pdf{safe_path}"
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        stream=True,
        allow_redirects=False)

    if resp.status_code != 200:
        abort(resp.status_code, description="File not found")

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers, content_type='application/pdf')


@app.route('/robots.txt')
@app.route('/favicon.ico')
@app.route('/apple-touch-icon-precomposed.png')
@app.route('/apple-touch-icon.png')
def static_from_root():
    return send_from_directory("static", request.path[1:])
