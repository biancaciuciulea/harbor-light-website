#!/usr/bin/env python3
"""Sync DistroKid pack covers + lyrics into the site repo.

Source: E:\\Publicate distrokid (or MUSIC_PACKS_ROOT).
Writes:
  assets/music/covers/{slug}.jpg   (800px web JPEG)
  content/music/lyrics/{slug}.txt
  content/music/pack_meta.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

PACKS_ROOT = Path(os.environ.get("MUSIC_PACKS_ROOT", r"E:\Publicate distrokid"))
COVERS_OUT = ROOT / "assets" / "music" / "covers"
LYRICS_OUT = ROOT / "content" / "music" / "lyrics"
META_OUT = ROOT / "content" / "music" / "pack_meta.json"
ALBUM_TRACKS = ROOT / "content" / "music" / "album_tracks.json"
COVER_SIZE = 800
JPEG_QUALITY = 84


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_needed_titles() -> dict[str, str]:
    """title -> preferred slug."""
    needed: dict[str, str] = {}
    for track in config.MUSIC_TRACKS:
        title = track["title"]
        needed[title] = track.get("slug") or slugify(title)
    # Neon Tears radio edit also matches pack "Neon Tears"
    needed.setdefault("Neon Tears", "neon-tears-radio-edit")
    if ALBUM_TRACKS.is_file():
        data = json.loads(ALBUM_TRACKS.read_text(encoding="utf-8"))
        for album in data.values():
            for t in album.get("tracks") or []:
                title = (t.get("title") or "").strip()
                if title:
                    needed.setdefault(title, slugify(title))
    # Featured
    feat = (config.SITE.get("music_featured_track") or {}).get("title")
    if feat:
        needed.setdefault(feat, slugify(feat))
    return needed


def _title_from_folder(folder: Path) -> str:
    meta_path = folder / "metadata.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            title = (meta.get("title") or "").strip()
            if title:
                return title
        except (OSError, json.JSONDecodeError):
            pass
    tc = folder / "TuneCore"
    if tc.is_dir():
        for wav in tc.glob("*.wav"):
            return wav.stem
    return ""


def index_packs(root: Path) -> dict[str, Path]:
    """Index Publicate packs + sibling session folders on the same drive root."""
    by_title: dict[str, Path] = {}
    scan_roots = []
    if root.is_dir():
        scan_roots.append(root)
        # Also scan E:\ session hashes (Steel Heart Rising etc. live outside Publicate)
        parent = root.parent
        if parent.is_dir() and parent.drive:
            scan_roots.append(parent)
    for scan in scan_roots:
        try:
            children = list(scan.iterdir())
        except OSError:
            continue
        for folder in children:
            if not folder.is_dir():
                continue
            name_l = folder.name.lower()
            if name_l in {
                "$recycle.bin",
                "system volume information",
                "mafia_mist_01",
                "mafia_mist_02",
                "carti amazon",
                "carti tts",
                "inaudio",
                "wav_studio",
                "image_studio",
                "audio_mastered",
                "altele",
                "preview",
            }:
                continue
            if folder.name == "Publicate distrokid":
                continue
            # Publicate children or root session folders with metadata
            if scan == root or (folder / "metadata.json").is_file():
                title = _title_from_folder(folder)
                if title and title not in by_title:
                    by_title[title] = folder
            # one level deeper (track_a / track_b layouts)
            if scan != root:
                try:
                    for child in folder.iterdir():
                        if child.is_dir() and (child / "metadata.json").is_file():
                            title = _title_from_folder(child)
                            if title and title not in by_title:
                                by_title[title] = child
                except OSError:
                    pass
    # Prefer Publicate copies when both exist
    if root.is_dir():
        for folder in root.iterdir():
            if folder.is_dir():
                title = _title_from_folder(folder)
                if title:
                    by_title[title] = folder
    return by_title


def pick_cover(folder: Path) -> Path | None:
    for cand in (
        folder / "cover.jpg",
        folder / "spotify_cover_3000x3000.png",
        folder / "TuneCore" / "tunecore_cover_3000x3000.png",
        folder / "TuneCore" / "cover_3000x3000.png",
        folder / "youtube_thumbnail.jpg",
    ):
        if cand.is_file():
            return cand
    # any TuneCore cover png
    tc = folder / "TuneCore"
    if tc.is_dir():
        for p in tc.glob("*cover*.png"):
            return p
        for p in tc.glob("*cover*.jpg"):
            return p
    return None


def read_lyrics(folder: Path) -> str:
    for cand in (
        folder / "TuneCore" / "lyrics.txt",
        folder / "lyrics.txt",
    ):
        if cand.is_file():
            try:
                return cand.read_text(encoding="utf-8").strip()
            except OSError:
                pass
    meta_path = folder / "metadata.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            lyrics = (meta.get("lyrics") or "").strip()
            if lyrics:
                return lyrics
        except (OSError, json.JSONDecodeError):
            pass
    return ""


def write_cover_jpeg(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        im.thumbnail((COVER_SIZE, COVER_SIZE), Image.Resampling.LANCZOS)
        # pad to square canvas for clean cards
        canvas = Image.new("RGB", (COVER_SIZE, COVER_SIZE), (12, 12, 18))
        x = (COVER_SIZE - im.width) // 2
        y = (COVER_SIZE - im.height) // 2
        canvas.paste(im, (x, y))
        canvas.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)


def pack_extras(folder: Path) -> dict:
    meta: dict = {}
    meta_path = folder / "metadata.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            meta = {}
    return {
        "theme": meta.get("theme") or "",
        "style": meta.get("style") or "",
        "bpm": meta.get("bpm") or "",
        "folder_id": folder.name,
    }


def main() -> int:
    needed = load_needed_titles()
    packs = index_packs(PACKS_ROOT)
    print(f"packs_root={PACKS_ROOT} exists={PACKS_ROOT.is_dir()} indexed={len(packs)} needed={len(needed)}")

    COVERS_OUT.mkdir(parents=True, exist_ok=True)
    LYRICS_OUT.mkdir(parents=True, exist_ok=True)

    meta_out: dict[str, dict] = {}
    ok_cover = 0
    ok_lyrics = 0
    missing = []

    for title, slug in sorted(needed.items(), key=lambda x: x[0].lower()):
        folder = packs.get(title)
        # Neon Tears pack title vs release title
        if folder is None and title == "Neon Tears (Radio Edit)":
            folder = packs.get("Neon Tears")
        entry: dict = {
            "title": title,
            "slug": slug,
            "cover": f"assets/music/covers/{slug}.jpg",
            "lyrics_file": f"content/music/lyrics/{slug}.txt",
        }
        if folder is None:
            missing.append(title)
            # keep prior assets if present
            cover_path = COVERS_OUT / f"{slug}.jpg"
            lyrics_path = LYRICS_OUT / f"{slug}.txt"
            entry["has_cover"] = cover_path.is_file()
            entry["has_lyrics"] = lyrics_path.is_file() and lyrics_path.stat().st_size > 0
            meta_out[slug] = entry
            continue

        entry.update(pack_extras(folder))
        cover_src = pick_cover(folder)
        cover_dest = COVERS_OUT / f"{slug}.jpg"
        if cover_src:
            write_cover_jpeg(cover_src, cover_dest)
            entry["has_cover"] = True
            entry["cover_source"] = str(cover_src)
            ok_cover += 1
        else:
            entry["has_cover"] = cover_dest.is_file()

        lyrics = read_lyrics(folder)
        lyrics_dest = LYRICS_OUT / f"{slug}.txt"
        if lyrics:
            lyrics_dest.write_text(lyrics + "\n", encoding="utf-8")
            entry["has_lyrics"] = True
            entry["lyrics_lines"] = len([ln for ln in lyrics.splitlines() if ln.strip()])
            ok_lyrics += 1
        else:
            entry["has_lyrics"] = lyrics_dest.is_file() and lyrics_dest.stat().st_size > 0

        meta_out[slug] = entry

    META_OUT.parent.mkdir(parents=True, exist_ok=True)
    META_OUT.write_text(
        json.dumps(
            {
                "packs_root": str(PACKS_ROOT),
                "count": len(meta_out),
                "covers_synced": ok_cover,
                "lyrics_synced": ok_lyrics,
                "missing_packs": missing,
                "by_slug": meta_out,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"covers={ok_cover} lyrics={ok_lyrics} missing_packs={len(missing)}")
    if missing:
        print("missing:", ", ".join(missing[:20]))
    print(f"wrote {META_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
