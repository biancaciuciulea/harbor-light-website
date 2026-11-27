# Harbor Light — Pinterest ARC Campaign Pack

Complete conversion pack to recruit ARC readers for Harbor Soft Hour Books 1–4.

| File | Role |
|------|------|
| [ENGINE.md](./ENGINE.md) | **Agency pin engine** (Playwright, i18n, CSV, motion) |
| [pinterest_pin_engine.py](./pinterest_pin_engine.py) | CLI: `--lang` `--preview` `--motion` `--seed` `--formats` |
| [pins_i18n.json](./pins_i18n.json) | EN/DE/FR/ES/IT copy (no RO, no internal jargon) |
| [templates/](./templates/) | 5 HTML formats + `base.css` |
| [out/](./out/) | Generated PNG + bulk CSV |
| [README_RO.md](./README_RO.md) | Romanian step-by-step upload guide |
| [PIN_COPY.md](./PIN_COPY.md) | Legacy EN titles / A/B (prefer `pins_i18n.json`) |
| [LINK_MATRIX.md](./LINK_MATRIX.md) | Book × Lang → ARC URL + UTM |
| [BOARDS.md](./BOARDS.md) | Boards, cadence, 2-week schedule |
| [pins/](./pins/) | Legacy ready PNG pins 1000×1500 |
| [scripts/build_pins.py](./scripts/build_pins.py) | Legacy PIL re-compose (kept intact) |

**Live hub:** https://picubiancamaria.com/arc.html  

**Regenerate (engine):**  
`python pinterest_pin_engine.py --lang en --preview`  
`python pinterest_pin_engine.py --lang all`

**Regenerate (legacy PIL):** `python scripts/build_pins.py`
