# Harbor Light — Audio Drama Website

Static SEO site generated from Spotify for Podcasters (Anchor) RSS feeds.

- **EN** `https://anchor.fm/s/119b406bc/podcast/rss`
- **DE** `https://anchor.fm/s/119c2139c/podcast/rss`
- **FR** `https://anchor.fm/s/119c33574/podcast/rss`

Free hosting: **GitHub Pages** (`/docs` or Actions artifact).

## Quick start

```bash
cd harbor-light-website
pip install -r requirements.txt
python generator.py
```

Output → `docs/` (author hub + Harbor Light series + `de.html`/`fr.html`/`es.html`/`it.html` landings + `en/` `de/` `fr/` shows + `tech-books.html` + `music.html`, sitemap, robots).

Catalog data in `config.py`: `FEEDS`, `HARBOR_SERIES`, `TECH_BOOKS`, `GUMROAD_COMPANIONS`, `MUSIC_TRACKS`.

CTA path on romance pages: **Spotify free → Gumroad full audio → Amazon Kindle** (`amazon.com` only).

## Before first publish

1. Edit `config.py`:
   - `SITE["base_url"]` → `https://picubiancamaria.com` (or Pages URL)
   - `SITE["formspree_endpoint"]` → real Formspree ID (newsletter stays hidden until set)
   - Optional: `SITE["gtm_id"]` (Google tag), `plausible_domain`, or `ga4_id`
2. Push to GitHub → enable **Pages** → Source: **GitHub Actions**
3. Workflow rebuilds daily from live RSS (and on every push)

## Local preview

Open `docs/index.html` in a browser, or:

```bash
python -m http.server 8080 --directory docs
```
