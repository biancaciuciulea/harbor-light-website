# ARC delivery files (Harbor Light · all book × lang)

`generator.py` copies KDP EPUBs (+ optional 6×9 PDF interiors) from
`output/kdp_packages/mafia_mist_0N/<lang>/` into `docs/arc-files/<token>/`.

- **Primary:** `*-ARC.epub` — Kindle / Apple Books / Kobo
- **Secondary:** `*-interior-6x9.pdf` — optional print-layout PDF when present
- **Hub:** `/arc.html` — picker (only editions with EPUB on disk)
- **Deep links:** `/arc/bookN-lang.html` — form → AJAX → download panel

Book 1 EN token is locked: `b1en-arc-7f3k9q2m` (do not rename — live links).

Do not link ARC file URLs from nav, sitemap body copy, or `llms.txt` catalogs.
`robots.txt` disallows `/arc-files/`.

**Client delivery (Free Formspree):** AJAX submit → `#arc-success`
(Download EPUB + optional PDF + Amazon review if ASIN + raw copyable URL).

Hidden fields: `form_type=arc`, `book`, `lang`, `asin`, `delivery_format=epub`.

**Registry:** Formspree Submissions (+ optional Google Sheets —
`ops/ARC_GOOGLE_SHEETS_SETUP.md`). No Gumroad.

The optional `arc_delivery/<token>/` mirror is legacy for Book 1 EN; build
source of truth is now the KDP package paths in `config.HARBOR_ARC`.
