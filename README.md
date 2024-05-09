# alchemyst

alchemyst.co.uk - a website for my University Chemistry notes

---

## Intro

This is a rebuild of a very old (2003) website I created when back at university. It was a relic of its time - PHP/MySQL stack, very basic UI that did the job, long before things like APIs and REST and so on.

As a learning exercise, I wanted to rebuild it in a language I'm becoming more proficient in now - Python - and also hook into some Google Cloud Platform magic (which is where it's hosted, and what I use at work) as further learning for me.

I also wanted to preserve the old URL structure which - despite being really nasty compound GET query variables - does reasonably ok on Google and I didn't want to lose the steady trickle of traffic the website already had. Maybe when the crawler re-learns, the NGINX redirection can be removed.

---

## To Do

- [ ] Some special characters not displaying properly - I think --> type arrows
- [ ] See if can simplify CSS / fix changes in heading
- [ ] Can LLM summarise for me?
- [ ] Take advantage of the fact there is nginx now - metrics + proxy/cache assets
- [ ] Center content on wide screens
- [ ] Pad the top menu more on wide screens
- [ ] Something to check logs for 404s
- [ ] Metrics on Datastore and GCS
- [ ] Test coverage is shocking
- [ ] Tags page
- [ ] Browser tests

---

## Running Locally

```sh
pipenv install --dev
gcloud auth application-default login
./go run
# or ./go run-wsgi if want to run in gunicorn
```

---

## Redirects

I was originally going to run NGINX in front of it for redirects from old site, but the patterns are structured enough that this is quite easy to do with Flask's route decorators and manipulating the query parameters.

Doesn't really need Cloud DataStore - this data is pretty much static - but I wanted to try it out!

---

## Prometheus Metrics & Gunicorn Workers

At the moment, the app is configured with a single worker in gunicorn - it's pretty low traffic website after all, and the nodes I run it across are tiddly. This means we can get Prometheus metrics easily enough with this in `__init__.py` ...

```python
from prometheus_flask_exporter.multiprocess import PrometheusMetrics
metrics = PrometheusMetrics(app, static_labels={'app': 'alchemyst'})
```

... and still get `python_*` metrics from the Prometheus client. Groovy. However, when `gunicorn` spawns more than one process (worker), we need to switch the above to import `GunicornPrometheusMetrics` instead, which will amalgamate the http stats that are being collected. Also awesome - but it can't do this for the base python metrics so they are switched off. Sad times.

**NOTE:** The `gunicorn_config.py` also needs updating as follows:

```python
import os
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(int(os.getenv('METRICS_PORT')))

def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
```

And environment variables are then needed:

```sh
export prometheus_multiproc_dir=/tmp   # this needs to be writable (k8s config emptyDir{} should do it)
export METRICS_PORT=9120
```

(specifically, it is the need to set the `prometheus_multiproc_dir` that turns off the python metrics - it gives somewhere to save the metric state)
