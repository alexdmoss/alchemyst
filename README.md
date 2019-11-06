# alchemyst

www.alchemyst.co.uk - a website for my University Chemistry notes

---

## Intro

This is a rebuild of a very old (2003) website I created when back at university. It was a relic of its time - PHP/MySQL stack, very basic UI that did the job, long before things like APIs and REST and so on.

As a learning exercise, I wanted to rebuild it in a language I'm becoming more proficient in now - Python - and also hook into some Google Cloud Platform magic (which is where it's hosted, and what I use at work) as further learning for me.

I also wanted to preserve the old URL structure which - despite being really nasty compound GET query variables - does reasonably ok on Google and I didn't want to lose the steady trickle of traffic the website already had. Maybe when the crawler re-learns, the NGINX redirection can be removed.

---

## To Do

- [x] Basic framework
- [x] Dockerfile
- [x] Basic UI
  - [x] Optional trailing slash in Flask
  - [x] Auto-reload in Flask
  - [x] Buttons on left menu
- [x] UI enhancements
  - [x] background image on #content
  - [x] social icons
  - [x] Shadow on nav links
  - [x] Footer stays on screen
  - [x] FA icons on nav links
  - [x] animated underline of links in #content
  - [x] Subtle shadow around #content
  - [x] Better fonts
- [x] Home Page
- [x] About Page
  - [x] Needs some images
- [x] Links Page (simplify)
- [x] PDF Index Page
  - [x] Better padding of table
  - [x] Table sorting / filtering
  - [x] Search form at top
- [x] Data Loader
- [x] Config file
- [x] Refactor: data model separated out
- [x] Organic
- [x] Inorganic
- [x] Physical
- [x] Notes Detail Page
  - [x] Format Date
  - [x] Format Tags
  - [x] Format Filesize
  - [x] Vertically middle the metadata
- [x] Notes as HTML - read from storage
- [x] Downloadable PDFs
- [ ] Hide downloads under alchemyst.co.uk domain
- [ ] Set tags & import into DataStore
- [ ] Tags page
- [ ] Convert existing notes into HTML and upload
- [ ] Mobile Friendly
  - [ ] Nav bar to hamburger
  - [ ] Does Search work?
- [ ] Contact Form (to my existing API)
- [ ] Search - Elastic?
- [ ] Tracking usage - Analytics
- [ ] Old URL redirection (separate repo?)
- [ ] Privacy Policy /privacy
- [ ] Add a LICENSE file
- [ ] 404 detection script?
- [ ] SEO assets
  - [x] favicon.ico
  - [x] sizes="180x180" href="/images/apple-touch-icon.png"
  - [x] sizes="32x32" href="/images/favicon-32x32.png"
  - [x] sizes="16x16" href="/images/favicon-16x16.png"
  - [x] "/site.webmanifest"
  - [ ] "/safari-pinned-tab.svg" color="#5bbad5"

## Copy from the Cat

- [ ] Healthcheck
- [ ] Compression
- [ ] Caching

---

## Removed Sections

- Ability to create new content through website - not needed, just me, static data now
- Admin Section - no need for login any more

---

## Architecture

I was originally going to run NGINX in front of it for redirects from old site, but the patterns are structured enough that this is quite easy to do with Flask's route decorators and manipulating the query parameters.

Doesn't really need Cloud DataStore - this data is pretty much static - but I wanted to try it out!
