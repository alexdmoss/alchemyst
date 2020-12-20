from alchemyst.api.clients.datastore_client import query, get


def query_by_kind(kind, category="", level=""):
    if category:
        return query(kind, "category", category)
    elif level:
        return query(kind, "level", level)
    else:
        return query(kind)


def get_entity(kind, id):
    return get(kind, str(id))
