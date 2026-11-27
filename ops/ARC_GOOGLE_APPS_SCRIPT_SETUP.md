# ARC — Google Apps Script (GRATUIT): Sheet + email automat

Cod gata de lipit (nimic de completat): [`ops/arc_google_apps_script.js`](arc_google_apps_script.js)  
Sheet ID deja în script: `1eA69Bg56IS4YS22htq4AlEUfVQgiv8IWXmW6HvrPfuw`  
Owner: `ing.biancaciuciulea@yahoo.com` (sau emailul Google activ)

---

## Lipire + Deploy (4 pași — nu schimba nimic)

1. Deschide Sheet-ul → **Extensions → Apps Script**
2. **Șterge tot** în `Cod.gs` → **lipește tot** fișierul `ops/arc_google_apps_script.js` → **nu schimba nimic** → **Save** (Ctrl+S / 💾)
3. **Deploy → New deployment** → tip **Web app**
   - **Execute as:** Eu (Me)
   - **Who has access:** Oricine (Anyone)
4. **Deploy** → autorizează → **copiază URL-ul `/exec`** și trimite-l (îl legăm pe site după)

Gata. Nu umple Script properties. Nu edita ID-ul. Nu edita emailul.

---

## Ce face după deploy

| Funcție | Status |
|---------|--------|
| Rând automat în Google Sheet | ✅ |
| Email cititor EN/DE/FR/ES/IT (EPUB + Kindle + review) | ✅ |
| Email notify owner | ✅ |
| Thank-you pe pagină (site) | ✅ deja live |

---

## După ce ai URL-ul `/exec`

Trimite URL-ul. Abia atunci se pune în `config.py` → `ARC_FORM_ENDPOINT` + `python generator.py` + push.  
**Nu legăm site-ul până nu ai `/exec`.**

Opțional dual Formspree: `ARC_FORM_DUAL_FORMSPREE = True`.

---

## Test rapid (după legare pe site)

1. https://picubiancamaria.com/arc/book1-en.html  
2. Trimite cu un email pe care îl controlezi  
3. Verifică: panel thank-you + email cititor + email owner + rând în Sheet  

---

## Limite gratuite Google

MailApp ~100 emailuri/zi (cont consumer). Suficient pentru ARC indie.

## Nu cumpăra Formspree Gold pentru asta

Autoresponse pe Free rămâne blocat. GAS acoperă email-ul cititorului + Sheet fără cost.
