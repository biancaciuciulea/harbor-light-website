#!/usr/bin/env python3
"""Fetch the 9D music YouTube playlist and map videos onto DistroKid catalog titles.

Writes content/music/youtube_playlist.json used by generator.py.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLuZYYTQk3kmQvcdY4rV5hN87xYVlGHKrb"
PLAYLIST_ID = "PLuZYYTQk3kmQvcdY4rV5hN87xYVlGHKrb"
OUT = ROOT / "content" / "music" / "youtube_playlist.json"

ALIASES = {
    "let the city lights guide your flow": "City Lights Flow",
    "neon tears": "Neon Tears (Radio Edit)",
    "rise from the ashe": "Rise from the Ashe",
}


def clean_title(title: str) -> str:
    t = title.strip()
    # Pattern: boilerplate then song at end
    m = re.search(
        r"9D\s*AUDIO.*?Use Headphones\)\s*(.+)$",
        t,
        flags=re.I,
    )
    if m and m.group(1).strip():
        t = m.group(1).strip()
    t = re.sub(r"^9D\s*AUDIO\s*[🎧]?\s*", "", t, flags=re.I)
    t = re.sub(r"[-–—|]*\s*Feel the music.*$", "", t, flags=re.I)
    t = re.sub(r"\(Use Headphones\)", "", t, flags=re.I)
    t = re.sub(r"\|\s*9D spatial.*$", "", t, flags=re.I)
    t = re.sub(r"\s*9D spatial.*$", "", t, flags=re.I)
    t = re.sub(r"^[-–—|:\s]+", "", t)
    t = re.sub(r"[-–—|:\s]+$", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" -–—|")
    key = t.lower()
    if key in ALIASES:
        return ALIASES[key]
    return t


def load_catalog() -> dict[str, str]:
    """lower title -> canonical title."""
    alb = json.loads((ROOT / "content/music/album_tracks.json").read_text(encoding="utf-8"))
    titles = set()
    for t in config.MUSIC_TRACKS:
        titles.add(t["title"])
    for a in alb.values():
        for t in a.get("tracks") or []:
            titles.add(t["title"])
    titles.add("Neon Tears")
    return {t.lower(): t for t in titles}


def fetch_playlist() -> list[dict]:
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--flat-playlist",
        "--print",
        "%(id)s\t%(title)s\t%(duration_string)s",
        PLAYLIST_URL,
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
    rows = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        vid, title, dur = line.split("\t", 2)
        rows.append({"id": vid, "title": title, "duration": dur})
    return rows


def main() -> int:
    catalog = load_catalog()
    rows = fetch_playlist()
    videos = []
    for r in rows:
        cleaned = clean_title(r["title"])
        match = catalog.get(cleaned.lower(), "")
        videos.append(
            {
                "id": r["id"],
                "url": f"https://youtu.be/{r['id']}",
                "title_raw": r["title"],
                "title_clean": cleaned,
                "duration": r["duration"],
                "matched_catalog": match,
                "is_9d_branded": bool(re.match(r"^\s*9D\s*AUDIO", r["title"], re.I)),
            }
        )

    by_match: dict[str, list] = {}
    unmatched_raw = []
    for v in videos:
        if v["matched_catalog"]:
            by_match.setdefault(v["matched_catalog"], []).append(v)
        else:
            unmatched_raw.append(v)

    preferred = {}
    for title, group in by_match.items():
        # Prefer clean Topic-style title (not 9D AUDIO prefix); else first
        plain = [g for g in group if not g["is_9d_branded"]]
        pick = plain[0] if plain else group[0]
        preferred[title] = {
            "youtube_id": pick["id"],
            "youtube_url": pick["url"],
            "youtube_title": pick["title_raw"],
            "duration": pick["duration"],
            "alts": [
                {
                    "youtube_id": g["id"],
                    "youtube_url": g["url"],
                    "youtube_title": g["title_raw"],
                }
                for g in group
                if g["id"] != pick["id"]
            ],
        }

    # Standalone YouTube-only tracks (not in DistroKid catalog), de-dupe by clean title
    standalone: dict[str, dict] = {}
    for v in unmatched_raw:
        key = (v["title_clean"] or v["title_raw"]).strip()
        if not key:
            continue
        # skip if this is just an alt of a matched song with empty clean
        existing = standalone.get(key.lower())
        if existing and existing.get("is_9d_branded") and not v["is_9d_branded"]:
            standalone[key.lower()] = {
                "title": key,
                "youtube_id": v["id"],
                "youtube_url": v["url"],
                "youtube_title": v["title_raw"],
                "duration": v["duration"],
                "is_9d_branded": v["is_9d_branded"],
            }
        elif key.lower() not in standalone:
            standalone[key.lower()] = {
                "title": key,
                "youtube_id": v["id"],
                "youtube_url": v["url"],
                "youtube_title": v["title_raw"],
                "duration": v["duration"],
                "is_9d_branded": v["is_9d_branded"],
            }

    payload = {
        "playlist_url": PLAYLIST_URL,
        "playlist_id": PLAYLIST_ID,
        "playlist_name": "Muzica 9d",
        "channel_name": "9D Pulse Prose",
        "channel_url": "https://www.youtube.com/@9DMusicPulse_Prose",
        "note": (
            "Playlist mixes 9D Pulse Prose uploads and Picu Bianca - Topic videos. "
            "Matched titles cross-link DistroKid/Apple catalog; unmatched are YouTube-only promotions."
        ),
        "video_count": len(videos),
        "matched_count": len(preferred),
        "standalone_count": len(standalone),
        "by_catalog_title": preferred,
        "standalone": sorted(standalone.values(), key=lambda x: x["title"].lower()),
        "all_videos": videos,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"videos={len(videos)} matched={len(preferred)} "
        f"standalone={len(standalone)} -> {OUT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
