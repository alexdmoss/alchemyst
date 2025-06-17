from dacite import from_dict
from dacite.config import Config
from datetime import datetime
from os import getenv
import json

from alchemyst.api.datastore import query_by_kind
from alchemyst.model.note import Note
from alchemyst import app


def get_notes(translation=""):
    translation = _translate_filter(translation)
    if getenv('USE_MOCKS') == 'True':
        results = _get_mock_notes(translation)
    else:
        results = _get_query_notes(translation)
    return [note_from_query(data) for data in results]


def _get_mock_notes(translation):
    with open('./tests/mocks/full-dataset.json', 'r') as f:
        data = json.load(f)
    if translation:
        return _filter_mock_notes(data['entities'], translation)
    return data["entities"]


def _filter_mock_notes(entities, translation):
    results = []
    for note in entities:
        for field in note:
            if note[field] == translation:
                results.append(note)
                break
    return results


def _get_query_notes(translation):
    if translation:
        filter_type = _identify_filter_type(translation)
        if filter_type == "category":
            query = query_by_kind(kind="Note", category=translation)
        elif filter_type == "level":
            query = query_by_kind(kind="Note", level=translation)
        else:
            query = query_by_kind(kind="Note")
    else:
        query = query_by_kind(kind="Note")
    return list(query.fetch())


def note_from_query(raw_data):
    return Note(
        name=get_string('name', raw_data),
        title=get_string('title', raw_data),
        author=get_string('author', raw_data),
        category=get_string('category', raw_data),
        tags=get_list('tags', raw_data),
        description=get_string('description', raw_data),
        level=get_string('level', raw_data),
        filesize=get_int('filesize', raw_data),
        asset_link=get_string('asset_link', raw_data),
        doc_id=get_int('doc_id', raw_data),
        last_modified=get_date('last_modified', raw_data),
    )


def get_int(key, raw):
    try:
        data = raw[key]
    except KeyError:
        data = 0
    return data


def get_string(key, raw):
    try:
        data = raw[key]
    except KeyError:
        data = ""
    return data


def get_list(key, raw):
    try:
        data = raw[key]
    except KeyError:
        data = []
    return data


def get_date(key, raw):
    try:
        data = raw[key]
    except KeyError:
        data = datetime.now()
    return data


def note_from_dict(note):
    return from_dict(data_class=Note, data=note, config=_isoformat_config())


def notes_from_dicts(notes):
    return [from_dict(data_class=Note, data=note, config=_isoformat_config())
            for note in notes]


def _isoformat_config():
    return Config(type_hooks={datetime: datetime.fromisoformat})


def _identify_filter_type(f):
    if f in ["organic", "inorganic", "physical"]:
        return "category"
    if f in ["1st Year Undergraduate", "2nd Year Undergraduate", "3rd Year Undergraduate"]:
        return "level"
    app.logger.error(f"Failed to identify filter type - {f} does not appear to be a category or a level")
    return None


def _translate_filter(v):
    if v == 'first-year':
        v = '1st Year Undergraduate'
    elif v == 'second-year':
        v = '2nd Year Undergraduate'
    elif v == 'third-year':
        v = '3rd Year Undergraduate'
    return v
