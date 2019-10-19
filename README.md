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
  - [ ] Needs some images
- [ ] Contact Form (to my existing API)
- [x] Links Page (simplify)
- [ ] Data Loader
- [ ] PDF Index Page
- [ ] Organic
- [ ] Inorganic
- [ ] Physical
- [ ] Tags page
- [ ] Notes Detail Page
  - [ ] Format Date
  - [ ] Format Tags
  - [ ] Format Filesize
  - [x] Vertically middle the metadata
- [ ] Notes as HTML
- [ ] Mobile Friendly
  - [ ] Nav bar to hamburger
  - [ ] Does Search work?
- [x] Config file
- [x] Refactor: data model separated out
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
