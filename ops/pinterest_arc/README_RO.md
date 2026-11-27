# Ghid Pinterest ARC — Harbor Light (pas cu pas)

Pack: `harbor-light-website/ops/pinterest_arc/`  
Hub live: https://picubiancamaria.com/arc.html  

Scop: recrutezi cititori de **dark mafia slow burn** în ARC Team (EPUB gratuit + review onest). Nu vinzi spice rapid.

---

## 0) Înainte să postezi

1. Deschide folderul `pins/` — acolo sunt PNG-urile 1000×1500.  
2. Ține deschis `PIN_COPY.md` (titlu + descriere EN) și `LINK_MATRIX.md` (URL cu UTM).  
3. Cont Pinterest Business (sau Creator) → Analytics activ.  
4. Bio profil: `Dark mafia slow burn · Free ARC Team` + link la `https://picubiancamaria.com/arc.html`

---

## 1) Creează board-urile (o singură dată)

În Pinterest → **Create → Board**. Nume exact (sau aproape):

1. Dark Mafia Romance ARCs  
2. Slow Burn Romance Books  
3. Harbor Light Series  
4. Forced Proximity Romance  
5. Dual POV Dark Romance  
6. Free Romance ARCs & Reviewer Life  
7. Arranged Marriage Romance  
8. Morally Grey Heroes  

Setare: **Public**. Descriere scurtă pe board: *Dark mafia slow burn · free ARC · honest reviews · 18+*.

Detalii ce pin pe ce board: vezi `BOARDS.md`.

---

## 2) Cum uploadezi un pin (rețetă)

Pentru fiecare pin:

1. **Pin** → Create Pin (sau Upload).  
2. **Imagine:** alege fișierul din `pins/` (vezi tabelul de mai jos).  
3. **Title:** copiază din `PIN_COPY.md` (Primary sau o variantă A/B). Max ~100 caractere.  
4. **Description:** tot din `PIN_COPY.md` — include linia de filtrare *Slow burn — protocol before heat…*  
5. **Destination link:** URL-ul exact cu UTM din `PIN_COPY.md` / `LINK_MATRIX.md`.  
   - **NU** pune link Amazon pe pin.  
   - **NU** tăia parametrii `utm_…`.  
6. **Board:** board-ul principal din `BOARDS.md`.  
7. Publish. Opțional: „Also save to” încă 1–2 board-uri din mapă.

### Mapare rapidă imagine → ce copiezi

| Fișier PNG | Secțiune în PIN_COPY | Link tip |
|------------|----------------------|----------|
| `01_series_start_here.png` | SERIES — Start Here | `…/arc/book1-en.html?…utm_content=series` |
| `02_book1_bound_by_blood.png` | BOOK 1 | `…utm_content=book1` |
| `03_book2_soft_marks.png` | BOOK 2 | `…utm_content=book2` |
| `04_book3_soft_hour.png` | BOOK 3 | `…utm_content=book3` |
| `05_book4_soft_gate.png` | BOOK 4 | `…utm_content=book4` |
| `06_arc_team_recruit.png` | GENERIC — ARC Team | `…/arc.html?…utm_content=recruit` |
| `07_trope_dark_mafia.png` | TROPE Dark Mafia | `…book1-en…utm_content=trope_mafia` |
| `08_trope_slow_burn.png` | TROPE Slow Burn | `…trope_slowburn` |
| `09_trope_forced_proximity.png` | TROPE Forced Proximity | `…trope_proximity` |
| `10_trope_dual_pov.png` | TROPE Dual POV | `…trope_dualpov` |

---

## 3) Ce postezi ASTĂZI (top 3)

Ordinea exactă:

1. **`01_series_start_here.png`**  
   - Board: *Dark Mafia Romance ARCs*  
   - Title/Desc: SERIES Primary din `PIN_COPY.md`  
   - Link:  
     `https://picubiancamaria.com/arc/book1-en.html?utm_source=pinterest&utm_medium=pin&utm_campaign=arc_harbor&utm_content=series`

2. **`06_arc_team_recruit.png`**  
   - Board: *Free Romance ARCs & Reviewer Life*  
   - Title/Desc: Recruit Primary  
   - Link:  
     `https://picubiancamaria.com/arc.html?utm_source=pinterest&utm_medium=pin&utm_campaign=arc_harbor&utm_content=recruit`

3. **`08_trope_slow_burn.png`**  
   - Board: *Slow Burn Romance Books*  
   - Title/Desc: Slow Burn trope  
   - Link:  
     `https://picubiancamaria.com/arc/book1-en.html?utm_source=pinterest&utm_medium=pin&utm_campaign=arc_harbor&utm_content=trope_slowburn`

Apoi urmează calendarul din `BOARDS.md` (5–7 pinuri/săptămână).

---

## 4) Limbă / alte ediții

- Traficul Pinterest romance e predominant **EN** → pinurile din pack sunt EN.  
- Dacă vrei DE/FR/ES/IT/RO: aceeași imagine + titlu/desc tradus ușor + URL din `LINK_MATRIX.md` cu `utm_content=bookN-lang`.  
- Nu inventa pagini ARC care nu sunt pe hub (ex. Book 4 DE).

---

## 5) Cum urmărești rezultatele

1. **Google Analytics 4** (site-ul are deja tracking):  
   - Rapoarte → Acquisition → Session source/medium → `pinterest / pin`  
   - Filtrează `utm_campaign = arc_harbor`  
   - Compară `utm_content` (series / book1 / recruit / tropes)

2. **Pinterest Analytics:** impresii, saves, outbound clicks pe fiecare pin.

3. **ARC real:** email-uri Formspree / subject `ARC Team — …` sau Google Sheet (vezi `ops/ARC_GOOGLE_SHEETS_SETUP.md`).

4. După **14 zile:** păstrează top 2 tipuri de pin; schimbă titlurile A/B pe imaginea câștigătoare.

---

## 6) Reguli de conversie (nu le încălca)

- Link = **pagină ARC**, nu Amazon.  
- Scrie mereu **slow burn / protocol before heat**.  
- Scrie **honest reviews / stars not for sale**.  
- 18+.  
- Un job pe pin: *Join ARC* — nu aglomera Spotify/Gumroad/Amazon în același pin.

---

## 7) Regenerează imaginile (dacă schimbi cover-ele)

```bat
cd /d "D:\Romane romance\harbor-light-website\ops\pinterest_arc"
python scripts\build_pins.py
```

Covere sursă: `refs/bookN-en.jpg`. Fundaluri: `refs/bg_*.jpg`.

---

## Structură pack

```
ops/pinterest_arc/
  PIN_COPY.md          ← titluri, descrieri, A/B, hashtag-uri
  LINK_MATRIX.md       ← Book × Lang → URL UTM
  BOARDS.md            ← board-uri + calendar 2 săptămâni
  README_RO.md         ← acest ghid
  pins/                ← PNG 1000×1500 gata de upload
  refs/                ← covere + fundaluri
  scripts/build_pins.py
```
