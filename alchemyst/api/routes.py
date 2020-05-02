from flask import abort
from flask import jsonify

from alchemyst import app
from alchemyst.api.notes import get_notes


@app.route("/api/notes")
def notes():
    app.logger.info("Fetching list of notes")
    notes = {
        "notes": get_notes()
    }
    app.logger.debug(notes)
    return jsonify(notes)


@app.route("/api/notes/<category>")
def notes_by_category(category):
    app.logger.info(f"Fetching list of notes with category: {category}")
    notes = {
        "notes": get_notes(category)
    }
    return jsonify(notes)


@app.route("/api/note/<note>")
def note(note_id):
    app.logger.info(f"Fetching note {note_id}")
    # note_id could be id (int) or name (str)
    try:
        note_id = int(note_id)
        note = next((i for i in get_notes() if i.doc_id == note_id), None)
    except ValueError:
        note = next((i for i in get_notes() if i.name == note_id), None)
    if note is None:
        abort(404)
    else:
        return jsonify(note)
