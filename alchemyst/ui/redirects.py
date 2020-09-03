'''
This set of routes is in place to handle migration from the old PHP-based website.
Once requests to any old URLs dry up, it can be safely removed.
'''

from flask import redirect, url_for, request
from alchemyst import app

from alchemyst.ui.note import note_view
from alchemyst.api.routes import note
from alchemyst.api.notes import note_from_dict


@app.route('/alchemystry/<path:filename>', methods=['GET'])
def redir_alchemystry(filename):
    new_path = request.path.replace("/alchemystry", "")
    return redirect(new_path, code=301)


@app.route('/index.php', methods=['GET'])
def redir_index():
    target = request.args.get('target')
    if target == 'about':
        return redirect(url_for('about'), code=301)
    elif target == 'links':
        return redirect(url_for('links'), code=301)
    else:
        return redirect(url_for('index'), code=301)


@app.route('/contact.php', methods=['GET'])
def redir_contact():
    return redirect(url_for('contact'), code=301)


@app.route('/search.php', methods=['GET'])
def redir_search():
    return redirect(url_for('search'), code=301)


@app.route('/pdfindex.php', methods=['GET'])
def redir_pdfs():

    doc_id = request.args.get('id')
    group = request.args.get('group')
    category = request.args.get('value')

    if doc_id is not None:
        note_name = _get_note_name_from_id(doc_id)
        return redirect(url_for('display_note', note_name=note_name), code=301)
    else:
        if group == 'category':
            return redirect(url_for('display_notes_by_category', category=category.lower()), code=301)
        elif group == 'level':
            if category == '1':
                return redirect(url_for('display_notes_by_category', category='first-year'), code=301)
            elif category == '2':
                return redirect(url_for('display_notes_by_category', category='second-year'), code=301)
            elif category == '3':
                return redirect(url_for('display_notes_by_category', category='third-year'), code=301)
            else:
                return redirect(url_for('display_notes'), code=301)
        else:
            return redirect(url_for('display_notes'), code=301)


# 404 suppression - it annoys me!
@app.route('/images/download_arrow.gif', methods=['GET'])
def download_arrow():
    return redirect(url_for('static', filename='images/download_arrow.gif'), code=301)


def _get_note_name_from_id(id):
    note_as_dict = note(id).get_json()
    note_obj = note_from_dict(note_as_dict)
    view = note_view(note_obj)
    return view.name
