# -*- coding: utf-8 -*-
"""Site + multi-language Spotify/Anchor RSS configuration."""

from __future__ import annotations

SITE = {
    "name": "Harbor Light Audio Drama",
    "tagline": "Dark mafia romance. Cinematic audio. Free chapters on Spotify.",
    "author": "Picu Bianca-Maria",
    "language": "en",
    "locale": "en_US",
    "base_url": "https://picubiancamaria.com",
    "custom_domain": "picubiancamaria.com",
    "github_repo": "harbor-light-website",
    "github_user": "biancaciuciulea",
    "email": "",
    # Free Formspree — replace YOUR_FORM_ID after signup
    "formspree_endpoint": "https://formspree.io/f/YOUR_FORM_ID",
}

# One feed per language show (Spotify for Podcasters / Anchor RSS)
FEEDS: list[dict[str, str]] = [
    {
        "lang": "en",
        "label": "English",
        "rss": "https://anchor.fm/s/119b406bc/podcast/rss",
        "spotify_show_url": "https://open.spotify.com/show/6pH6mP43frd87Vjdh6D2oW",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-en-audio",
        "amazon_url": "https://www.amazon.com/dp/B0HDHRDVDS",
    },
    {
        "lang": "de",
        "label": "Deutsch",
        "rss": "https://anchor.fm/s/119c2139c/podcast/rss",
        "spotify_show_url": "https://open.spotify.com/show/6MqSbSQ8pxM9nvjzOalE8s",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-de-audio",
        "amazon_url": "https://www.amazon.de/dp/B0HLZVNH99",
    },
    {
        "lang": "fr",
        "label": "Français",
        "rss": "https://anchor.fm/s/119c33574/podcast/rss",
        "spotify_show_url": "https://open.spotify.com/show/1d7wBjUOokNQupl9b7kKJr",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-fr-audio",
        "amazon_url": "https://www.amazon.fr/dp/B0HM23J19C",
    },
]

# GitHub Pages: publish /docs
OUTPUT_DIR = "docs"
META_DESCRIPTION_LEN = 155
