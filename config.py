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

# GitHub Pages: publish /docs
OUTPUT_DIR = "docs"
META_DESCRIPTION_LEN = 155
TECH_BOOKS_PATH = "tech-books.html"
