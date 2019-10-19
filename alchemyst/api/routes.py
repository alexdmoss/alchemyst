from flask import abort
from flask import jsonify

from alchemyst import app
from alchemyst.api.notes import get_notes


@app.route("/api/notes")
def notes():
    app.logger.info("Fetching list of services")
    notes = {
        "notes": get_notes()
    }
    return jsonify(notes)


@app.route("/api/notes/<note_name>")
def note(note_name):
    app.logger.info(f"Fetching note {note_name}")
    note = next((i for i in get_notes() if i.name == note_name), None)
    if note is None:
        abort(404)
    else:
        return jsonify(note)
