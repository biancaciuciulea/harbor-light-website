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

Output → `docs/` (hub + `en/` `de/` `fr/` episode pages, sitemap, robots).

## Before first publish

1. Edit `config.py`:
   - `SITE["base_url"]` → your Pages URL  
     (`https://<user>.github.io/harbor-light-website`)
   - `SITE["formspree_endpoint"]` → free Formspree form ID
   - Optional: paste DE/FR `spotify_show_url` when you have them
2. Push to GitHub → enable **Pages** → Source: **GitHub Actions**
3. Workflow rebuilds daily from live RSS (and on every push)

## Local preview

Open `docs/index.html` in a browser, or:

```bash
python -m http.server 8080 --directory docs
```
