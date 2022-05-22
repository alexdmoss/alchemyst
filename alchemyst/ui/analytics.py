'''
This set of routes is in place to calls to the Plausible JS & API from this host,
as we don't have NGINX in front to do this for us (ish).
'''

from flask import request, Response
import requests

from alchemyst import app


def _proxy_url(http_url: str):
    # https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask
    resp = requests.request(
        method=request.method,
        url=http_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, headers)


@app.route('/api/event')
def proxy_plausible_api():
    return _proxy_url(http_url="https://plausible.alexos.dev/api/event")


@app.route('/js/visits.js')
def proxy_plausible_js():
    return _proxy_url(http_url="https://plausible.alexos.dev/js/plausible.outbound-links.js")
