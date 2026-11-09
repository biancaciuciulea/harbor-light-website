# Published storefront copy (source of truth for paste sheets)

Vendored from NovelTitan / studio packages so GitHub Pages does not invent Amazon / Gumroad / Spotify text.

| Path | Source |
|------|--------|
| `amazon/bookN/{lang}.json` | `output/kdp_packages/mafia_mist_0N/{lang}/KDP_METADATA.json` |
| `amazon/bookN/{lang}.html` | `html_description` from that JSON |
| `gumroad/book1/{lang}/` | `dark-romance-audiobook-studio/output_gumroad/{lang}/book1/.../02_metadata/` |
| `spotify/SPOTIFY_UPLOAD_ALL_BOOKS_LANGS.txt` | studio `output_marketing/` Spotify master |
| `spotify/book1/{lang}/` | show/trailer/ch01 + episode MD + social paste |

## Refresh

```bat
cd dark-romance-audiobook-studio
python -u scripts/build_spotify_upload_master.py

cd ..\harbor-light-website
python scripts/sync_published_copy.py
python generator.py
```

Then commit + push `docs/` so Pages redeploys.
