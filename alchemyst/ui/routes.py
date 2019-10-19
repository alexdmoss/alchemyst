import yaml
from datetime import datetime

from flask import render_template
from alchemyst import app

from alchemyst.ui.note import note_view
from alchemyst.api.routes import note, notes
from alchemyst.api.notes import note_from_dict, notes_from_dicts


with open('app-config.yaml') as app_cfg_file:
    app_cfg = yaml.load(app_cfg_file, Loader=yaml.FullLoader)
    layout = app_cfg['layout']
    layout['year'] = datetime.now().year


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home', layout=layout)


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', layout=layout)


@app.route('/links')
def links():
    return render_template('links.html', title='Links', layout=layout)


@app.route('/about')
def about():
    return render_template('about.html', title='About', layout=layout)


@app.route('/tags')
def tags():
    return render_template('tags.html', title='Tags', layout=layout)


@app.route('/search')
def search():
    return render_template('search.html', title='Search', layout=layout)


@app.route('/notes')
def display_notes():
    notes_as_dict = notes().get_json()
    notes_list = notes_from_dicts(notes_as_dict["notes"])
    view = [note_view(note) for note in notes_list]
    return render_template('notes.html', notes=view, title='Notes', layout=layout)


@app.route('/note/<note_name>')
def display_note(note_name):
    note_as_dict = note(note_name).get_json()
    note_obj = note_from_dict(note_as_dict)
    view = note_view(note_obj)
    return render_template('note.html', note=view, title='Note', layout=layout)
