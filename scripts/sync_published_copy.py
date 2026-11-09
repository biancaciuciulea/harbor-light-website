#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vendor published Gumroad + Spotify paste packs into content/ for the site generator."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT.parent / "dark-romance-audiobook-studio"
GUM_ROOT = STUDIO / "output_gumroad"
MKT = STUDIO / "output_marketing"
CONTENT_GUM = ROOT / "content" / "gumroad"
CONTENT_SPOT = ROOT / "content" / "spotify"
LANGS = ("en", "de", "fr", "es", "it")


def _extract_block(section: str, label: str) -> str:
    pat = rf">>> COPY BEGIN — {re.escape(label)}\r?\n(.*?)\r?\n>>> COPY END — {re.escape(label)}"
    m = re.search(pat, section, re.S)
    return m.group(1).strip() if m else ""


def _book1_section(text: str, lang: str) -> str:
    for m in re.finditer(
        r"^##############################################################################\r?\n# BOOK (\d+) · ([A-Z]{2}) ·",
        text,
        re.M,
    ):
        if int(m.group(1)) != 1 or m.group(2) != lang.upper():
            continue
        nxt = re.search(
            r"^##############################################################################\r?\n# BOOK ",
            text[m.end() :],
            re.M,
        )
        end = m.end() + nxt.start() if nxt else len(text)
        return text[m.start() : end]
    return ""


def sync_gumroad() -> list[str]:
    copied: list[str] = []
    CONTENT_GUM.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        meta_dir = GUM_ROOT / lang / "book1" / "GUMROAD_PRODUCT" / "02_metadata"
        if not meta_dir.is_dir():
            continue
        dest = CONTENT_GUM / "book1" / lang
        dest.mkdir(parents=True, exist_ok=True)
        for name in (
            "DESCRIPTION.html",
            "FIELDS.json",
            "RECEIPT_PASTE.md",
            "GUMROAD_PRODUCT.md",
        ):
            src = meta_dir / name
            if src.is_file():
                shutil.copy2(src, dest / name)
                copied.append(f"gumroad/book1/{lang}/{name}")
        desc = meta_dir / "DESCRIPTION.html"
        if desc.is_file():
            shutil.copy2(desc, CONTENT_GUM / "book1" / f"{lang}.html")
        mkt_md = MKT / lang / "book1" / "GUMROAD_PRODUCT.md"
        if mkt_md.is_file():
            shutil.copy2(mkt_md, dest / "GUMROAD_PRODUCT_marketing.md")
            copied.append(f"gumroad/book1/{lang}/GUMROAD_PRODUCT_marketing.md")
    return copied


def sync_spotify() -> list[str]:
    copied: list[str] = []
    CONTENT_SPOT.mkdir(parents=True, exist_ok=True)
    master = MKT / "SPOTIFY_UPLOAD_ALL_BOOKS_LANGS.txt"
    if master.is_file():
        shutil.copy2(master, CONTENT_SPOT / "SPOTIFY_UPLOAD_ALL_BOOKS_LANGS.txt")
        copied.append("spotify/SPOTIFY_UPLOAD_ALL_BOOKS_LANGS.txt")
        text = master.read_text(encoding="utf-8")
    else:
        text = ""

    for lang in LANGS:
        section = _book1_section(text, lang) if text else ""
        dest = CONTENT_SPOT / "book1" / lang
        dest.mkdir(parents=True, exist_ok=True)

        show_name = _extract_block(section, "SHOW NAME") if section else ""
        show_desc = _extract_block(section, "SHOW DESCRIPTION") if section else ""
        titles = re.findall(
            r">>> COPY BEGIN — EPISODE TITLE\r?\n(.*?)\r?\n>>> COPY END — EPISODE TITLE",
            section,
            re.S,
        )
        descs = re.findall(
            r">>> COPY BEGIN — EPISODE DESCRIPTION / SHOW NOTES\r?\n(.*?)\r?\n>>> COPY END — EPISODE DESCRIPTION / SHOW NOTES",
            section,
            re.S,
        )
        tags = re.findall(
            r">>> COPY BEGIN — TAGS\r?\n(.*?)\r?\n>>> COPY END — TAGS",
            section,
            re.S,
        )
        payload = {
            "book": 1,
            "lang": lang,
            "show_name": show_name,
            "show_description": show_desc,
            "trailer_title": titles[0].strip() if titles else "",
            "trailer_description": descs[0].strip() if descs else "",
            "trailer_tags": tags[0].strip() if tags else "",
            "ch01_title": titles[1].strip() if len(titles) > 1 else "",
            "ch01_description": descs[1].strip() if len(descs) > 1 else "",
            "ch01_tags": tags[1].strip() if len(tags) > 1 else "",
            "source_note": "Parsed from SPOTIFY_UPLOAD_ALL_BOOKS_LANGS.txt",
        }
        (dest / "show.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (dest / "SHOW_NAME.txt").write_text(show_name + "\n", encoding="utf-8")
        (dest / "SHOW_DESCRIPTION.txt").write_text(show_desc + "\n", encoding="utf-8")
        if payload["trailer_title"]:
            (dest / "TRAILER.txt").write_text(
                f"Title: {payload['trailer_title']}\n\n"
                f"{payload['trailer_description']}\n\n"
                f"Tags: {payload['trailer_tags']}\n",
                encoding="utf-8",
            )
        if payload["ch01_title"]:
            (dest / "CH01.txt").write_text(
                f"Title: {payload['ch01_title']}\n\n"
                f"{payload['ch01_description']}\n\n"
                f"Tags: {payload['ch01_tags']}\n",
                encoding="utf-8",
            )
        copied.append(f"spotify/book1/{lang}/show.json")

        src_dir = MKT / lang / "book1"
        if src_dir.is_dir():
            ep_dest = dest / "episodes"
            ep_dest.mkdir(parents=True, exist_ok=True)
            for md in sorted(src_dir.glob("SPOTIFY_*.md")):
                shutil.copy2(md, ep_dest / md.name)
                copied.append(f"spotify/book1/{lang}/episodes/{md.name}")
            for social in ("SOCIAL_FACEBOOK.txt", "SOCIAL_TIKTOK.txt"):
                s = src_dir / social
                if s.is_file():
                    shutil.copy2(s, dest / social)
                    copied.append(f"spotify/book1/{lang}/{social}")
    return copied


def main() -> int:
    if not STUDIO.is_dir():
        print(f"Studio not found: {STUDIO}")
        return 1
    copied = sync_gumroad() + sync_spotify()
    print(f"Synced {len(copied)} files into content/")
    for c in copied[:30]:
        print(f"  {c}")
    if len(copied) > 30:
        print(f"  … +{len(copied) - 30} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
