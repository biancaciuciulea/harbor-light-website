# ARC delivery files (Book 1 EN)

Source files copied into `docs/arc-files/<token>/` by `generator.py`.

- **Primary:** `*.epub` — Kindle / Apple Books / Kobo ARC default
- **Secondary:** `*-interior-6x9.pdf` — optional print-layout PDF

Do not link these URLs from nav, sitemap, or `llms.txt`.

**Client delivery (Free Formspree):** AJAX submit on `arc.html` → `#arc-success`
panel (Download EPUB + raw link). No paid Redirect / Autoresponse required.

**Registry:** Formspree Submissions (+ optional Google Sheets Workflow —
`ops/ARC_GOOGLE_SHEETS_SETUP.md`).

Rotate the token folder name if the link leaks widely.
