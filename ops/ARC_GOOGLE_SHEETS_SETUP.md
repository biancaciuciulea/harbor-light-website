# ARC signups → Google Sheets (Formspree Free)

**Goal:** every ARC form submit on https://picubiancamaria.com/arc.html is logged as a Sheet row automatically — no paid Formspree Autoresponse / Redirect needed.

Form endpoint: `mnppkppz`  
Client already gets the EPUB on-page via AJAX thank-you (`#arc-success`).  
Owner already gets Formspree notify email.  
This doc = optional spreadsheet registry on top of Formspree Submissions.

---

## Registry options (pick what you need)

| Layer | Where | Cost | Notes |
|-------|--------|------|--------|
| **1. Formspree Submissions** | Formspree → form `mnppkppz` → **Submissions** | Free | Already on. This *is* the signup archive. |
| **2. Google Sheets (Workflow)** | Formspree → **Workflow** → Google Sheets | Free | Auto-rows; connect Google once in UI. |
| **3. Site JSON** | `data/arc_signups.json` | — | **Not possible** from a static GitHub Pages site alone (no backend write). |

Best free combo: **AJAX thank-you (client)** + **Formspree Submissions (archive)** + **Sheets Workflow (spreadsheet)**.

---

## 3 clicks — connect Google Sheets

1. Open [Formspree](https://formspree.io/forms) → form **`mnppkppz`**.
2. Open **Workflow** (or **Integrations**) → **+ Add New** → **Google Sheets**.
3. Connect your Google account → pick/create a spreadsheet (e.g. `ARC Harbor Light Book1`) → save.

After that, each submit appends a row (name, email, country, profile, checkboxes, `form_type=arc_book1_en`, `epub_url`, etc.).

### Useful columns to keep

- `submitted_at` / Formspree timestamp  
- `name`, `email`, `country`, `reader_profile`  
- `form_type`, `book`, `asin`, `delivery_format`  
- `age_18`, `honest_review`, `slow_burn_ok`  
- `epub_url` (raw link also shown to the client on-page)

Filter tip: only rows where `form_type` = `arc_book1_en` (same form may get newsletter/other site posts).

---

## What the reader sees (no Sheets required)

1. Submit on `/arc.html`
2. Stay on site → panel **`#arc-success`**: big **Download EPUB** + raw copyable URL  
3. Owner email notify from Formspree (default)

EPUB URL:

`https://picubiancamaria.com/arc-files/b1en-arc-7f3k9q2m/bound-by-blood-harbor-light-ARC.epub`

---

## Free-plan limits (do not buy Formspree for these)

- **Autoresponse** (email-to-client with link) — locked on Free → we use on-page thank-you instead  
- **Custom Redirect** (`_next`) — locked on Free → AJAX `fetch` keeps the user on our page  

Sheets Workflow + Submissions archive are enough for “înregistrezi automat”.

---

## Optional later: email-to-client with Apps Script

Only if you insist the link must also arrive by email without Formspree Gold:

1. Deploy a Google Apps Script web app that accepts POST  
2. Point the ARC form `action` at that URL (or dual-post)  
3. Script: append Sheet → `MailApp.sendEmail` to client with EPUB URL → optional notify owner  

Stub / deploy steps can live in `ops/ARC_APPS_SCRIPT_STUB.md` if needed. Prefer AJAX thank-you first.

---

## Test checklist

1. Open https://picubiancamaria.com/arc.html  
2. Submit with a real email you control  
3. Confirm `#arc-success` appears with Download + raw link (no Formspree thank-you redirect)  
4. Confirm owner Formspree inbox / email notify  
5. Confirm Submissions list has the row  
6. If Sheets Workflow connected: confirm new row in the spreadsheet  
