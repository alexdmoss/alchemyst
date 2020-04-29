# alchemyst

www.alchemyst.co.uk - a website for my University Chemistry notes

---

## Intro

This is a rebuild of a very old (2003) website I created when back at university. It was a relic of its time - PHP/MySQL stack, very basic UI that did the job, long before things like APIs and REST and so on.

As a learning exercise, I wanted to rebuild it in a language I'm becoming more proficient in now - Python - and also hook into some Google Cloud Platform magic (which is where it's hosted, and what I use at work) as further learning for me.

I also wanted to preserve the old URL structure which - despite being really nasty compound GET query variables - does reasonably ok on Google and I didn't want to lose the steady trickle of traffic the website already had. Maybe when the crawler re-learns, the NGINX redirection can be removed.

---

## Usage

Dockerfiles are split up due to the *really* long time it takes to install the grpcio pip module without wheels on alpine. To get the base image to rebuild it needs a git tag with `base*` for the [CI](https:/cloud.drone.io) to pick up, as it seems to lack globbing on file paths in the repo, which is a bit tedious.

---

## Deferred

- [ ] Something to check logs for 404s
- [ ] Metrics
- [ ] Test coverage is shocking
- [ ] 404 detection script
- [ ] Caching - especially full document from datastore
- [ ] Tags page
- [ ] Convert existing notes into HTML and upload

## Tests

- [ ] Contact Form relies on CORS - can only test once promoted

## Copy from the Cat

- [ ] Healthcheck
- [ ] Compression
- [ ] Caching

---

## Running Locally

```sh
pipenv install --dev
gcloud auth application-default login
./go run
```

---

## Removed Sections

- Ability to create new content through website - not needed, just me, static data now
- Admin Section - no need for login any more

---

## Architecture

I was originally going to run NGINX in front of it for redirects from old site, but the patterns are structured enough that this is quite easy to do with Flask's route decorators and manipulating the query parameters.

Doesn't really need Cloud DataStore - this data is pretty much static - but I wanted to try it out!

