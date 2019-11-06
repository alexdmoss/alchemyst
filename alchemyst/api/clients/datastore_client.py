from google.cloud import datastore
import os


def query(kind, filter_key="", filter_val=""):
    query = _datastore_client().query(kind=kind)
    if filter_key and filter_val:
        query.add_filter(filter_key, '=', filter_val)
    return query


def _datastore_client():
    return datastore.Client(
        namespace=os.getenv("DATA_STORE_NAMESPACE"),
        project=os.getenv("DATA_STORE_PROJECT"),
    )
