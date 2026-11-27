# ARC signups → registry (Formspree + optional Sheets / GAS)

**Goal:** every ARC submit is logged automatically — and, after a short free deploy, the reader also gets an email with the EPUB link.

---

## Ce e deja automat (fără setup extra)

| Layer | Where | Cost | Notes |
|-------|--------|------|--------|
| **Formspree Submissions** | Form `mnppkppz` → **Submissions** | Free | **Mereu ON.** Acesta *este* arhiva de signup. |
| **Owner notify** | Formspree email | Free | Default ON |
| **EPUB pe pagină** | `#arc-success` după AJAX | Free | Cititorul vede Download imediat |

Datele **au fost înregistrate automat** în Formspree de la început. Nu lipsea registry-ul.

---

## Email automat către cititor (FREE) — Google Apps Script

Formspree Free **nu** are Autoresponse. Calea preferată:

→ **[`ops/ARC_GOOGLE_APPS_SCRIPT_SETUP.md`](ARC_GOOGLE_APPS_SCRIPT_SETUP.md)**  
→ cod: [`ops/arc_google_apps_script.js`](arc_google_apps_script.js)

După deploy (~5 min): Sheet + email cititor (EN/DE/FR/ES/IT) + owner.  
`config.py` → `ARC_FORM_ENDPOINT` = URL `/exec` → `python generator.py` → push.

Opțional `ARC_FORM_DUAL_FORMSPREE = True` oglindește și în Formspree.

---

## Opțional: Formspree → Google Sheets Workflow

Dacă vrei Sheet **fără** Apps Script (doar registry, fără auto-email cititor):

1. [Formspree](https://formspree.io/forms) → form **`mnppkppz`**
2. **Workflow** → **+ Add New** → **Google Sheets**
3. Conectează Google → alege/creează spreadsheet → save

### Coloane utile

- timestamp, `first_name`, `email`
- `form_type`, `book` / `book_id`, `lang`, `asin`, `delivery_format`
- `age_18`, `honest_review`
- `epub_url`, `review_url`, `utm_*`

Filtru: `form_type` = `arc`.

---

## Ce vede cititorul

1. Alege book × limba pe hub → `/arc/bookN-lang.html`
2. Submit → rămâne pe site → **`#arc-success`**: Download EPUB + Send to Kindle + review
3. După GAS deploy: același link îi vine și pe **email** (limba paginii)

Exemplu Book 1 EN:

`https://picubiancamaria.com/arc-files/b1en-arc-7f3k9q2m/bound-by-blood-harbor-light-ARC.epub`

---

## Nu cumpăra Formspree Gold pentru asta

- **Autoresponse** — locked pe Free → GAS  
- **Custom Redirect** — locked pe Free → AJAX pe site  

## Test

1. https://picubiancamaria.com/arc.html → o ediție → submit  
2. `#arc-success` + Download  
3. Formspree Submissions / owner mail  
4. După GAS: inbox cititor + Sheet row  
