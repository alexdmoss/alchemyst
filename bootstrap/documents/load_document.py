from google.cloud import datastore
from dataclasses import asdict, dataclass
import os
import sys
import glob


def main():

    client = _datastore_client()

    documents = glob.glob("./bootstrap/documents/*.html")

    for document in documents:
    
        filename = os.path.basename(document)
        doc_id = os.path.splitext(filename)[0]
    
        with open(document, 'r') as f:
            file_contents = f.read()
            doc = Document(
                name=doc_id,
                data=file_contents,
            )
            upsert_document(client, doc)


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


def upsert_document(client, document):
    print(document.name)
    entity = get(client, kind='Document', id=document.name)
    send_put = False
    if entity is None:
        key = create_key(client, 'Document', document.name)
        entity = datastore.Entity(key=key, exclude_from_indexes=['data'])
        send_put = True
    for key, value in asdict(document).items():
        entity.update({
            key: value
        })
        send_put = True
    if send_put:
        put(client, entity)

    return entity


@dataclass
class Document:
    name: str
    data: str


if __name__ == "__main__":
    sys.exit(main())
