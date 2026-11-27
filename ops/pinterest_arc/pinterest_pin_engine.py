#!/usr/bin/env python3
"""Agency-level Pinterest pin engine for Harbor Light ARC (EN/DE/FR/ES/IT).

Playwright HTML/CSS → PNG 1000×1500 (device_scale_factor=2).
Optional FFmpeg Ken Burns motion. Never RO. Never Amazon destinations.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
SITE_ROOT = ROOT.parents[1]  # harbor-light-website
TEMPLATES = ROOT / "templates"
I18N_PATH = ROOT / "pins_i18n.json"
BG_DIR = ROOT / "assets" / "backgrounds"
OUT_ROOT = ROOT / "out"
CSV_DIR = OUT_ROOT / "csv"
PREVIEW_DIR = OUT_ROOT / "_preview"
HARBOR_ASSETS = SITE_ROOT / "assets" / "harbor"
REFS = ROOT / "refs"

PIN_W, PIN_H = 1000, 1500
DEVICE_SCALE = 2
TARGET_PINS = 18
SITE_BASE = "https://picubiancamaria.com"
ACTIVE_LANGS = ("en", "de", "fr", "es", "it")

FORMATS = (
    "trope_map",
    "aesthetic_moodboard",
    "dialogue_quote",
    "kindle_mockup_pov",
    "binge_series",
)

BG_FILES = [
    "bg_01_harbor_rain.jpg",
    "bg_02_obsidian_ward.jpg",
    "bg_03_iron_contract.jpg",
    "bg_04_clinic_ember.jpg",
    "bg_05_steel_gaze_blur.jpg",
    "bg_06_series_silhouette.jpg",
]

# Prefer certain backgrounds per format (plan §7)
FORMAT_BG_PREF: dict[str, list[int]] = {
    "trope_map": [1, 2, 3],
    "aesthetic_moodboard": [0, 3, 5],
    "dialogue_quote": [1, 4],
    "kindle_mockup_pov": [2, 4],
    "binge_series": [5, 0],
}


@dataclass
class PinJob:
    lang: str
    format: str
    bg_id: int
    hook_id: int
    hook: str
    filename: str
    board_name: str
    title: str
    description: str
    alt_text: str
    destination_url: str
    book: int | None = None
    quote: str | None = None
    pov_label: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)


def _load_site_config() -> Any | None:
    """Import site config.py for ARC hubs / HARBOR_SERIES when available."""
    site = str(SITE_ROOT)
    if site not in sys.path:
        sys.path.insert(0, site)
    try:
        import config as site_config  # type: ignore

        return site_config
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] config.py import failed ({exc}); using fallback ARC paths")
        return None


def load_i18n() -> dict[str, Any]:
    data = json.loads(I18N_PATH.read_text(encoding="utf-8"))
    assert_no_jargon(data)
    return data


def assert_no_jargon(i18n: dict[str, Any]) -> None:
    """Fail fast if banned internal jargon leaks into pin copy."""
    ban = list(i18n.get("meta", {}).get("jargon_ban") or [])
    if not ban:
        ban = [
            "Quiet List",
            "Berths",
            "Holding squeeze",
            "Soft Gate weapon",
            "Glass Holding",
            "Obsidian Coven",
        ]
    # Check language packs only — exclude meta.jargon_ban itself
    scan = {k: v for k, v in i18n.items() if k != "meta"}
    blob = json.dumps(scan, ensure_ascii=False)
    hits = [term for term in ban if term.lower() in blob.lower()]
    if hits:
        raise SystemExit(f"Jargon ban hit in pins_i18n.json: {hits}")


def resolve_cover(book: int, lang: str) -> Path:
    """Resolve cover from assets/harbor, then refs, with EN fallback."""
    candidates = [
        HARBOR_ASSETS / f"book{book}-{lang}.jpg",
        HARBOR_ASSETS / f"book{book}-en.jpg",
        REFS / f"book{book}-{lang}.jpg",
        REFS / f"book{book}-en.jpg",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"No cover for book{book} lang={lang}")


def edition_exists(cfg: Any | None, book: int, lang: str) -> bool:
    if cfg is None:
        return lang == "en" and book in (1, 2, 3, 4)
    series = getattr(cfg, "HARBOR_SERIES", None) or []
    for entry in series:
        if int(entry.get("book") or 0) != book:
            continue
        for ed in entry.get("editions") or []:
            if str(ed.get("lang") or "").lower() == lang:
                return True
    return False


def arc_hub_path(cfg: Any | None, lang: str) -> str:
    if lang == "ro":
        lang = "en"
    if cfg is not None:
        fn = getattr(cfg, "arc_hub_path", None)
        if callable(fn):
            return str(fn(lang))
        paths = getattr(cfg, "ARC_HUB_PATHS", None) or {}
        if lang in paths:
            return str(paths[lang])
    fallback = {
        "en": "arc.html",
        "de": "de/arc.html",
        "fr": "fr/arc.html",
        "es": "es/arc.html",
        "it": "it/arc.html",
    }
    return fallback.get(lang, "arc.html")


def resolve_dest_url(
    cfg: Any | None,
    *,
    lang: str,
    fmt: str,
    pin_id: str,
    book: int | None = None,
) -> str:
    """Prefer deep /arc/bookN-lang.html when edition exists; else lang hub. Never Amazon/RO."""
    if lang == "ro":
        raise ValueError("RO is not an ARC/Pinterest language")

    path: str
    target_book = book
    if target_book is None and fmt == "kindle_mockup_pov":
        target_book = 1
    if target_book is None and fmt == "binge_series":
        target_book = 1

    if target_book and edition_exists(cfg, target_book, lang):
        path = f"arc/book{target_book}-{lang}.html"
    else:
        path = arc_hub_path(cfg, lang)

    query = urlencode(
        {
            "utm_source": "pinterest",
            "utm_medium": "organic",
            "utm_campaign": f"{fmt}_{pin_id}",
        }
    )
    return f"{SITE_BASE}/{path}?{query}"


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def build_matrix(
    i18n: dict[str, Any],
    cfg: Any | None,
    lang: str,
    *,
    seed: int = 42,
    formats_filter: list[str] | None = None,
    preview: bool = False,
) -> list[PinJob]:
    if lang not in ACTIVE_LANGS:
        raise ValueError(f"Unsupported lang {lang!r}; allowed {ACTIVE_LANGS}")

    rng = random.Random(seed)
    lang_pack = i18n[lang]
    boards = i18n["meta"]["boards"]
    formats = list(formats_filter or FORMATS)
    for f in formats:
        if f not in FORMATS:
            raise ValueError(f"Unknown format: {f}")

    if preview:
        # One pin per format for gallery QA
        jobs: list[PinJob] = []
        for i, fmt in enumerate(formats):
            jobs.append(
                _make_job(
                    i18n=i18n,
                    cfg=cfg,
                    lang=lang,
                    fmt=fmt,
                    bg_id=FORMAT_BG_PREF.get(fmt, [0])[0] % len(BG_FILES),
                    hook_id=0,
                    book=_default_book(fmt, 0),
                    boards=boards,
                    lang_pack=lang_pack,
                )
            )
        return jobs

    # Round-robin: each format ≥3 → 15, then +3 heroes
    slots: list[str] = []
    for _ in range(3):
        slots.extend(formats if formats_filter else list(FORMATS))
    heroes = ["trope_map", "binge_series", "kindle_mockup_pov"]
    for h in heroes:
        if h in formats:
            slots.append(h)
    slots = slots[:TARGET_PINS]

    bg_use = [0] * len(BG_FILES)
    hook_use: dict[str, list[int]] = {}
    seen: set[tuple[str, int, int]] = set()
    jobs = []

    for idx, fmt in enumerate(slots):
        pack = lang_pack["formats"][fmt]
        hooks = list(pack.get("hooks") or ["Harbor Light"])
        if fmt not in hook_use:
            hook_use[fmt] = [0] * len(hooks)

        # least-used preferred bg, with preference bias
        pref = FORMAT_BG_PREF.get(fmt, list(range(len(BG_FILES))))
        candidates = sorted(
            range(len(BG_FILES)),
            key=lambda b: (bg_use[b], 0 if b in pref else 1, rng.random()),
        )

        placed = False
        for bg_id in candidates:
            # least-used hook
            hook_id = min(range(len(hooks)), key=lambda h: (hook_use[fmt][h], rng.random()))
            key = (fmt, bg_id, hook_id)
            if key in seen:
                # try other hooks on same bg
                for alt_h in range(len(hooks)):
                    key2 = (fmt, bg_id, alt_h)
                    if key2 not in seen:
                        hook_id = alt_h
                        key = key2
                        break
                else:
                    continue
            seen.add(key)
            bg_use[bg_id] += 1
            hook_use[fmt][hook_id] += 1
            book = _default_book(fmt, idx)
            jobs.append(
                _make_job(
                    i18n=i18n,
                    cfg=cfg,
                    lang=lang,
                    fmt=fmt,
                    bg_id=bg_id,
                    hook_id=hook_id,
                    book=book,
                    boards=boards,
                    lang_pack=lang_pack,
                )
            )
            placed = True
            break
        if not placed:
            # force unique by bumping hook with synthetic index
            bg_id = idx % len(BG_FILES)
            hook_id = idx % max(1, len(hooks))
            while (fmt, bg_id, hook_id) in seen:
                hook_id = (hook_id + 1) % 97
            seen.add((fmt, bg_id, hook_id % len(hooks)))
            jobs.append(
                _make_job(
                    i18n=i18n,
                    cfg=cfg,
                    lang=lang,
                    fmt=fmt,
                    bg_id=bg_id,
                    hook_id=hook_id % len(hooks),
                    book=_default_book(fmt, idx),
                    boards=boards,
                    lang_pack=lang_pack,
                )
            )

    return jobs


def _default_book(fmt: str, idx: int) -> int | None:
    if fmt == "kindle_mockup_pov":
        return (idx % 4) + 1
    if fmt in ("dialogue_quote", "aesthetic_moodboard", "trope_map"):
        return 1 + (idx % 2)
    if fmt == "binge_series":
        return 1
    return None


def _make_job(
    *,
    i18n: dict[str, Any],
    cfg: Any | None,
    lang: str,
    fmt: str,
    bg_id: int,
    hook_id: int,
    book: int | None,
    boards: dict[str, str],
    lang_pack: dict[str, Any],
) -> PinJob:
    pack = lang_pack["formats"][fmt]
    hooks = list(pack.get("hooks") or ["Harbor Light"])
    hook = hooks[hook_id % len(hooks)]
    pin_id = f"{bg_id:02d}h{hook_id}"
    filename = f"{lang}_{fmt}_bg{bg_id:02d}_h{hook_id}.png"

    quote = None
    pov_label = None
    if fmt == "dialogue_quote":
        quotes = list(pack.get("quotes") or [])
        quote = quotes[hook_id % max(1, len(quotes))] if quotes else hook
    if fmt == "kindle_mockup_pov":
        labels = list(pack.get("pov_labels") or ["Dual POV"])
        pov_label = labels[hook_id % len(labels)]
        cycle = list(pack.get("book_cycle") or [1, 2, 3, 4])
        if book is None:
            book = cycle[hook_id % len(cycle)]

    seo_title = str(pack.get("seo_title") or hook)
    # Vary title slightly with hook for uniqueness in CSV
    title = f"{seo_title} · {hook}"[:100]
    description = str(pack.get("seo_desc") or "")
    alt_text = str(pack.get("alt") or title)
    dest = resolve_dest_url(cfg, lang=lang, fmt=fmt, pin_id=pin_id, book=book)

    return PinJob(
        lang=lang,
        format=fmt,
        bg_id=bg_id,
        hook_id=hook_id,
        hook=hook,
        filename=filename,
        board_name=str(boards.get(fmt) or "Harbor Light Series"),
        title=title,
        description=description,
        alt_text=alt_text,
        destination_url=dest,
        book=book,
        quote=quote,
        pov_label=pov_label,
    )


def render_html(job: PinJob, lang_pack: dict[str, Any], out_html: Path) -> Path:
    fmt = job.format
    pack = lang_pack["formats"][fmt]
    template = (TEMPLATES / f"{fmt}.html").read_text(encoding="utf-8")
    bg_path = BG_DIR / BG_FILES[job.bg_id]
    if not bg_path.exists():
        raise FileNotFoundError(f"Missing background: {bg_path}")

    ctx: dict[str, str] = {
        "lang": job.lang,
        "brand": str(lang_pack.get("brand") or "Picu Bianca-Maria"),
        "filter_line": str(lang_pack.get("filter_line") or ""),
        "bg_url": file_uri(bg_path),
        "cta": str(pack.get("cta") or "Free ARC →"),
        "eyebrow": str(pack.get("eyebrow") or "Harbor Light"),
        "hook": job.hook,
        "title": str(pack.get("title") or job.hook),
        "subtitle": str(pack.get("subtitle") or ""),
        "attribution": str(pack.get("attribution") or ""),
        "quote": job.quote or job.hook,
        "pov_label": job.pov_label or "Dual POV",
        "cover_url": "",
    }

    # Covers
    book = job.book or 1
    cover = resolve_cover(book, job.lang)
    ctx["cover_url"] = file_uri(cover)

    # Trope chips
    tropes_html_ready = list(pack.get("tropes") or [])
    # Mood tiles: bg + covers
    tiles = [
        file_uri(bg_path),
        file_uri(resolve_cover(1, job.lang)),
        file_uri(resolve_cover(2, job.lang)),
        file_uri(resolve_cover(min(3, 4), job.lang)),
    ]
    covers = [file_uri(resolve_cover(b, job.lang)) for b in (1, 2, 3, 4)]

    html = template
    # Simple mustache-ish replace for scalars
    for key, val in ctx.items():
        html = html.replace("{{ " + key + " }}", val)
        html = html.replace("{{" + key + "}}", val)

    # Jinja-lite loops
    html = _render_loop(html, "tropes", tropes_html_ready, item_key="trope")
    html = _render_loop(html, "tiles", tiles, item_key="tile")
    html = _render_loop(html, "covers", covers, item_key="cover")

    # Strip leftover {% if %} blocks simply
    html = re.sub(
        r"{%\s*if\s+attribution\s*%}(.*?){%\s*endif\s*%}",
        lambda m: m.group(1) if ctx.get("attribution") else "",
        html,
        flags=re.S,
    )

    out_html.parent.mkdir(parents=True, exist_ok=True)
    # Copy CSS beside HTML so relative link works
    css_src = TEMPLATES / "base.css"
    css_dst = out_html.parent / "base.css"
    if not css_dst.exists() or css_dst.read_bytes() != css_src.read_bytes():
        shutil.copy2(css_src, css_dst)
    out_html.write_text(html, encoding="utf-8")
    return out_html


def _render_loop(html: str, name: str, items: list[str], item_key: str) -> str:
    pattern = re.compile(
        rf"{{%\s*for\s+{item_key}\s+in\s+{name}\s*%}}(.*?){{%\s*endfor\s*%}}",
        re.S,
    )

    def repl(m: re.Match[str]) -> str:
        body = m.group(1)
        parts = []
        for item in items:
            chunk = body.replace("{{ " + item_key + " }}", item).replace(
                "{{" + item_key + "}}", item
            )
            parts.append(chunk)
        return "".join(parts)

    return pattern.sub(repl, html)


def screenshot_png(html_path: Path, png_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    png_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": PIN_W, "height": PIN_H},
            device_scale_factor=DEVICE_SCALE,
        )
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.locator(".pin").screenshot(path=str(png_path), type="png")
        browser.close()


def verify_dimensions(png_path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
    except ImportError:
        # Playwright device_scale_factor=2 → 2000×3000 native; accept either 1000 or 2000
        return (0, 0)
    with Image.open(png_path) as im:
        w, h = im.size
    # Prefer exact 1000×1500 for bulk upload; downscale if 2x
    if (w, h) == (PIN_W * DEVICE_SCALE, PIN_H * DEVICE_SCALE):
        im2 = Image.open(png_path)
        im2 = im2.resize((PIN_W, PIN_H), Image.Resampling.LANCZOS)
        im2.save(png_path, "PNG", optimize=True)
        w, h = PIN_W, PIN_H
    if (w, h) != (PIN_W, PIN_H):
        raise RuntimeError(f"Bad dimensions {w}x{h} for {png_path.name}; expected {PIN_W}x{PIN_H}")
    return w, h


def maybe_motion(png_path: Path, mp4_path: Path) -> bool:
    """8s Ken Burns 1000×1500. Returns False if ffmpeg missing."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("[motion] ffmpeg not on PATH — skipping")
        return False
    mp4_path.parent.mkdir(parents=True, exist_ok=True)
    # Zoompan Ken Burns: slow zoom + slight pan over 8s @ 30fps
    vf = (
        f"scale=1100:1650,zoompan=z='min(zoom+0.0004,1.08)':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=240:s={PIN_W}x{PIN_H}:fps=30"
    )
    cmd = [
        ffmpeg,
        "-y",
        "-loop",
        "1",
        "-i",
        str(png_path),
        "-vf",
        vf,
        "-t",
        "8",
        "-pix_fmt",
        "yuv420p",
        "-an",
        str(mp4_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or b"").decode("utf-8", errors="replace")[:400]
        print(f"[motion] ffmpeg failed for {png_path.name}: {err}")
        return False


def export_csv(jobs: list[PinJob], lang: str) -> Path:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    path = CSV_DIR / f"pinterest_bulk_upload_{lang}.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "filename",
                "board_name",
                "title",
                "description",
                "alt_text",
                "destination_url",
            ],
        )
        writer.writeheader()
        for job in jobs:
            if "amazon." in job.destination_url.lower():
                raise SystemExit(f"Amazon destination forbidden: {job.destination_url}")
            if "/arc/book" in job.destination_url and "-ro.html" in job.destination_url:
                raise SystemExit(f"RO destination forbidden: {job.destination_url}")
            writer.writerow(
                {
                    "filename": job.filename,
                    "board_name": job.board_name,
                    "title": job.title,
                    "description": job.description,
                    "alt_text": job.alt_text,
                    "destination_url": job.destination_url,
                }
            )
    return path


def write_preview_gallery(png_paths: list[Path]) -> Path:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    cards = []
    for p in png_paths:
        rel = p.name
        # copy into preview dir for self-contained gallery
        dest = PREVIEW_DIR / p.name
        if p.resolve() != dest.resolve():
            shutil.copy2(p, dest)
        cards.append(
            f'<figure><img src="{rel}" width="333" height="500" alt="{rel}" />'
            f"<figcaption>{rel}</figcaption></figure>"
        )
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>Pinterest Pin Preview</title>
<style>
body{{margin:0;background:#0B1220;color:#F4EFE6;font-family:Georgia,serif}}
h1{{padding:24px;font-size:28px}}
.grid{{display:flex;flex-wrap:wrap;gap:18px;padding:0 24px 48px}}
figure{{margin:0;width:333px}}
img{{display:block;width:100%;height:auto;border-radius:4px;box-shadow:0 8px 24px rgba(0,0,0,.45)}}
figcaption{{font-size:12px;margin-top:8px;opacity:.8;word-break:break-all}}
</style></head><body>
<h1>Harbor Light — Pin Engine Preview</h1>
<div class="grid">{"".join(cards)}</div>
</body></html>"""
    index = PREVIEW_DIR / "index.html"
    index.write_text(html, encoding="utf-8")
    return index


def render_jobs(
    jobs: list[PinJob],
    i18n: dict[str, Any],
    *,
    motion: bool = False,
    preview: bool = False,
) -> list[Path]:
    rendered: list[Path] = []
    work = OUT_ROOT / "_work"
    work.mkdir(parents=True, exist_ok=True)

    for job in jobs:
        lang_pack = i18n[job.lang]
        out_dir = PREVIEW_DIR if preview else (OUT_ROOT / job.lang)
        out_dir.mkdir(parents=True, exist_ok=True)
        html_path = work / f"{job.filename}.html"
        png_path = out_dir / job.filename
        print(f"  render {job.filename}")
        render_html(job, lang_pack, html_path)
        screenshot_png(html_path, png_path)
        verify_dimensions(png_path)
        if motion:
            maybe_motion(png_path, png_path.with_suffix(".mp4"))
        rendered.append(png_path)
    return rendered


def run_for_lang(
    lang: str,
    *,
    preview: bool,
    motion: bool,
    seed: int,
    formats: list[str] | None,
) -> dict[str, Any]:
    i18n = load_i18n()
    cfg = _load_site_config()
    jobs = build_matrix(
        i18n, cfg, lang, seed=seed, formats_filter=formats, preview=preview
    )
    print(f"[{lang}] {len(jobs)} pins (preview={preview})")
    paths = render_jobs(jobs, i18n, motion=motion, preview=preview)
    csv_path = export_csv(jobs, lang if not preview else f"{lang}_preview")
    return {"lang": lang, "count": len(paths), "paths": paths, "csv": csv_path, "jobs": jobs}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Harbor Light Pinterest pin engine")
    p.add_argument(
        "--lang",
        default="en",
        help="en|de|fr|es|it|all",
    )
    p.add_argument("--preview", action="store_true", help="One pin per format + gallery")
    p.add_argument("--motion", action="store_true", help="Optional 8s Ken Burns MP4")
    p.add_argument("--seed", type=int, default=42, help="Matrix RNG seed")
    p.add_argument(
        "--formats",
        default="",
        help="Comma filter: trope_map,aesthetic_moodboard,...",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fmt_filter = [f.strip() for f in args.formats.split(",") if f.strip()] or None

    if args.lang == "all":
        langs = list(ACTIVE_LANGS)
    else:
        lang = args.lang.lower()
        if lang == "ro":
            raise SystemExit("RO is forbidden for Pinterest ARC pins")
        if lang not in ACTIVE_LANGS:
            raise SystemExit(f"--lang must be one of {ACTIVE_LANGS + ('all',)}")
        langs = [lang]

    # Ensure chromium
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        raise SystemExit("Install playwright: pip install playwright && playwright install chromium")

    all_preview_paths: list[Path] = []
    summary: list[dict[str, Any]] = []

    for lang in langs:
        result = run_for_lang(
            lang,
            preview=args.preview,
            motion=args.motion,
            seed=args.seed,
            formats=fmt_filter,
        )
        summary.append(result)
        all_preview_paths.extend(result["paths"])

    if args.preview:
        gallery = write_preview_gallery(all_preview_paths)
        print(f"Preview gallery → {gallery}")

    print("\n=== Summary ===")
    for row in summary:
        print(f"  {row['lang']}: {row['count']} PNG → {row['csv']}")
        if row["jobs"]:
            sample = row["jobs"][0]
            print(
                f"    sample CSV: {sample.filename} | {sample.board_name} | {sample.destination_url}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
