# Open WebUI — A Field Guide

An English documentation website with a cosmic visual direction, chapter covers and a modular Django architecture. The web edition adapts the complete source guide, chapters 00–18, into focused English reading paths. The original chapter is linked from each page.

## Contents

1. [Run locally](#run-locally)
2. [Architecture](#architecture)
3. [Edit a chapter](#edit-a-chapter)
4. [Design and interactions](#design-and-interactions)
5. [Static export for Sites](#static-export-for-sites)
6. [Deploy Django](#deploy-django)
7. [Validation](#validation)

## Run locally

Use Python 3.10 or newer. From the extracted project directory:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell alternative
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Open http://127.0.0.1:8000/. No database, migrations, posts, CMS or administrator login is needed for these authored documentation pages.

## Architecture

| Location | Responsibility |
| --- | --- |
| `_core/` | Settings, top-level URLs, WSGI and ASGI |
| `main/` | Landing page and general site routes |
| `webui_doc/` | Documentation routes and catalogue metadata |
| `webui_doc/templates/webui_doc/chapters/` | Five hardcoded English chapter bodies |
| `templates/base.html` | Shared HTML document shell |
| `templates/partials/` | Header, footer, search and chapter list |
| `webui_doc/templates/webui_doc/partials/` | Chapter figures and previous/next navigation |
| `static/css/` | Tokens, layout, cosmos, documentation and responsive styles |
| `static/js/modules/` | Parallax, search and reading enhancements |
| `static/imgs/` | Optimised copies of original chapter assets |
| `scripts/` | Static export and route/reference checks |

Views select trusted chapter metadata and render explicit templates. Prose stays in HTML; `catalog.py` stores only navigation metadata. Namespaced Django URLs avoid hardcoded application-route coupling. Django autoescaping remains enabled.

## Edit a chapter

Edit the relevant `chapters/00.html` through `04.html`. Shared reading layout lives in `chapter_base.html`. Figures reuse the `figure.html` partial. If you add or rename a section, update the matching `sections` entry in `catalog.py` so both navigation and search reflect it.

For another chapter, add its metadata and template, then run the exporter and checks. The app deliberately validates slugs against the catalogue before selecting a template; unknown paths return 404.

## Design and interactions

The landing page uses vertical original covers, orbit lines and a restrained star field. The palette pairs visible midnight-blue and indigo gradients with muted turquoise typography and a faint petroleum-green atmospheric tint; buttons use deep teal rather than pale mint. CSS modules load directly with content-derived URL versions, so a changed palette requests fresh assets instead of reusing an old imported stylesheet. Chapter heroes use the same vocabulary and lead into a focused article layout. Layouts adapt at 1200, 900 and 650 pixels, including smaller screens with 22-pixel gutters.

Parallax modifies only the hero artwork using one scheduled update per animation frame. Reduced-motion preferences disable the movement and fading. No animation loop, canvas or remote font service is required.

The landing hero browses all five chapter covers with a layered, manual carousel. Swiping, dragging, arrow buttons, numbered selectors and keyboard arrows update one shared selection, including the heading, description, chapter number and destination. The foreground cover is a native chapter link; tapping an exposed background cover previews it first. Vertical touch gestures remain available for page scrolling, and a completed drag suppresses the following click so swiping cannot accidentally open a chapter. There is no autoplay. Reduced-motion preferences disable the cover transitions and copy animation. CSS and JavaScript request URLs carry content-derived versions so updated interactions load after publication.

Search filters chapter titles, summaries and section headings. It is navigation search, not full-text paragraph search. Native dialogs support keyboard dismissal and focus management. Illustrations can be enlarged; without JavaScript, their links still open the image. Content and chapter links work without JavaScript. Chapter printing has its own stylesheet.

## Static export for Sites

Sites serves the static export. **It does not run this Python/Django server.** Both versions use the exact same Django templates:

```bash
python scripts/export_static.py
python scripts/check_site.py
```

The exporter requests the real Django routes and writes seven pages to `dist/`, copies static assets and creates a portable source ZIP. It omits hosting identity, credentials and runtime state from the ZIP. Re-export after changing templates, content, URLs or assets.

## Deploy Django

Use a Python-capable host and a production WSGI/ASGI server. The `_core.wsgi:application` entry point is ready for that setup. Do not use Django's development server for production.

Set `DJANGO_DEBUG=0`, a strong `DJANGO_SECRET_KEY`, and the comma-separated `DJANGO_ALLOWED_HOSTS`. Run `python manage.py collectstatic` and configure the host or reverse proxy to serve `staticfiles/`. HTTPS is required by the production settings. If TLS terminates at a proxy, configure Django's trusted proxy settings for that actual deployment; they are intentionally not assumed here.

Production hosting infrastructure is outside this visual prototype. The Django source has a development-only fallback secret and refuses to start without an explicit production secret.

## Validation

The build was checked with Django's system check and its test client. The validation script checks all seven routes, unknown-chapter 404s, matching section anchors, duplicate ids, local links and static assets. JavaScript modules are syntax checked separately.

Browser layout, scrolling, modal interactions and mobile rendering require a visual browser review. Automated route checks do not establish those behaviours.
