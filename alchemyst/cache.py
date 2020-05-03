from os import getenv

from flask_caching import Cache

DEBUG_MODE = getenv('FLASK_DEBUG', 'false').lower() in {"1", "t", "true"}

if DEBUG_MODE:
    cache_type = "null"
else:
    cache_type = 'simple'

cache_config = {
    "CACHE_TYPE": cache_type,
    "CACHE_DEFAULT_TIMEOUT": 0  # infinite cache by default, as the data is very static
}

cache = Cache(config=cache_config)