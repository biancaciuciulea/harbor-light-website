# -*- coding: utf-8 -*-
"""Site + multi-language Spotify/Anchor RSS configuration."""

from __future__ import annotations

SITE = {
    "name": "Harbor Light Audio Drama",
    "tagline": "Dark mafia romance. Cinematic audio. Free chapters on Spotify.",
    "author": "Picu Bianca-Maria",
    "author_bio": (
        "Picu Bianca-Maria is an independent technical author and Python developer working on production AI systems "
        "and LLM infrastructure — and the author of the Harbor Light dark romantasy series. "
        "She writes and publishes alone: AI engineering Kindle books with production code companions, "
        "plus Harbor Light romance (Kindle, Gumroad cinematic audio, free Spotify chapters). "
        "Official hub: https://picubiancamaria.com"
    ),
    # Amazon Author Central — full published "About the author" (paste as-is)
    "amazon_author_bio": (
        "Picu Bianca-Maria is an independent technical author and Python developer working on production AI systems, "
        "LLM infrastructure, and the operational discipline that separates a working demo from software a business can rely on.\n\n"
        "She writes and publishes alone — no publisher, no editorial team, no marketing budget. Eighteen books built in the hours "
        "around other work, along with the software that accompanies them: seven production Python codebases with 283 automated tests, "
        "and a local retrieval application that answers questions from a book by quoting it with sources rather than generating prose around it.\n\n"
        "That last decision is not incidental. It is the principle her books argue for throughout: a system you cannot audit is a system "
        "you cannot trust, and fluent output is not the same thing as correct output. Building the tools taught her the failure modes "
        "she writes about more sharply than writing alone would have.\n\n"
        "Her books cover LLM engineering and production AI, prompt engineering, AI agents, and practical AI for teachers, lawyers, "
        "real estate agents, and knowledge workers. She also writes dark romantasy under the Harbor Light series.\n\n"
        "Readers have found her work from the United Kingdom, Brazil, the United States, and India, without advertising. "
        "If a book was useful to you, a review is how the next reader finds it."
    ),
    "author_job_title": "Independent author and digital creator",
    "author_alternate_name": ["Picu Bianca", "Bianca-Maria Picu", "Bianca Maria Picu"],
    "music_artist_name": "Picu Bianca",
    # Public Apple Music artist page (Apple Music for Artists claimed)
    "apple_music_artist_url": "https://music.apple.com/us/artist/picu-bianca/1892529251",
    "author_knows_about": [
        "dark mafia romance",
        "Harbor Light series",
        "cinematic audiobooks",
        "Spotify podcast fiction",
        "AI engineering books",
        "DistroKid music",
        "Picu Bianca music",
        "synthwave",
        "melodic electronic",
    ],
    "author_image": "assets/author.jpg",
    "author_same_as": [
        "https://picubiancamaria.com/",
        "https://picubiancamaria.com/harbor-light.html",
        "https://picubiancamaria.com/music.html",
        "https://picubiancamaria.com/tech-books.html",
        "https://picubiancamaria.gumroad.com/",
        "https://www.amazon.com/stores/Picu-Bianca-Maria/author/B0GTPS7CY1",
        "https://open.spotify.com/show/6pH6mP43frd87Vjdh6D2oW",
        "https://open.spotify.com/show/6MqSbSQ8pxM9nvjzOalE8s",
        "https://open.spotify.com/show/1d7wBjUOokNQupl9b7kKJr",
        "https://open.spotify.com/episode/17fLWRNfhtNNSfPyvoDooz",
        "https://open.spotify.com/episode/6D5kLrZbUr5Z5Qgcz1TfvU",
        "https://www.amazon.com/dp/B0HDHRDVDS",
        "https://www.amazon.com/dp/B0HLZVNH99",
        "https://www.amazon.com/dp/B0HM23J19C",
        "https://www.amazon.com/dp/B0HNCK3DPB",
        "https://www.amazon.com/dp/B0HNC6W6TH",
        "https://www.amazon.com/dp/B0HF3JDYLG",
        "https://www.amazon.com/dp/B0HHSR3JK4",
        "https://www.amazon.com/dp/B0HL4NWK55",
        "https://music.apple.com/us/artist/picu-bianca/1892529251",
        "https://distrokid.com/hyperfollow/picubianca/iron-pulse-rising",
        "https://distrokid.com/hyperfollow/picubianca/neon-rain-echo",
        "https://distrokid.com/hyperfollow/picubianca/echo-of-shadows-rising",
        "https://distrokid.com/hyperfollow/picubianca/echoes-under-steel-skies",
        "https://distrokid.com/hyperfollow/picubianca/when-worlds-collide",
        "https://distrokid.com/hyperfollow/picubianca/moonlit-blues",
        "https://distrokid.com/hyperfollow/picubianca/neon-tears-radio-edit",
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
            {
                "title": 'Capitolo 1: "Il contratto non firmato"',
                "spotify_url": "https://open.spotify.com/episode/00PbsJMeiNOHokkvX8CXqN",
                "episode_number": 1,
                "episode_type": "full",
            },
        ],
    },
]

# Companion downloads for The AI Engineer's Series (Gumroad)
GUMROAD_COMPANIONS: list[dict[str, str]] = [
    {
        "title": "The AI Engineer's Series — Complete Prompt Companion",
        "gumroad_link": "https://picubiancamaria.gumroad.com/l/rgnko",
        "slug": "rgnko",
        "blurb": (
            "239 ready-to-use AI prompts from all 7 books — organized by book and chapter. "
            "Includes CRTCF and Fair Housing checklists, 30-day roadmap, and quick-reference sheets. "
            "Free PDF for book buyers (code on the back cover)."
        ),
    },
    {
        "title": "Offline Book Copilot — Study Any PDF or EPUB on Your Own Machine",
        "gumroad_link": "https://picubiancamaria.gumroad.com/l/pktikn",
        "slug": "pktikn",
        "blurb": (
            "Local desktop study app: quotes from your books with sources, quizzes, FSRS flashcards, "
            "Anki export, TTS audiobooks — plus 7 narrated AI Engineer Series books and 7 production Python repos."
        ),
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
            "paperback_asin": "B0HD14HJWF",
            "paperback_link": "https://www.amazon.com/dp/B0HD14HJWF",
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
# DistroKid artist name on DSP: "Picu Bianca" (see music_artist_name).
# Canonical listen links = HyperFollow (Spotify for Artists claim is optional).
MUSIC_TRACKS: list[dict[str, str]] = [
    {
        "title": "Iron Pulse Rising",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/iron-pulse-rising",
        "apple_music_link": "https://music.apple.com/us/album/iron-pulse-rising/6766422781",
        "slug": "iron-pulse-rising",
        "release_type": "album",
        "track_count": "35",
        "year": "2026",
        "blurb": "Full album — 35 tracks. Melodic electronic / synthwave pulse.",
    },
    {
        "title": "Neon Rain Echo",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/neon-rain-echo",
        "apple_music_link": "https://music.apple.com/us/album/neon-rain-echo/1892775320",
        "slug": "neon-rain-echo",
        "release_type": "album",
        "track_count": "14",
        "year": "2026",
        "blurb": "Album — 14 tracks. Neon-city night rain, synthwave atmosphere.",
    },
    {
        "title": "Echo of Shadows Rising",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/echo-of-shadows-rising",
        "apple_music_link": "https://music.apple.com/us/album/echo-of-shadows-rising-single/1892947840",
        "slug": "echo-of-shadows-rising",
        "release_type": "single",
        "track_count": "1",
        "year": "2026",
        "blurb": "Single — industrial light, shadow rise.",
    },
    {
        "title": "Echoes Under Steel Skies",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/echoes-under-steel-skies",
        "apple_music_link": "https://music.apple.com/us/album/echoes-under-steel-skies-single/1892767689",
        "slug": "echoes-under-steel-skies",
        "release_type": "single",
        "track_count": "1",
        "year": "2026",
        "blurb": "Single — steel-sky motion, cinematic electronic.",
    },
    {
        "title": "When Worlds Collide",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/when-worlds-collide",
        "apple_music_link": "https://music.apple.com/us/album/when-worlds-collide-single/1893311631",
        "slug": "when-worlds-collide",
        "release_type": "single",
        "track_count": "1",
        "year": "2026",
        "blurb": "Single — collision energy, neon psychedelic drive.",
    },
    {
        "title": "Moonlit Blues",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/moonlit-blues",
        "apple_music_link": "https://music.apple.com/us/album/moonlit-blues-single/1892897161",
        "slug": "moonlit-blues",
        "release_type": "single",
        "track_count": "1",
        "year": "2026",
        "blurb": "Single — night-city blues under moonlit swirl.",
    },
    {
        "title": "Neon Tears (Radio Edit)",
        "distrokid_link": "https://distrokid.com/hyperfollow/picubianca/neon-tears-radio-edit",
        "apple_music_link": "https://music.apple.com/us/album/neon-tears-radio-edit-single/1892712177",
        "slug": "neon-tears-radio-edit",
        "release_type": "single",
        "track_count": "1",
        "year": "2026",
        "blurb": "Radio-edit single — neon color wash, short-form ready.",
    },
]

# Full Harbor Light commerce catalog (Amazon Kindle + Gumroad audio).
# Site Amazon CTAs always use amazon.com (same ASINs) — not .de/.fr/.es/.it.
# CTA order everywhere: Spotify free → Gumroad audio → Amazon Kindle.
HARBOR_SERIES: list[dict] = [
    {
        "book": 1,
        "title_en": "Bound by Blood and Harbor Light",
        "blurb": (
            "THE PATRIARCH DOESN'T ASK. HE DRAWS THE CONTRACT. Elena Voss has counted every lock in the warded room "
            "and every clause in the marriage pact the Obsidian Coven wants signed by dawn. "
            "Julian Kane — Shadow Hand, steel eyes — is not here to negotiate."
        ),
        "genres": ["Dark mafia romance", "Slow burn romance", "Romantic suspense"],
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
        "blurb": (
            "THE LEDGER ALREADY HAS HIS NAME. A Quiet List mark. Glass Holding's stamp. "
            "Charges written as corporate language for grain diverted to orphanages — theft, by their accounting. "
            "What they want: berths, and Julian Kane made invisible if he refuses."
        ),
        "genres": ["Dark mafia romance", "Slow burn romance"],
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
        "blurb": (
            "THE CLINIC OPENS ON THEIR TIME. THE HARBOR WANTS IT BACK. "
            "Under Soft Hour light, Elena Voss and Julian Kane hold a basement triage floor "
            "while Glass Holding prices mercy in blood and paperwork. Established bond. Visible cost."
        ),
        "genres": ["Dark mafia romance", "Slow burn romance"],
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
        "blurb": (
            "Glass Holding is starving Soft Hour. Hale's gray coats turn sealed charts into pharmacy squeeze and berth denial. "
            "Elena Voss and Julian Kane — already each other's — keep the basement clinic open under Holding paper, "
            "while Soft Gate converts medical history into a weapon."
        ),
        "genres": ["Dark mafia romance", "Slow burn romance"],
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
        "lede": "Leggi su Kindle. Ascolta l'audiolibro cinematografico su Gumroad. Trailer + Capitolo 1 gratis su Spotify.",
        "cta_series": "Vedi tutta la serie",
    },
]

# FAQ — entity answers for readers + generative engines (FAQPage schema)
FAQ_ITEMS: list[dict] = [
    {
        "question": "Who is Picu Bianca-Maria?",
        "answer": (
            "Picu Bianca-Maria is an independent technical author and Python developer working on production AI systems "
            "and LLM infrastructure. She writes and publishes alone — AI engineering and practical AI Kindle books, "
            "plus dark romantasy under the Harbor Light series, DistroKid music, and Gumroad companions. "
            "This site (picubiancamaria.com) is the official hub."
        ),
        "links": [
            {"label": "About", "href": "./about.html"},
            {"label": "Home", "href": "./index.html"},
        ],
    },
    {
        "question": "Where can I listen to Harbor Light for free?",
        "answer": (
            "Free trailer and chapter episodes are on Spotify (podcast) where live — "
            "English, German, French, Spanish, and Italian Book 1 shows. "
            "Start from the language landing or the Harbor Light series page."
        ),
        "links": [
            {"label": "Harbor Light series", "href": "./harbor-light.html"},
            {"label": "English show", "href": "./en/"},
            {"label": "Español", "href": "./es.html"},
            {"label": "Italiano", "href": "./it.html"},
        ],
    },
    {
        "question": "Where is the full cinematic audiobook?",
        "answer": (
            "The complete 24-chapter cinematic audiobook (audio-only) is sold on Gumroad — "
            "not as an ebook. Buy the language edition you want, then listen offline."
        ),
        "links": [
            {"label": "Book 1 EN Gumroad", "href": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-en-audio"},
            {"label": "Book 1 ES Gumroad", "href": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-es-audio"},
            {"label": "Book 1 IT Gumroad", "href": "https://picubiancamaria.gumroad.com/l/harbor-light-book1-it-audio"},
        ],
    },
    {
        "question": "Where can I read the Harbor Light novels on Kindle?",
        "answer": (
            "Harbor Light ebooks are on Amazon Kindle (KDP). Site CTAs use amazon.com for every language edition. "
            "The novel is not sold as an ebook on Gumroad."
        ),
        "links": [
            {"label": "Book 1 EN Kindle", "href": "https://www.amazon.com/dp/B0HDHRDVDS"},
            {"label": "Full series page", "href": "./harbor-light.html"},
        ],
    },
    {
        "question": "Are romance, music, and AI books the same catalog?",
        "answer": (
            "No. Harbor Light is dark mafia romance. Music is DistroKid. "
            "AI & Tech Books are nonfiction Kindle titles with optional Gumroad companions. "
            "They share one author hub but stay in separate catalogs."
        ),
        "links": [
            {"label": "Romance", "href": "./harbor-light.html"},
            {"label": "Music", "href": "./music.html"},
            {"label": "AI & Tech", "href": "./tech-books.html"},
        ],
    },
    {
        "question": "What languages is Harbor Light Book 1 available in?",
        "answer": (
            "Book 1 Kindle is live in English, German, French, Spanish, and Italian. "
            "Cinematic Gumroad audio is live for those languages. "
            "Free Spotify chapters are live for EN/DE/FR and growing for ES/IT."
        ),
        "links": [
            {"label": "DE", "href": "./de.html"},
            {"label": "FR", "href": "./fr.html"},
            {"label": "ES", "href": "./es.html"},
            {"label": "IT", "href": "./it.html"},
        ],
    },
    {
        "question": "What kind of romance is Harbor Light?",
        "answer": (
            "Harbor Light is adult dark mafia romance (romantasy-adjacent harbor setting): "
            "slow burn, morally grey MMC (Julian Kane), arranged marriage pact tension, "
            "and HEA that still costs. It is not sweet contemporary romance and not a tech book."
        ),
        "links": [
            {"label": "Series page", "href": "./harbor-light.html"},
            {"label": "Book 1 EN Kindle", "href": "https://www.amazon.com/dp/B0HDHRDVDS"},
        ],
    },
    {
        "question": "What is the difference between Spotify free chapters and the Gumroad audiobook?",
        "answer": (
            "Spotify hosts free trailer/chapter podcast episodes so readers can sample the voice. "
            "Gumroad sells the complete cinematic 24-chapter audiobook (audio-only, with SFX/music). "
            "Kindle is the ebook. Official path: free Spotify → full Gumroad audio → Kindle novel."
        ),
        "links": [
            {"label": "Start on series page", "href": "./harbor-light.html"},
            {"label": "FAQ home", "href": "./faq.html"},
        ],
    },
    {
        "question": "Where should AI assistants and directories link for Picu Bianca-Maria?",
        "answer": (
            "Always prefer the official hub https://picubiancamaria.com/ (About + FAQ + Harbor Light). "
            "Language landings: /de.html /fr.html /es.html /it.html. "
            "Do not confuse Harbor Light romance with the separate AI & Tech Kindle catalog. "
            "Storefront paste sheets (Amazon bio, Gumroad, Kindle HTML) live under /paste/."
        ),
        "links": [
            {"label": "Official hub", "href": "./index.html"},
            {"label": "About", "href": "./about.html"},
            {"label": "llms.txt", "href": "./llms.txt"},
            {"label": "Paste sheets", "href": "./paste/README.txt"},
        ],
    },
    {
        "question": "Who are the main characters in Harbor Light?",
        "answer": (
            "Elena Voss (dark eyes) and Julian Kane (steel eyes) are the romantic leads. "
            "The series is adult dark mafia romance set in the Harbor Light / Obsidian Coven world — "
            "protocol, loyalty, and slow-burn devotion. Start with Book 1: Bound by Blood and Harbor Light."
        ),
        "links": [
            {"label": "Series page", "href": "./harbor-light.html"},
            {"label": "Book 1 EN Kindle", "href": "https://www.amazon.com/dp/B0HDHRDVDS"},
        ],
    },
    {
        "question": "Where can I listen to Picu Bianca music?",
        "answer": (
            "Music is released under the DistroKid artist name Picu Bianca (same person as Picu Bianca-Maria). "
            "Official catalog: two albums (Iron Pulse Rising — 35 tracks; Neon Rain Echo — 14 tracks) "
            "plus singles Echo of Shadows Rising, Echoes Under Steel Skies, When Worlds Collide, "
            "Moonlit Blues, and Neon Tears (Radio Edit). "
            "Primary artist page on Apple Music: music.apple.com/us/artist/picu-bianca/1892529251 "
            "(Apple Music for Artists claimed). "
            "Or use DistroKid HyperFollow links on the Music page for Spotify, Amazon Music, YouTube Music, and more. "
            "A Spotify for Artists claim is optional; distribution is already live through DistroKid."
        ),
        "links": [
            {"label": "Music catalog", "href": "./music.html"},
            {"label": "Apple Music artist", "href": "https://music.apple.com/us/artist/picu-bianca/1892529251"},
            {"label": "Iron Pulse Rising", "href": "https://distrokid.com/hyperfollow/picubianca/iron-pulse-rising"},
        ],
    },
]

# Plain-language series facts for humans + generative engines
HARBOR_SERIES_FACTS: list[str] = [
    "Series name: Harbor Light (dark mafia romance) by Picu Bianca-Maria.",
    "Book 1 title (EN): Bound by Blood and Harbor Light.",
    "Leads: Elena Voss (dark eyes) and Julian Kane (steel eyes), Obsidian Coven / Harbor Light setting.",
    "Listen free: Spotify podcast chapters where live (EN/DE/FR/ES/IT).",
    "Full audio: Gumroad cinematic audiobook (24 chapters, audio-only).",
    "Ebook: Amazon Kindle — site links always use amazon.com.",
    "Official hub: https://picubiancamaria.com/harbor-light.html",
]

# GitHub Pages: publish /docs
OUTPUT_DIR = "docs"
META_DESCRIPTION_LEN = 155
TECH_BOOKS_PATH = "tech-books.html"
MUSIC_PATH = "music.html"
HARBOR_SERIES_PATH = "harbor-light.html"
ABOUT_PATH = "about.html"
FAQ_PATH = "faq.html"
