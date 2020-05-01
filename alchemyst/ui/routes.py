import yaml
import requests
from datetime import datetime

from flask import render_template, request, Response
from alchemyst import app

from alchemyst.ui.note import note_view
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
def display_notes():
    url_path = request.path
    notes_as_dict = notes().get_json()
    notes_list = notes_from_dicts(notes_as_dict["notes"])
    view = [note_view(note) for note in notes_list]
    return render_template('notes.html', notes=view, title='Notes', layout=layout, path=url_path)


@app.route('/notes/<category>', methods=['GET'])
def display_notes_by_category(category):
    url_path = request.path
    notes_as_dict = notes_by_category(category).get_json()
    notes_list = notes_from_dicts(notes_as_dict["notes"])
    view = [note_view(note) for note in notes_list]
    return render_template('notes.html', notes=view, title='Notes', layout=layout, path=url_path)


@app.route('/note/<note_name>', methods=['GET'])
def display_note(note_name):
    note_as_dict = note(note_name).get_json()
    note_obj = note_from_dict(note_as_dict)
    print(note_obj)
    view = note_view(note_obj)
    print(view)
    return render_template('note.html', note=view, title='Note', layout=layout)


@app.route('/pdf/<category>/<pdf_file>', methods=['GET'])
def download_pdf(category, pdf_file):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, f'https://storage.googleapis.com/{bucket}/'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

    # return redirect(f'https://storage.googleapis.com/{bucket}/pdfs/{category}/{pdf_file}')
