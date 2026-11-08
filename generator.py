#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harbor Light — static site generator from Spotify/Anchor RSS feeds.

Fetches EN/DE/FR (and any feed in config.FEEDS), writes SEO-friendly HTML
into docs/ for GitHub Pages.

  python generator.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedparser
from jinja2 import Environment, FileSystemLoader, select_autoescape

import config

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
ASSETS_SRC = ROOT / "assets"
OUT = ROOT / config.OUTPUT_DIR

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, *, fallback: str = "episode") -> str:
    s = (text or "").lower().strip()
    s = _SLUG_RE.sub("-", s).strip("-")
    return (s[:80] or fallback)


def strip_html(raw: str) -> str:
    text = html.unescape(_TAG_RE.sub(" ", raw or ""))
    return _WS_RE.sub(" ", text).strip()


def truncate(text: str, n: int) -> str:
    text = (text or "").strip()
    if len(text) <= n:
        return text
    cut = text[: n - 1].rsplit(" ", 1)[0]
    return (cut or text[: n - 1]).rstrip(".,;:") + "…"


def rfc2822_to_iso(entry: dict[str, Any]) -> str:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return ""
    try:
        dt = datetime(*parsed[:6], tzinfo=timezone.utc)
        return dt.date().isoformat()
    except Exception:
        return ""


def rfc2822_display(entry: dict[str, Any]) -> str:
    iso = rfc2822_to_iso(entry)
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso).strftime("%b %d, %Y")
    except Exception:
        return iso


def enclosure_url(entry: dict[str, Any]) -> str:
    encs = entry.get("enclosures") or []
    if encs:
        href = encs[0].get("href") or ""
        if href:
            return href
    for link in entry.get("links") or []:
        if link.get("rel") == "enclosure" and link.get("href"):
            return link["href"]
    return ""


def feed_image_url(feed: Any, entry: dict[str, Any] | None = None) -> str:
    if entry:
        img = entry.get("image")
        if isinstance(img, dict) and img.get("href"):
            return img["href"]
        if isinstance(img, str) and img.startswith("http"):
            return img
    image = getattr(feed, "image", None) if feed else None
    if isinstance(image, dict) and image.get("href"):
        return image["href"]
    if image is not None and getattr(image, "href", None):
        return image.href
    itunes = getattr(feed, "itunes_image", None) if feed else None
    if isinstance(itunes, dict) and itunes.get("href"):
        return itunes["href"]
    return ""


def sort_key(ep: dict[str, Any]) -> tuple:
    """Trailers first, then episode number ascending, then date."""
    is_trailer = 0 if ep.get("episode_type") == "trailer" else 1
    num = ep.get("episode_number")
    num_key = int(num) if isinstance(num, int) else 10_000
    return (is_trailer, num_key, ep.get("published_iso") or "")


def parse_episode(entry: dict[str, Any], *, lang: str, used_slugs: set[str]) -> dict[str, Any]:
    title = (entry.get("title") or "Untitled").strip()
    summary_html = entry.get("summary") or entry.get("description") or ""
    plain = truncate(strip_html(summary_html), config.META_DESCRIPTION_LEN)
    ep_type = (entry.get("itunes_episodetype") or "full").lower()
    raw_num = entry.get("itunes_episode")
    try:
        ep_num = int(raw_num) if raw_num not in (None, "") else None
    except (TypeError, ValueError):
        ep_num = None

    if ep_type == "trailer":
        base = f"{lang}-trailer"
    elif ep_num is not None:
        base = f"{lang}-episode-{ep_num}"
    else:
        base = f"{lang}-{slugify(title)}"

    slug = base
    i = 2
    while slug in used_slugs:
        slug = f"{base}-{i}"
        i += 1
    used_slugs.add(slug)
    filename = f"{slug}.html"

    spotify_url = (entry.get("link") or "").strip()
    # Prefer open.spotify.com when Anchor already redirects there in link field
    if "podcasters.spotify.com" in spotify_url:
        # Keep as-is — still a valid listen CTA
        pass

    return {
        "lang": lang,
        "title": title,
        "slug": slug,
        "filename": filename,
        "summary_html": summary_html,
        "plain_summary": plain or title,
        "audio_url": enclosure_url(entry),
        "spotify_url": spotify_url,
        "duration": entry.get("itunes_duration") or "",
        "episode_type": ep_type,
        "episode_number": ep_num,
        "guid": entry.get("id") or "",
        "published_iso": rfc2822_to_iso(entry),
        "published_display": rfc2822_display(entry),
        "image": feed_image_url(None, entry),
    }


def _parse_rss(url: str) -> Any:
    """Fetch RSS as bytes first — more reliable than feedparser URL fetch on Anchor."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "HarborLightSiteGenerator/1.0 (+https://github.com/)"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    return feedparser.parse(raw)


def fetch_show(feed_cfg: dict[str, str]) -> dict[str, Any]:
    lang = feed_cfg["lang"]
    url = feed_cfg["rss"]
    try:
        parsed = _parse_rss(url)
    except Exception as exc:
        print(f"WARN {lang}: fetch failed → {exc}")
        parsed = feedparser.parse(url)

    if getattr(parsed, "bozo", False) and not parsed.entries:
        print(f"WARN {lang}: RSS not ready / invalid XML → {url}")
        return {
            "lang": lang,
            "label": feed_cfg.get("label") or lang.upper(),
            "rss": url,
            "ok": False,
            "title": feed_cfg.get("label") or lang.upper(),
            "description": "",
            "image": "",
            "link": feed_cfg.get("spotify_show_url") or "",
            "spotify_show_url": feed_cfg.get("spotify_show_url") or "",
            "gumroad_url": feed_cfg.get("gumroad_url") or "",
            "amazon_url": feed_cfg.get("amazon_url") or "",
            "episodes": [],
            "error": str(getattr(parsed, "bozo_exception", "empty feed")),
        }

    used: set[str] = set()
    episodes = [parse_episode(e, lang=lang, used_slugs=used) for e in parsed.entries]
    episodes.sort(key=sort_key)
    # Fill missing images from feed
    fimg = feed_image_url(parsed.feed)
    for ep in episodes:
        if not ep["image"]:
            ep["image"] = fimg

    desc = strip_html(parsed.feed.get("summary") or parsed.feed.get("description") or "")
    return {
        "lang": lang,
        "label": feed_cfg.get("label") or lang.upper(),
        "rss": url,
        "ok": True,
        "title": parsed.feed.get("title") or feed_cfg.get("label") or lang.upper(),
        "description": desc,
        "image": fimg,
        "link": parsed.feed.get("link") or feed_cfg.get("spotify_show_url") or "",
        "spotify_show_url": feed_cfg.get("spotify_show_url")
        or parsed.feed.get("link")
        or "",
        "gumroad_url": feed_cfg.get("gumroad_url") or "",
        "amazon_url": feed_cfg.get("amazon_url") or "",
        "episodes": episodes,
        "error": "",
    }


def episode_jsonld(ep: dict[str, Any], site: dict[str, Any], show: dict[str, Any]) -> str:
    lang = show["lang"]
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "name": ep["title"],
        "description": ep["plain_summary"],
        "datePublished": ep["published_iso"] or None,
        "url": f"{site['base_url']}/{lang}/{ep['filename']}",
        "inLanguage": lang,
        "author": {"@type": "Person", "name": site["author"]},
        "partOfSeries": {
            "@type": "PodcastSeries",
            "name": show["title"],
            "url": f"{site['base_url']}/{lang}/",
        },
    }
    if ep.get("audio_url"):
        data["associatedMedia"] = {
            "@type": "MediaObject",
            "contentUrl": ep["audio_url"],
            "encodingFormat": "audio/mpeg",
        }
    if ep.get("duration"):
        data["duration"] = ep["duration"]
    if ep.get("episode_number") is not None:
        data["episodeNumber"] = ep["episode_number"]
    return json.dumps({k: v for k, v in data.items() if v is not None}, ensure_ascii=False, indent=2)


def series_jsonld(show: dict[str, Any], site: dict[str, Any]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "PodcastSeries",
        "name": show["title"],
        "description": show["description"] or site["tagline"],
        "url": f"{site['base_url']}/{show['lang']}/",
        "author": {"@type": "Person", "name": site["author"]},
        "inLanguage": show["lang"],
    }
    if show.get("image"):
        data["image"] = show["image"]
    if show.get("spotify_show_url"):
        data["sameAs"] = [show["spotify_show_url"]]
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_site_ctx(show: dict[str, Any] | None = None) -> dict[str, Any]:
    site = dict(config.SITE)
    if show:
        site = {
            **site,
            "spotify_show_url": show.get("spotify_show_url") or site.get("spotify_show_url", ""),
            "gumroad_url": show.get("gumroad_url") or "",
            "amazon_url": show.get("amazon_url") or "",
            "default_og_image": show.get("image") or "",
            "language": show["lang"],
        }
    return site


def render_all(shows: list[dict[str, Any]]) -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    assets_out = OUT / "assets"
    if ASSETS_SRC.is_dir():
        shutil.copytree(ASSETS_SRC, assets_out)
    else:
        assets_out.mkdir()

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    year = datetime.now(timezone.utc).year
    root_index = env.get_template("home.html")
    lang_index = env.get_template("index.html")
    episode_tpl = env.get_template("episode.html")

    # Root hub
    (OUT / "index.html").write_text(
        root_index.render(
            site=config.SITE,
            shows=shows,
            year=year,
            base_path="./",
            rss_url=shows[0]["rss"] if shows else "",
            og_image=next((s["image"] for s in shows if s.get("image")), ""),
        ),
        encoding="utf-8",
    )

    all_urls: list[str] = [f"{config.SITE['base_url']}/"]

    for show in shows:
        lang = show["lang"]
        lang_dir = OUT / lang
        lang_dir.mkdir(parents=True, exist_ok=True)
        site = build_site_ctx(show)
        base_path = "../"

        (lang_dir / "index.html").write_text(
            lang_index.render(
                site=site,
                episodes=show["episodes"],
                feed_title=show["title"],
                feed_description=show["description"],
                feed_image=show["image"],
                year=year,
                base_path=base_path,
                rss_url=show["rss"],
                og_image=show["image"],
                series_jsonld=series_jsonld(show, site),
                show_ok=show["ok"],
                show_error=show.get("error") or "",
                shows=shows,
                current_lang=lang,
            ),
            encoding="utf-8",
        )
        all_urls.append(f"{config.SITE['base_url']}/{lang}/")

        eps = show["episodes"]
        for i, ep in enumerate(eps):
            prev_ep = eps[i - 1] if i > 0 else None
            next_ep = eps[i + 1] if i + 1 < len(eps) else None
            (lang_dir / ep["filename"]).write_text(
                episode_tpl.render(
                    site=site,
                    episode=ep,
                    prev_ep=prev_ep,
                    next_ep=next_ep,
                    year=year,
                    base_path=base_path,
                    rss_url=show["rss"],
                    og_image=ep.get("image") or show.get("image") or "",
                    episode_jsonld=episode_jsonld(ep, site, show),
                    shows=shows,
                    current_lang=lang,
                ),
                encoding="utf-8",
            )
            all_urls.append(f"{config.SITE['base_url']}/{lang}/{ep['filename']}")

    # robots + sitemap
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {config.SITE['base_url']}/sitemap.xml\n",
        encoding="utf-8",
    )
    url_xml = "\n".join(
        f"  <url><loc>{html.escape(u)}</loc></url>" for u in all_urls
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_xml}\n"
        "</urlset>\n",
        encoding="utf-8",
    )

    # Keep a copy of last build meta
    meta = {
        "built_utc": datetime.now(timezone.utc).isoformat(),
        "shows": [
            {
                "lang": s["lang"],
                "title": s["title"],
                "episodes": len(s["episodes"]),
                "ok": s["ok"],
                "error": s.get("error") or "",
            }
            for s in shows
        ],
    }
    (OUT / "build.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


def main() -> int:
    shows = [fetch_show(cfg) for cfg in config.FEEDS]
    render_all(shows)
    print(f"Wrote site → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
