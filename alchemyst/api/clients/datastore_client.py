from google.cloud import datastore
import os


def query(kind):
    return _datastore_client().query(kind=kind)


def _datastore_client():
    return datastore.Client(
        namespace=os.getenv("DATA_STORE_NAMESPACE", "Alchemyst"),
        project=os.getenv("DATA_STORE_PROJECT", "moss-wok"),
    )
