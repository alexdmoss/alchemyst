from google.cloud import datastore
from os import getenv

from alchemyst import app


def query(kind, filter_key="", filter_val=""):
    query = _datastore_client().query(kind=kind)
    app.logger.debug(query)
    if filter_key and filter_val:
        query.add_filter(filter_key, '=', filter_val)
    return query


def get(kind, id):
    key = _datastore_client().key(kind, id)
    return _datastore_client().get(key)


def _datastore_client():
    return datastore.Client(
        namespace=getenv("DATA_STORE_NAMESPACE"),
        project=getenv("DATA_STORE_PROJECT"),
    )
