from alchemyst.api.clients.datastore_client import query, get
from alchemyst import app


def query_by_kind(kind, category=""):
    app.logger.debug(f"Querying kind:{kind}")
    if category:
        return query(kind, "category", category)
    else:
        return query(kind)


def get_entity(kind, id):
    return get(kind, str(id))
