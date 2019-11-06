from alchemyst.api.clients.datastore_client import query


def query_by_kind(kind, category=""):
    if category:
        return query(kind, "category", category)
    else:
        return query(kind)
