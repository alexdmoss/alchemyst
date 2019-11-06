from os import getenv

from alchemyst.api.storage import get_document_from_gcs


def get_document(id):
    doc = ""
    if getenv('USE_MOCKS') == 'True':
        doc = f"Using Mocks - would be serving document ID: {id}"
        with open('./tests/mocks/document.html', 'r') as f:
            doc += f.read()
    else:
        doc = get_document_from_gcs(id)
    if doc is not None:
        return doc
    else:
        return "<div class='centered'><div class='error'>Sorry, but this file was not found!</div></div>"
