from google.cloud import datastore
from dataclasses import asdict
import os
import json
import sys
# import datetime
from alchemyst.model.note import Note


def main():

    client = _datastore_client()

    notes = read_data()

    for note in notes:
        print(f"Updating Note: {note.name}")
        upsert_note(client, note)


def read_data():
    with open('./pdf.json', 'r') as f:
        data = json.load(f)
    results = data["entities"]
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


def create_key(client, kind, id):
    return client.key(kind, id)


def get(client, kind, id):
    return client.get(create_key(client, kind, id))


def put(client, entity):
    return client.put(entity)


def _datastore_client():
    return datastore.Client(
        namespace=os.getenv("DATA_STORE_NAMESPACE"),
        project=os.getenv("DATA_STORE_PROJECT"),
    )


def upsert_note(client, note):
    entity = get(client, kind='Note', id=note.name)
    send_put = False
    if entity is None:
        key = create_key(client, 'Note', note.name)
        entity = datastore.Entity(key=key)
        send_put = True
    for key, value in asdict(note).items():
        entity.update({
            key: value
        })
        send_put = True
    if send_put:
        put(client, entity)

    return entity


if __name__ == "__main__":
    sys.exit(main())
