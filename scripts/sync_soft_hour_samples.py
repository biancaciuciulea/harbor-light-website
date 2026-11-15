#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync Soft Hour Chapter 1 free-text samples from annotated studio chapters.

Auto rule: for each live Soft Hour edition (gumroad or sample playlist in FEEDS),
if studio has input/annotated/bookN_ch01_{lang}.md, write content/samples/bookN-ch01-{lang}.md.

Then `python generator.py` embeds them on language landings + dedicated sample pages.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

STUDIO_ANN = ROOT.parent / "dark-romance-audiobook-studio" / "input" / "annotated"
OUT = ROOT / "content" / "samples"


def strip_annotated(raw: str) -> str:
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            raw = raw[end + 4 :]
    paras: list[str] = []
    title = "Chapter 1"
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("[") and s.endswith("]"):
            m = re.match(r"\[CHAPTER:\s*(\d+)\s*\|\s*(.+?)\]", s)
            if m:
                tit = m.group(2).strip().rstrip(".")
                title = f"Chapter {m.group(1)}: {tit}"
            continue
        if re.match(
            r"^(Chapter|Kapitel|Chapitre|Capítulo|Capitolo)\s+\d+\.",
            s,
            re.I,
        ):
            continue
        paras.append(s)
    return f"# {title}\n\n" + "\n\n".join(paras) + "\n"


def live_soft_hour_pairs() -> set[tuple[int, str]]:
    """(book, lang) pairs that have Soft Hour gumroad and/or sample playlist."""
    pairs: set[tuple[int, str]] = set()
    for book in config.HARBOR_SERIES:
        n = int(book.get("book") or 0)
        for ed in book.get("editions") or []:
            lang = str(ed.get("lang") or "").lower()
            if lang and ed.get("gumroad"):
                pairs.add((n, lang))
    for feed in config.FEEDS:
        lang_raw = str(feed.get("lang") or "").lower()
        book = int(feed.get("book") or 1)
        lang = lang_raw.split("-")[0]
        if feed.get("spotify_sample_playlist_url") or feed.get("gumroad_url"):
            if lang:
                pairs.add((book, lang))
    return pairs


def main() -> None:
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    skipped: list[str] = []
    for book, lang in sorted(live_soft_hour_pairs()):
        src = STUDIO_ANN / f"book{book}_ch01_{lang}.md"
        if not src.is_file():
            continue
        dest = OUT / f"book{book}-ch01-{lang}.md"
        # Preserve hand-curated site samples unless --force
        if dest.is_file() and not force:
            skipped.append(dest.name)
            continue
        text = strip_annotated(src.read_text(encoding="utf-8"))
        dest.write_text(text, encoding="utf-8")
        written.append(dest.name)
        print(f"OK {dest.name} · {len(text.split())} words")
    for name in skipped:
        print(f"skip existing {name} (use --force to overwrite)")
    if not written and not skipped:
        print("No Soft Hour sample sources found to sync.")
    else:
        print(f"Synced {len(written)} · skipped {len(skipped)}. Run: python generator.py")


if __name__ == "__main__":
    main()
