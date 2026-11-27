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

Output → `docs/` (author hub + `about.html` + `faq.html` + `llms.txt` + Harbor Light series + `de.html`/`fr.html`/`es.html`/`it.html` landings + `en/` `de/` `fr/` `es/` `it/` shows + `tech-books.html` + `music.html`, sitemap, robots).

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

## GA4 Data API (weekly email report)

1. Enable **Google Analytics Data API** in Google Cloud
2. Create a **service account**, download JSON → `secrets/ga4-service-account.json`
3. In GA4 → Admin → **Property access management**, add that service-account email as **Viewer**
4. Copy numeric **Property ID** (Admin → Property settings) into `.env` (see `.env.example`)
5. Optional SMTP in `.env` for email (Gmail App Password)
6. Run:

```bash
pip install -r requirements.txt
python scripts/ga4_weekly_report.py
python scripts/ga4_weekly_report.py --email
```

GitHub Action `ga4-weekly-report.yml` runs Mondays if these secrets exist:
`GA4_PROPERTY_ID`, `GA4_SA_JSON`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `REPORT_FROM`, `REPORT_TO`.

## ARC signup — ce e automat (RO)

Hub-uri: `/arc.html` · `/de/arc.html` · `/fr/arc.html` · `/es/arc.html` · `/it/arc.html`

### Astăzi (fără setup extra)

- **Datele se înregistrează automat** în Formspree → form `mnppkppz` → **Submissions** (așa a fost mereu).
- Owner primește notify Formspree.
- Cititorul vede **Download EPUB** pe pagină (`#arc-success` după AJAX).
- Formspree Free **nu** trimite Autoresponse (email cu link) — asta e limitarea planului, nu un bug.

### După ~5 min deploy Google Apps Script (GRATUIT)

- Sheet registry + **email automat cititorului** (EN/DE/FR/ES/IT) cu EPUB + Send to Kindle + review
- Email owner din script
- Opțional dual-post către Formspree (`ARC_FORM_DUAL_FORMSPREE = True`)

Pași: [`ops/ARC_GOOGLE_APPS_SCRIPT_SETUP.md`](ops/ARC_GOOGLE_APPS_SCRIPT_SETUP.md)  
Cod: [`ops/arc_google_apps_script.js`](ops/arc_google_apps_script.js)  
Apoi în `config.py`:

```python
ARC_FORM_ENDPOINT = "https://script.google.com/macros/s/XXXX/exec"
```

`python generator.py` → push. Fără URL-ul `/exec`, auto-email-ul nu poate porni magie — site-ul e pregătit; lipsește doar deploy-ul tău.

## Formspree newsletter count (optional)

Site form endpoint is already live: `SITE["formspree_endpoint"]` → `https://formspree.io/f/mnppkppz`
(templates `base.html` / `home.html`). ARC folosește același form ca fallback / dual mirror.

To let scripts pull submission counts (not just the dashboard):

1. Formspree → form **mnppkppz** → **Settings** → enable **HTTP API**
2. Copy the **Read-only** API key into `.env` as `FORMSPREE_API_KEY` (see `.env.example`)
3. Run: `python scripts/formspree_status.py`

**Plan note:** Formspree Submissions API is **Professional/Business** only. On Free, open the Formspree inbox and count there — do not invent keys.

## Spotify plays (manual)

RSS feeds in `config.py` (`FEEDS[].rss`) power the site only — they do **not** expose play counts.
Spotify Web API has **no** official creator “episode plays” scope. Use [Spotify for Creators](https://creators.spotify.com) → each show → Analytics (CSV export OK). No Spotify OAuth secrets exist in this repo.
