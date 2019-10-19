import dataclasses
import json

from alchemyst.model.note import Note


def note_view(note):
    return Note(
        name=note.name,
        title=note.title,
        author=note.author,
        category=note.category,
        tags=note.tags,
        description=note.description,
        level=note.level,
        filesize=note.filesize,
        asset_link=note.asset_link,
        doc_id=note.doc_id,
        last_modified=note.last_modified,
    )


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        else:
            return o.isoformat()
