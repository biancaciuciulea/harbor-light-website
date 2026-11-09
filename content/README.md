# Published storefront copy (source of truth for paste sheets)

Vendored from NovelTitan / studio packages so GitHub Pages does not invent Amazon/Gumroad text.

| Path | Source |
|------|--------|
| `amazon/bookN/{lang}.json` | `output/kdp_packages/mafia_mist_0N/{lang}/KDP_METADATA.json` |
| `amazon/bookN/{lang}.html` | `html_description` from that JSON |
| `gumroad/book1/{lang}.html` | `dark-romance-audiobook-studio/output_gumroad/{lang}/book1/.../DESCRIPTION.html` |

After publishing new KDP/Gumroad copy, re-sync these files, then run `python generator.py` (writes `docs/paste/`).
