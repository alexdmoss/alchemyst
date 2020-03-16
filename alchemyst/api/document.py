from os import getenv

from alchemyst.api.datastore import get_entity
from alchemyst.model.document import Document


def get_document(id):
    if getenv('USE_MOCKS') == 'True':
        with open(f'./tests/mocks/document.html', 'r') as f:
            doc = f.read()
    else:
        raw_data = get_entity('Document', id)
        doc = document_from_query(raw_data)
    if doc.data is not None:
        return doc.data
    else:
        return '''<div class='centered'><div class='error'>
        Sorry, but the HTML version wasn't found, or hasn't been converted yet.
        You can still download it using the above link!
        </div></div>'''


def document_from_query(raw_data):
    return Document(
        name=get_key('name', raw_data),
        data=get_key('data', raw_data),
    )


def get_key(key, raw_data):
    try:
        data = raw_data[key]
    except KeyError:
        data = None
    except TypeError:
        data = None
    return data
