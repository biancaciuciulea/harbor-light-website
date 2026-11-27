# ARC — Google Apps Script (GRATUIT): Sheet + email automat cititor + owner

**De ce:** Formspree Free **nu** are Autoresponse (email către cititor).  
**Soluția:** un Web App Google Apps Script care:

1. Înregistrează signup-ul în **Google Sheet** (registry automat)
2. Trimite **email cititorului** cu link EPUB (+ Send to Kindle + review) în limba paginii
3. Notifică **owner**-ul (și opțional oglindește în Formspree)

Cod gata de lipit: [`ops/arc_google_apps_script.js`](arc_google_apps_script.js)

---

## Ce merge ASTĂZI (fără deploy GAS)

| Funcție | Status |
|---------|--------|
| Formular ARC pe `/arc/bookN-lang.html` | ✅ live |
| Thank-you pe pagină + buton **Download EPUB** | ✅ live (AJAX `#arc-success`) |
| Înregistrare automată signup | ✅ **Formspree Submissions** (`mnppkppz`) — a fost mereu așa |
| Email notify către tine (owner) | ✅ Formspree (default) |
| Email automat către cititor cu link EPUB | ❌ **nu** pe Free Formspree — apare doar pe pagină |

Datele **au fost și sunt** înregistrate automat în Formspree → form `mnppkppz` → **Submissions**. Nu lipsea registry-ul; lipsea doar Autoresponse.

---

## Ce merge DUPĂ ~5 minute deploy GAS

| Funcție | Status |
|---------|--------|
| Tot ce e mai sus | ✅ |
| Row automat în **Google Sheet** | ✅ |
| **Email automat cititor** (EN/DE/FR/ES/IT) cu EPUB + Kindle + review | ✅ |
| Email notify owner din script | ✅ |
| Opțional: dual-post și către Formspree | ✅ (config `ARC_FORM_DUAL_FORMSPREE`) |

---

## Setup în 5 pași (RO)

### 1. Creează Sheet-ul

1. Deschide [Google Sheets](https://sheets.google.com) (contul cu care vrei să trimiți mailuri).
2. **Blank spreadsheet** → redenumește: `Harbor Light ARC Signups`.
3. Lasă primul tab; scriptul creează/umple header-ele pe foaia `ARC Signups`.

### 2. Lipeste scriptul

1. În Sheet: **Extensions → Apps Script**.
2. Șterge stub-ul `function myFunction…`.
3. Copiază tot din `ops/arc_google_apps_script.js` → Save (💾).
4. (Opțional) **Project Settings → Script properties**:
   - `OWNER_EMAIL` = `ing.biancaciuciulea@yahoo.com` (sau alt inbox)
   - `SHEET_NAME` = `ARC Signups` (default)

### 3. Deploy Web App

1. **Deploy → New deployment**
2. Tip: **Web app**
3. **Execute as:** Me  
4. **Who has access:** Anyone  
5. Deploy → autorizează contul Google (MailApp + Sheets)  
6. Copiază URL-ul care se termină în `/exec`  
   Exemplu: `https://script.google.com/macros/s/XXXXXXXX/exec`

### 4. Lipește URL-ul în site

În `harbor-light-website/config.py`:

```python
ARC_FORM_ENDPOINT = "https://script.google.com/macros/s/XXXXXXXX/exec"
ARC_FORM_DUAL_FORMSPREE = True   # True = GAS primary + oglindă Formspree; False = doar GAS
```

Apoi:

```bash
cd harbor-light-website
python generator.py
git add -A
git commit -m "Wire ARC form to Google Apps Script endpoint"
git push
```

### 5. Test rapid

1. Deschide o ediție live, ex. https://picubiancamaria.com/arc/book1-en.html  
2. Trimite cu un email pe care îl controlezi  
3. Verifică:
   - panel `#arc-success` + Download EPUB pe pagină  
   - email cititor (inbox + spam)  
   - email owner  
   - rând nou în Sheet  
   - (dacă dual) și Submission în Formspree  

---

## Arhitectură pe site

```
Browser AJAX
    → ARC_FORM_ENDPOINT (GAS)     [dacă e setat]
         → Sheet append
         → MailApp → cititor (localizat)
         → MailApp → owner
    → optional dual → Formspree mnppkppz
    → oricum: show #arc-success (EPUB pe pagină)

Dacă ARC_FORM_ENDPOINT e gol:
    → Formspree only (registry + owner; EPUB doar pe pagină)
```

Fără URL-ul tău `/exec` în `config.py`, site-ul **nu poate** trimite email magic — lipsa deploy-ului e singurul blocaj. Codul + pașii sunt gata; după paste URL + regenerate + push, auto-email-ul e live.

---

## Limite gratuite Google (orientativ)

- MailApp ~100 emailuri/zi (cont consumer) / mai multe pe Workspace  
- Suficient pentru ARC indie; dacă crești, mută pe Workspace sau queue

## Nu cumpăra Formspree Gold pentru asta

Autoresponse + Redirect pe Free rămân blocate. GAS acoperă email-ul cititorului + Sheet fără cost.
