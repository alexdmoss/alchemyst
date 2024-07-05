import sys
from gunicorn.app.wsgiapp import run

# fake the command-line arguments for Gunicorn (easier with distroless)
sys.argv = [
    'gunicorn',
    'main:app',
    '--bind', '0.0.0.0:5000',
    '--workers', '1',
    '--threads', '3',
    '--access-logformat', '{ "remote_address": "%(h)s", "username": "%(u)s", "request_date": "%(t)s", "request": "%(r)s", "request_method": "%(m)s", "path": "%(U)s", "query_string": "%(q)s", "protocol": "%(H)s", "status": "%(s)s", "response_length": %(B)d, "referer": "%(f)s", "user_agent": "%(a)s", "request_seconds": %(T)d, "request_microseconds": %(D)d, "request_decimal_seconds": "%(L)s", "process_id": "%(p)s" }',  # noqa: E501
    "--log-config=logging.conf"
]

if __name__ == '__main__':
    sys.exit(run())
