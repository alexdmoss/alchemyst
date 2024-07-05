from flask import abort
from flask import jsonify

from alchemyst import app, cache
from alchemyst.api.notes import get_notes


@app.route("/health")
def ping():
    return "OK"


@app.route("/api/notes")
@cache.cached()
def notes():
    app.logger.info("Fetching list of notes")
    notes = {
        "notes": get_notes()
    }
    return jsonify(notes)


@app.route("/api/notes/<category>")
@cache.cached()
def notes_by_category(category):
    app.logger.info(f"Fetching list of notes with category: {category}")
    notes = {
        "notes": get_notes(category)
    }
    return jsonify(notes)


@app.route("/api/note/<note>")
@cache.cached()
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
