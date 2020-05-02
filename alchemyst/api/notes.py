from dacite import from_dict
from dacite.config import Config
from datetime import datetime
from os import getenv
import json

from alchemyst.api.datastore import query_by_kind
from alchemyst.model.note import Note
from alchemyst import app


def get_notes(filter=""):
    filter = _translate_filter(filter)
    if getenv('USE_MOCKS') == 'True':
        results = []
        with open('./tests/mocks/full-dataset.json', 'r') as f:
            data = json.load(f)
        if filter:
            for note in data['entities']:
                for field in note:
                    if note[field] == filter:
                        results.append(note)
        else:
            results = data["entities"]
    else:
        if filter:
            query = query_by_kind(kind="Note", category=filter)
        else:
            query = query_by_kind(kind="Note")
        results = list(query.fetch())
    app.logger.debug(results)
    notes = [note_from_query(data) for data in results]
    return notes


def note_from_query(raw_data):
    return Note(
        name=get_key('name', raw_data),
        title=get_key('title', raw_data),
        author=get_key('author', raw_data),
        category=get_key('category', raw_data),
        tags=get_key('tags', raw_data),
        description=get_key('description', raw_data),
        level=get_key('level', raw_data),
        filesize=get_key('filesize', raw_data),
        asset_link=get_key('asset_link', raw_data),
        doc_id=get_key('doc_id', raw_data),
        last_modified=get_key('last_modified', raw_data),
    )


def get_key(key, raw_data):
    try:
        data = raw_data[key]
    except KeyError:
        data = None
    return data


def note_from_dict(note):
    return from_dict(data_class=Note, data=note, config=_isoformat_config())


def notes_from_dicts(notes):
    return [from_dict(data_class=Note, data=note, config=_isoformat_config())
            for note in notes]


def _isoformat_config():
    return Config(type_hooks={datetime: datetime.fromisoformat})


def _translate_filter(v):
    if v == 'first-year':
        v = '1st Year Undergraduate'
    elif v == 'second-year':
        v = '2nd Year Undergraduate'
    elif v == 'third-year':
        v = '3rd Year Undergraduate'
    return v
