# Pinterest Pin Engine (agency)

Modular Playwright HTML/CSS → PNG engine for Harbor Light ARC pins.

**Languages:** EN, DE, FR, ES, IT only — never RO.  
**Destinations:** ARC hub / deep `/arc/bookN-lang.html` + UTM — never Amazon.  
**Legacy pack:** `scripts/build_pins.py` + `pins/` remain intact.

## Layout

```
ops/pinterest_arc/
  pinterest_pin_engine.py
  pins_i18n.json
  templates/          # 5 formats + base.css
  assets/backgrounds/ # bg_01…bg_06 (+ Midjourney prompts in README)
  out/{lang}/         # PNG (+ optional MP4)
  out/csv/            # pinterest_bulk_upload_{lang}.csv
  out/_preview/       # --preview gallery
```

## Commands

```bat
cd /d "D:\Romane romance\harbor-light-website\ops\pinterest_arc"

pip install playwright pillow
playwright install chromium

python pinterest_pin_engine.py --lang en --preview
python pinterest_pin_engine.py --lang en
python pinterest_pin_engine.py --lang all
python pinterest_pin_engine.py --lang de --motion --seed 7
python pinterest_pin_engine.py --lang en --formats trope_map,binge_series
```

## Formats

| Format | Template |
|--------|----------|
| `trope_map` | Trope chips + hook |
| `aesthetic_moodboard` | 2×2 mood tiles |
| `dialogue_quote` | Quote + small cover |
| `kindle_mockup_pov` | Cover mockup + POV badge |
| `binge_series` | Books 1–4 row |

~18 unique pins/lang — uniqueness key `(format, bg, hook)`.

## Upgrades vs bare plan

- Imports `ARC_HUB_PATHS` / `HARBOR_SERIES` from site `config.py`
- Jargon ban-list assert before render
- `--preview` → `out/_preview/index.html`
- Post-render dimension check (1000×1500)
- Optional `--motion` Ken Burns MP4 (skips if no ffmpeg)

## CSV columns

`filename, board_name, title, description, alt_text, destination_url`

UTM: `utm_source=pinterest&utm_medium=organic&utm_campaign={format}_{id}`
