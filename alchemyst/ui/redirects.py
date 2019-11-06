'''
This set of routes is in place to handle migration from the old PHP-based website.
Once requests to any old URLs dry up, it can be safely removed.
'''

from flask import redirect, url_for, request
from alchemyst import app


@app.route('/index.php', methods=['GET'])
def redir_index():
    target = request.args.get('target')
    if target == 'about':
        return redirect(url_for('about'))
    elif target == 'links':
        return redirect(url_for('links'))
    else:
        return redirect(url_for('index'))


@app.route('/contact.php', methods=['GET'])
def redir_contact():
    return redirect(url_for('contact'))


@app.route('/pdfindex.php', methods=['GET'])
def redir_pdfs():

    doc_id = request.args.get('id')
    group = request.args.get('group')
    category = request.args.get('value').lower()

    if doc_id:
        note_name = get_note_name_from_id(doc_id)
        return redirect(url_for('display_note_by_id', note_name))
    else:
        if group == "category":
            if category:
                return redirect(url_for('display_notes_by_category', category))
            else:
                return redirect(url_for('display_notes'))
        elif group == "level":
            if category == '1':
                return redirect(url_for('display_notes_by_category', 'first-year'))
            elif category == '2':
                return redirect(url_for('display_notes_by_category', 'second-year'))
            elif category == '3':
                return redirect(url_for('display_notes_by_category', 'third-year'))
        else:
            return redirect(url_for('display_notes'))


def get_note_name_from_id(id):
    print('hmmmmm')
