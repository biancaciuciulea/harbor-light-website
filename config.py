# -*- coding: utf-8 -*-
"""Site + multi-language Spotify/Anchor RSS configuration."""

from __future__ import annotations

SITE = {
    "name": "Harbor Light Audio Drama",
    "tagline": "Dark mafia romance. Cinematic audio. Free chapters on Spotify.",
    "author": "Picu Bianca-Maria",
    "author_bio": (
        "Hi, I'm Picu Bianca-Maria. I am an independent author and digital creator. "
        "Welcome to my creative hub where I bring together cinematic audio dramas, "
        "AI engineering playbooks, and spatial music."
    ),
    "author_image": "assets/author.jpg",
    "author_same_as": [
        "https://picubiancamaria.gumroad.com/",
        "https://open.spotify.com/show/6pH6mP43frd87Vjdh6D2oW",
        "https://open.spotify.com/show/6MqSbSQ8pxM9nvjzOalE8s",
        "https://open.spotify.com/show/1d7wBjUOokNQupl9b7kKJr",
        "https://www.amazon.com/dp/B0HDHRDVDS",
        "https://distrokid.com/hyperfollow/picubianca/iron-pulse-rising",
    ],
    "language": "en",
    "locale": "en_US",
    "base_url": "https://picubiancamaria.com",
    "custom_domain": "picubiancamaria.com",
    "github_repo": "harbor-light-website",
    "github_user": "biancaciuciulea",
    "email": "",
    # Free Formspree — set real ID to enable email capture on the site
    "formspree_endpoint": "https://formspree.io/f/mnppkppz",
    # Optional analytics — empty = no tracking script
    "gtm_id": "GTM-WFCFBTR3",  # Google tag / Tag Manager container
    "plausible_domain": "",  # e.g. "picubiancamaria.com"
    "ga4_id": "G-6TC0BTZ83E",  # GA4 web stream (config under the same Google tag)
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
        "amazon_url": "https://www.amazon.com/dp/B0HLZVNH99",
    },
    {
        "lang": "fr",
        "label": "Français",
        "rss": "https://anchor.fm/s/119c33574/podcast/rss",
        "spotify_show_url": "https://open.spotify.com/show/1d7wBjUOokNQupl9b7kKJr",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-fr-audio",
        "amazon_url": "https://www.amazon.com/dp/B0HM23J19C",
    },
    {
        "lang": "es",
        "label": "Español",
        "rss": "https://anchor.fm/s/119e5c774/podcast/rss",
        # Trailer/show CTA until Spotify show URL is available
        "spotify_show_url": "https://open.spotify.com/episode/17fLWRNfhtNNSfPyvoDooz",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-es-audio",
        "amazon_url": "https://www.amazon.com/dp/B0HNCK3DPB",
        # Cap. 1 live on Spotify; RSS may lag — keep linked until feed includes it
        "extra_episodes": [
            {
                "title": 'Capítulo 1: "El contrato sin firmar"',
                "spotify_url": "https://open.spotify.com/episode/3uUHhNlQ9Xu7QbI9DDcaCg",
                "episode_number": 1,
                "episode_type": "full",
            },
        ],
    },
    {
        "lang": "it",
        "label": "Italiano",
        "rss": "https://anchor.fm/s/119e60144/podcast/rss",
        "spotify_show_url": "https://open.spotify.com/episode/6D5kLrZbUr5Z5Qgcz1TfvU",
        "gumroad_url": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-it-audio",
        "amazon_url": "https://www.amazon.com/dp/B0HNC6W6TH",
        "extra_episodes": [
            {
                "title": 'Trailer: "Il contratto non firmato"',
                "spotify_url": "https://open.spotify.com/episode/6D5kLrZbUr5Z5Qgcz1TfvU",
                "episode_type": "trailer",
            },
        ],
    },
]

# Companion downloads for The AI Engineer's Series (Gumroad)
GUMROAD_COMPANIONS: list[dict[str, str]] = [
    {
        "title": "The AI Engineer's Series — Complete Prompt Companion",
        "gumroad_link": "https://picubiancamaria.gumroad.com/l/rgnko",
    },
    {
        "title": "The AI Engineer's Series — Ultimate Production Repo + Offline Copilot",
        "gumroad_link": "https://picubiancamaria.gumroad.com/l/pktikn",
    },
]

# Kindle catalog — productivity series + engineering series
TECH_BOOKS: dict[str, list[dict[str, str]]] = {
    "The AI Engineer's Series": [
        {
            "title": "AI for Real Estate Agents: Close More Deals, Respond Faster, Spend Less Time on Admin",
            "amazon_link": "https://www.amazon.com/dp/B0HCZNBCT2",
            "asin": "B0HCZNBCT2",
        },
        {
            "title": "Automate Your Work with AI: 10 Automations That Give You 10 Hours Back Every Week",
            "amazon_link": "https://www.amazon.com/dp/B0HCZLBJXS",
            "asin": "B0HCZLBJXS",
        },
        {
            "title": "ChatGPT for Lawyers: Save 12 Hours Per Week, Bill More, Burn Out Less",
            "amazon_link": "https://www.amazon.com/dp/B0GXQHDHKZ",
            "asin": "B0GXQHDHKZ",
        },
        {
            "title": "10x Productivity with AI: Work Smarter, Leave On Time, Reclaim Your Focus",
            "amazon_link": "https://www.amazon.com/dp/B0HCZLC2DS",
            "asin": "B0HCZLC2DS",
        },
        {
            "title": "Make Money with ChatGPT: The Freelancer's Complete Playbook for AI-Powered Income",
            "amazon_link": "https://www.amazon.com/dp/B0HCZ8TMHH",
            "asin": "B0HCZ8TMHH",
        },
        {
            "title": "AI Side Hustles for Beginners: 8 Complete Starter Kits, Start in 48 Hours",
            "amazon_link": "https://www.amazon.com/dp/B0HCYYLRRJ",
            "asin": "B0HCYYLRRJ",
        },
        {
            "title": "AI for Teachers: Save 6 Weeks a Year, Plan Faster, Grade Smarter",
            "amazon_link": "https://www.amazon.com/dp/B0HCV6D5ZN",
            "asin": "B0HCV6D5ZN",
        },
    ],
    "The 1'st AI Engineering Series": [
        {
            "title": "Prompt Engineering Mastery: The Definitive Guide to LLMs, Advanced RAG, and Agentic Workflows (2026 Edition)",
            "amazon_link": "https://www.amazon.com/dp/B0GS77LKB2",
            "asin": "B0GS77LKB2",
        },
        {
            "title": "LLM Engineering: Building Production-Ready Language Models: Guide for ML Engineers, Software Engineers, and DevOps",
            "amazon_link": "https://www.amazon.com/dp/B0GRMHPWD8",
            "asin": "B0GRMHPWD8",
        },
        {
            "title": "Mastering Large Language Models: From Theory to Production: Complete Guide for Developers, Data Scientists, and AI Engineers",
            "amazon_link": "https://www.amazon.com/dp/B0GRGR4DHP",
            "asin": "B0GRGR4DHP",
        },
        {
            "title": "The Art of Prompt Engineering: Maximizing LLM Performance",
            "amazon_link": "https://www.amazon.com/dp/B0GSC87H47",
            "asin": "B0GSC87H47",
        },
        {
            "title": "Prompt Engineering: From Basics to Advanced Patterns: A Practical Guide from First Prompts to Reliable AI Workflows",
            "amazon_link": "https://www.amazon.com/dp/B0GSH9XQF2",
            "asin": "B0GSH9XQF2",
        },
        {
            "title": "AI Agents in Production: Building Reliable, Scalable, and Secure LLM Agents",
            "amazon_link": "https://www.amazon.com/dp/B0GHPVL52F",
            "asin": "B0GHPVL52F",
        },
        {
            "title": "LLM Engineering: The Definitive Guide to Building, Scaling, and Monitoring Production-Ready AI Systems",
            "amazon_link": "https://www.amazon.com/dp/B0GSL5DCHN",
            "asin": "B0GSL5DCHN",
        },
    ],
}

# Series blurbs shown on the tech catalog page
TECH_SERIES_BLURBS: dict[str, str] = {
    "The AI Engineer's Series": "Practical AI for real jobs — real estate, law, teaching, freelancing, and weekly productivity.",
    "The 1'st AI Engineering Series": "Production LLM engineering — prompts, RAG, agents, scaling, and monitoring.",
}

# DistroKid HyperFollow catalog (artist: picubianca)
MUSIC_TRACKS: list[dict[str, str]] = [
    {
        "title": "Iron Pulse Rising",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/iron-pulse-rising",
        "slug": "iron-pulse-rising",
    },
    {
        "title": "Neon Rain Echo",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/neon-rain-echo",
        "slug": "neon-rain-echo",
    },
    {
        "title": "Echo of Shadows Rising",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/echo-of-shadows-rising",
        "slug": "echo-of-shadows-rising",
    },
    {
        "title": "Echoes Under Steel Skies",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/echoes-under-steel-skies",
        "slug": "echoes-under-steel-skies",
    },
    {
        "title": "When Worlds Collide",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/when-worlds-collide",
        "slug": "when-worlds-collide",
    },
    {
        "title": "Moonlit Blues",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/moonlit-blues",
        "slug": "moonlit-blues",
    },
    {
        "title": "Neon Tears (Radio Edit)",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/neon-tears-radio-edit",
        "slug": "neon-tears-radio-edit",
    },
]

# Full Harbor Light commerce catalog (Amazon Kindle + Gumroad audio).
# Site Amazon CTAs always use amazon.com (same ASINs) — not .de/.fr/.es/.it.
# CTA order everywhere: Spotify free → Gumroad audio → Amazon Kindle.
HARBOR_SERIES: list[dict] = [
    {
        "book": 1,
        "title_en": "Bound by Blood and Harbor Light",
        "blurb": "Three locks. An unsigned marriage pact. Elena Voss and Julian Kane in Harbor Light mist — loyalty is currency, love has no ledger line.",
        "cover": "assets/harbor/book1-en.jpg",
        "editions": [
            {
                "lang": "en",
                "label": "English",
                "cover": "assets/harbor/book1-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HDHRDVDS",
                "gumroad": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-en-audio",
                "spotify": "https://open.spotify.com/show/6pH6mP43frd87Vjdh6D2oW",
            },
            {
                "lang": "de",
                "label": "Deutsch",
                "cover": "assets/harbor/book1-de.jpg",
                "amazon": "https://www.amazon.com/dp/B0HLZVNH99",
                "gumroad": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-de-audio",
                "spotify": "https://open.spotify.com/show/6MqSbSQ8pxM9nvjzOalE8s",
            },
            {
                "lang": "fr",
                "label": "Français",
                "cover": "assets/harbor/book1-fr.jpg",
                "amazon": "https://www.amazon.com/dp/B0HM23J19C",
                "gumroad": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-fr-audio",
                "spotify": "https://open.spotify.com/show/1d7wBjUOokNQupl9b7kKJr",
            },
            {
                "lang": "es",
                "label": "Español",
                "cover": "assets/harbor/book1-es.jpg",
                "amazon": "https://www.amazon.com/dp/B0HNCK3DPB",
                "gumroad": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-es-audio",
                "spotify": "https://open.spotify.com/episode/17fLWRNfhtNNSfPyvoDooz",
            },
            {
                "lang": "it",
                "label": "Italiano",
                "cover": "assets/harbor/book1-it.jpg",
                "amazon": "https://www.amazon.com/dp/B0HNC6W6TH",
                "gumroad": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-it-audio",
                "spotify": "https://open.spotify.com/episode/6D5kLrZbUr5Z5Qgcz1TfvU",
            },
        ],
    },
    {
        "book": 2,
        "title_en": "Bound by Soft Marks and Harbor Light",
        "blurb": "The Soft Marks escalate. Desire cuts deeper than protocol — and Harbor Light keeps score.",
        "cover": "assets/harbor/book2-en.jpg",
        "editions": [
            {
                "lang": "en",
                "label": "English",
                "cover": "assets/harbor/book2-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HF3JDYLG",
                "gumroad": "",
                "spotify": "",
            },
            {
                "lang": "de",
                "label": "Deutsch",
                "cover": "assets/harbor/book2-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HNWB2DGG",
                "gumroad": "",
                "spotify": "",
            },
            {
                "lang": "fr",
                "label": "Français",
                "cover": "assets/harbor/book2-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HNWH6NXD",
                "gumroad": "",
                "spotify": "",
            },
            {
                "lang": "es",
                "label": "Español",
                "cover": "assets/harbor/book2-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HPBNJ84Z",
                "gumroad": "",
                "spotify": "",
            },
            {
                "lang": "it",
                "label": "Italiano",
                "cover": "assets/harbor/book2-en.jpg",
                "amazon": "https://www.amazon.com/dp/B0HPD6LYMP",
                "gumroad": "",
                "spotify": "",
            },
        ],
    },
    {
        "book": 3,
        "title_en": "Bound by Soft Hour and Harbor Light",
        "blurb": "Clinic under empire. Soft Hour is sanctuary — until the ledger calls it leverage.",
        "cover": "",
        "editions": [
            {
                "lang": "en",
                "label": "English",
                "cover": "",
                "amazon": "https://www.amazon.com/dp/B0HHSR3JK4",
                "gumroad": "",
                "spotify": "",
            },
        ],
    },
    {
        "book": 4,
        "title_en": "Bound by Soft Gate and Harbor Light",
        "blurb": "The Soft Gate opens. Paper becomes power — and Elena chooses what survives the harbor.",
        "cover": "",
        "editions": [
            {
                "lang": "en",
                "label": "English",
                "cover": "",
                "amazon": "https://www.amazon.com/dp/B0HL4NWK55",
                "gumroad": "",
                "spotify": "",
            },
        ],
    },
]

# Short local landings (conversion pages per language)
LANG_LANDINGS: list[dict[str, str]] = [
    {
        "lang": "de",
        "slug": "de.html",
        "title": "Hafenlicht — Dunkle Mafia Romance",
        "lede": "Lies auf Kindle. Hör das filmische Hörbuch auf Gumroad. Kostenlose Kapitel auf Spotify.",
        "cta_series": "Zur kompletten Serie",
    },
    {
        "lang": "fr",
        "slug": "fr.html",
        "title": "Lumière du Port — Romance mafia sombre",
        "lede": "Lisez sur Kindle. Écoutez l'audiolivre cinématique sur Gumroad. Chapitres gratuits sur Spotify.",
        "cta_series": "Voir toute la série",
    },
    {
        "lang": "es",
        "slug": "es.html",
        "title": "Luz del Puerto — Romance mafia oscuro",
        "lede": "Lee en Kindle. Escucha el audiolibro cinematográfico en Gumroad. Tráiler + Capítulo 1 gratis en Spotify.",
        "cta_series": "Ver la serie completa",
    },
    {
        "lang": "it",
        "slug": "it.html",
        "title": "Luce del Porto — Romance mafia dark",
        "lede": "Leggi su Kindle. Ascolta l'audiolibro cinematografico su Gumroad. Trailer gratis su Spotify.",
        "cta_series": "Vedi tutta la serie",
    },
]

# GitHub Pages: publish /docs
OUTPUT_DIR = "docs"
META_DESCRIPTION_LEN = 155
TECH_BOOKS_PATH = "tech-books.html"
MUSIC_PATH = "music.html"
HARBOR_SERIES_PATH = "harbor-light.html"
