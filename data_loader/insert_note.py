from google.cloud import datastore
from dataclasses import asdict
import os
import sys
import datetime
from alchemyst.api.data import Note


def main():

    note = Note(
        name="alicyclic-chemistry",
        title="Alicyclic Chemistry",
        author="Alex Moss",
        category="organic",
        tags=["alicyclic", "conformation", "energetics", "stereoselectivity", "Baldwin", "anomeric", "reactivity"],
        description="Basic notes on conformation, energetics, stereoselectivity and reactivity",
        level="2nd Year Undergraduate",
        filesize=162816,
        asset_link="/alicyclic-chemistry.pdf",
        doc_id=82,
        last_modified=datetime.datetime(2003, 12, 9, 0, 0, 0)
    )
    upsert_note(note)

    note = Note(
        name="aromatic-and-heterocyclic-chemistry",
        title="Aromatic & Heterocyclic Chemistry",
        author="Alex Moss",
        category="organic",
        tags=["aromatic", "heterocyclic", "aromaticity", "electrophilic", "nucleophilic", "radical", "pyrroles", "thiophenes",
              "furans", "isoxazoles", "pyrazoles", "isothiazoles", "pyridines", "quinolines", "isoquinolines", "indoles"],
        description="Covers aromatic reaction types, then moves onto the Synthesis and Reaction Types of each class of Heterocyclic Compound. Mostly from the two primers on these topics",
        level="2nd Year Undergraduate",
        filesize=295936,
        asset_link="/aromatic-and-heterocyclic-chemistry.pdf",
        doc_id=83,
        last_modified=datetime.datetime(2003, 12, 9, 1, 0, 0)
    )
    upsert_note(note)


def create_key(kind, id):
    return _datastore_client().key(kind, id)


def get(kind, id):
    return _datastore_client().get(create_key(kind, id))


def put(entity):
    return _datastore_client().put(entity)


def _datastore_client():
    return datastore.Client(
        namespace=os.getenv("DATA_STORE_NAMESPACE", "Alchemyst"),
        project=os.getenv("DATA_STORE_PROJECT", "moss-work"),
    )


def upsert_note(note: Note):
    entity = get(kind='Note', id=note.name)
    send_put = False
    if entity is None:
        key = create_key('Note', note.name)
        entity = datastore.Entity(key=key)
        send_put = True
    for key, value in asdict(note).items():
        if key not in entity.keys():
            entity.update({
                key: value
            })
            send_put = True
    if send_put:
        put(entity)

    return entity


if __name__ == "__main__":
    sys.exit(main())
