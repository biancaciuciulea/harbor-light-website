#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write published Amazon tech-book descriptions into content/tech/{ASIN}.json.

Source: live Amazon product pages (scraped) + author-pasted authoritative copy.
Re-run after publishing new tech ASINs, then: python generator.py
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402

OUT = ROOT / "content" / "tech"

# Published Amazon descriptions (plain). Prefer author paste when provided.
DESCRIPTIONS: dict[str, str] = {
    # --- The AI Engineer's Series ---
    "B0HCZ8TMHH": """Make Money with ChatGPT is the guide that closes the gap between preparation and income — with a specific playbook for 6 proven income streams:

• Content Writing — $0.20-0.45/word as a niche specialist vs $0.02 as a generalist
• LinkedIn Ghostwriting — $400-1,500/month per client retainer
• Email Marketing — Recurring retainers for sequence writing
• AI Consulting — Help businesses implement the tools you already know
• Virtual Assistance — AI-powered admin at premium rates
• Social Media Management — Monthly batch in 90 minutes""",
    "B0HCV6D5ZN": """What if you could have your evenings back?

The average teacher spends 266 minutes per week on lesson planning alone — before marking, parent emails, reports, or admin. This book changes that.

AI for Teachers gives you 63 tested, copy-this prompts for the tasks that eat your professional time:

• Lesson plans produced in 90 seconds instead of 45 minutes
• Three-level differentiation in 12 minutes instead of 45
• Marking feedback for 30 students in 18 minutes instead of 2 hours
• Report comments drafted in 8 minutes instead of 40
• Parent emails and school communications in under 3 minutes each

Teachers using these methods recover an average of 5.9 hours per week (Gallup-Walton 2025). That's 6 full weeks of professional time returned to you every year.

Every method is Safe, Professional, and Curriculum-Aligned. The PGCR framework (Plan, Generate, Customise, Reuse) ensures AI is your professional tool — never your replacement.

Includes dedicated sections for primary teachers, NQTs/ECTs, SEND differentiation, EAL adaptation, gifted & talented extension, and the school leader's AI integration guide.

Free companion included at picubiancamaria.gumroad.com/l/rgnko/B01READER — 239 prompts, checklists, and templates.""",
    "B0HCYYLRRJ": """8 income streams. Zero experience required. Start this weekend.

This isn't a theory book. It's 8 complete starter kits — each one containing everything you need to launch your first AI-powered side hustle in under 48 hours.

Each kit includes: the exact tools, the tested prompts, the platform setup, the first-client playbook, and realistic income projections based on documented results.

• AI Content Writer — $0.20-0.45/word, first client within 7 days on Fiverr
• AI Social Media Manager — $300-800/month per client, batch in 2 hours
• AI Voiceover & Podcast Editor — $50-150/project, no recording equipment needed
• AI Logo & Graphic Designer — $25-200/design, zero artistic skill required
• AI Research Assistant — $30-75/hour, work for academics and businesses
• AI Email Marketing Specialist — $500-2,000/month retainer per client
• AI Resume & Cover Letter Writer — $50-150/resume, high repeat business
• AI Customer Service Agent — $15-25/hour, fully remote, flexible hours

No experience. No expensive tools. No technical background required.

Free companion: picubiancamaria.gumroad.com/l/rgnko/B03READER""",
    "B0GXQHDHKZ": """The 12 non-billable hours every attorney works every week. Recovered.

Bloomberg Law's 2024 survey of 1,054 attorneys found the average lawyer works 48 hours per week and bills 36. Those 12.3 hours — consumed by file notes, billing narratives, document formatting, internal admin, and business development — represent $174,720 per year in uncollected potential at a $280/hour billing rate.

This book provides the complete, ABA Formal Opinion 512-compliant framework for recovering 4-6 of those hours using AI tools — without compromising professional standards or client confidentiality.

34 document drafting prompts across 12 practice areas. Full CRTCF compliance workflow. Mandatory verification protocols for court submissions.

Covers: NDAs, employment agreements, demand letters, board minutes, lease summaries, settlement agreements, personal injury letters, GDPR data processing agreements, and more.

Includes the 30-day quick-start implementation guide, legal AI tool taxonomy, and client development system.

This book does not constitute legal advice. Professional judgment and CRTCF compliance are required for all methods.

Free companion: picubiancamaria.gumroad.com/l/rgnko/B04READER""",
    "B0HCZLC2DS": """Stop managing work. Start doing it.

The average knowledge worker receives 117 emails per day. Experiences 275 interruptions. Takes 23 minutes to regain focus after each one. The mathematics of modern work are incompatible with sustained output.

10x Productivity with AI gives you 6 evidence-based systems that recover 3-8 hours per week without working longer:

• The Email System — 3.6 hours/week saved (Microsoft/NBER RCT, n=6,000)
• Meeting Efficiency — Half the meeting time, same output
• Focus Protection — Two 90-minute blocks of uninterrupted deep work daily
• AI Writing — 30 minutes saved every day on professional communications
• Research & Synthesis — Hours to minutes for information-heavy tasks
• Weekly Review — 15 minutes on Friday for a clear, confident week ahead

Every method is grounded in published research (Gloria Mark, Microsoft, UCL). Every prompt is ready to copy and use immediately.

Includes dedicated sections for managers, remote workers, and team leaders.

Free companion: picubiancamaria.gumroad.com/l/rgnko/B05READER""",
    "B0HCZNBCT2": """78% of buyers hire the first agent who responds substantively.

The industry average response time to buyer enquiries: 917 minutes. Your new response time: under 5 minutes. That single change alone has documented conversion rates 21x higher than a 30-minute response.

AI for Real Estate Agents gives you 8 complete AI systems for every part of your practice:

• Listing Descriptions — Compelling, Fair Housing-compliant copy in 20 minutes
• Lead Response — 5 phone templates for instant personalised response
• CMA Narratives — Professional market analysis from your data in 25 minutes
• Social Media — 15 posts per month in a 90-minute batch session
• Client Communication — Automated buyer journey and seller update sequences
• Buyer Consultations — Structured system from brief to offer support
• Administration — Transaction checklists, viewing notes, pipeline reviews
• Market Intelligence — Monthly analysis distributed across all channels

All content Fair Housing compliant. MLS and US market standards throughout.

Includes the agent business plan system, geographic farming guide, investor/luxury market specialisation, and referral partnership framework.

Free companion: picubiancamaria.gumroad.com/l/rgnko/B06READER""",
    "B0HCZLBJXS": """52,000 copy-paste operations per year. All of them unnecessary.

The average knowledge worker performs 52,000 copy-paste operations annually — moving information between systems that should be connected. ProcessMaker's 2024 analysis of 4 million data points puts this at 289 hours per year — more than 7 full working weeks — spent on zero-value data transfer.

Automate Your Work with AI gives you 10 no-code automations using tools that are mostly free:

• Email filtering (Gmail — free, 30 minutes setup)
• Meeting transcription and AI summaries (Otter.ai — free)
• Workflow automation (Zapier/Make.com — free plans)
• Social media scheduling (Buffer — free)
• Automated invoicing (Wave — free forever)
• Meeting scheduling (Calendly — free)
• AI document templates (ChatGPT/Claude)
• Data synthesis automation
• Content repurposing system
• Weekly review automation

Total setup time: 4 hours. Weekly time saved: 10+ hours.

No coding. No IT department. No enterprise budget. Just the free and low-cost tools that already exist, connected intelligently.

Includes 15 additional automations, the one-year implementation calendar, and role-specific guides for consultants, marketing professionals, HR, sales, and educators.

Free companion: picubiancamaria.gumroad.com/l/rgnko/B07READER""",
    # --- The 1'st AI Engineering Series ---
    "B0GS77LKB2": """If you already know how to write a prompt — this is the book that shows you how to build systems around them.

Prompt Engineering Mastery is the advanced practitioner's guide for teams shipping LLM systems at scale: complex RAG pipelines, agentic workflows, security hardening, and evaluation infrastructure. It is the direct systems-level continuation of the prompting craft.

THIS BOOK IS FOR YOU IF:

• You're building RAG pipelines and need faithfulness consistently above 90%
• You're designing agentic workflows where prompt failures have cascading consequences
• You need to defend against prompt injection in a production application
• You want to evaluate prompts systematically with eval sets, not by feel
• You need a current reference for GPT-4o, Claude 3.x, and Gemini 1.5 — updated for 2026

New to prompt engineering? Start with The Art of Prompt Engineering or Prompt Engineering: From Basics to Advanced.

THREE PRODUCTION CASE STUDIES — FULL BEFORE/AFTER IN PART IV:

• Contract extraction: Manual review 40% → 16%. Three prompt failures identified and fixed. Same model.
• Document QA: RAG faithfulness 70% → 94%. One grounding instruction change. Full prompt included.
• Support chatbot: Escalation rate reduced 67% through refusal boundary redesign.

2026 EDITION — WHAT'S UPDATED:

• Model-specific patterns for GPT-4o, Claude 3.x, Gemini 1.5
• Security chapter: 6 new injection attack patterns from production environments
• Agentic prompt design: dedicated coverage — fundamentally different from chat prompting
• RAG chapter: updated with current production case studies

17 CHAPTERS + APPENDIX B: Battle-Tested Prompt Templates — production-ready, tested against real systems, copy and adapt immediately.

The patterns that reduced manual review by 60%, improved RAG faithfulness to 94%, and cut support escalations by 67% are documented in full — including the prompts that failed and the specific changes that fixed them.""",
    "B0GRGR4DHP": """"Mastering Large Language Models: From Theory to Production" is the definitive guide for anyone who wants to deeply understand and implement large language models in production. Written by Picu Bianca-Maria, this book offers a "Senior Architect" perspective on the entire LLM lifecycle, from theoretical foundations to complex production implementations. The book covers all essential aspects: from Transformer architecture and pre-training, to fine-tuning, prompt engineering, RAG, optimization, deployment, scaling, and security. Each chapter is an original synthesis, based on a vast bibliography, but reformulated with unique analogies and critical comparisons.

What you will learn:
• Foundations: Deep understanding of Transformer architecture and language model evolution
• Training: Pre-training and fine-tuning, including PEFT techniques like LoRA and QLoRA
• Prompt Engineering: From fundamentals to advanced techniques (chain-of-thought, tree-of-thought)
• RAG: Implementing Retrieval-Augmented Generation systems
• Optimization: Quantization, pruning, distillation for efficiency
• Deployment: Deployment strategies, API design, testing
• Scaling: Distributed training and inference
• Monitoring: Observability, logging, alerting for LLM systems
• Cost Management: Cost optimization and resource management
• Security: Protection against attacks, prompt injection, best practices
• Evaluation: Metrics, benchmarks, A/B testing
• Case Studies: Real-world implementations and lessons learned
• Future: Emerging trends and new architectures

This book is the essential resource for developers, data scientists, and AI engineers who want to build robust, scalable, and efficient LLM systems.""",
    "B0GRMHPWD8": """"LLM Engineering: Building Production-Ready Language Models" is the essential guide for engineers building and implementing LLM systems in production. Written by Picu Bianca-Maria, this book offers a "Senior Architect" perspective on the entire LLM engineering lifecycle, from architecture and training to deployment, scaling, and maintenance. The book covers all essential aspects of LLM engineering: data pipelines, training infrastructure, fine-tuning, versioning, API design, caching, load balancing, error handling, testing, CI/CD, cost management, compliance, monitoring, and troubleshooting. Each chapter is an original synthesis, based on a vast bibliography, but reformulated with unique analogies and critical comparisons.

What you will learn:
• Foundations: Understanding LLM architecture and essential components
• Training: Data pipelines, hardware infrastructure, optimizations
• Fine-tuning: Workflows, PEFT, LoRA, best practices
• Management: Versioning, registries, metadata, lineage
• API Design: RESTful, GraphQL, streaming, error handling
• Performance: Caching, latency optimization, throughput
• Scaling: Load balancing, auto-scaling, resource allocation
• Resilience: Error handling, retry strategies, circuit breakers
• Testing: Unit, integration, performance, A/B testing
• CI/CD: ML pipelines, automation, deployment, rollback
• Cost Management: Analysis, budgeting, optimization, ROI
• Compliance: GDPR, AI regulations, audit trails
• Monitoring: Metrics, logging, alerting, dashboards
• Troubleshooting: Debugging, common issues, solutions
• Scaling: Architectures for millions of users

This book is the essential resource for ML engineers, software engineers, and DevOps who want to build robust, scalable, and efficient LLM systems for production.""",
    "B0GSH9XQF2": """You're not getting the results you want from ChatGPT. Not because the model is limited — but because there's a skill behind consistently useful AI output that nobody taught you. This book teaches that skill, from the first prompt you've ever written to building workflows that professionals depend on daily.

THIS BOOK IS FOR YOU IF:

• You use ChatGPT, Claude, or Gemini and know you're not getting full value
• You're a professional — developer, analyst, writer, manager, consultant — who wants to work faster with AI
• You want structure and repeatable systems, not random tips
• You have no ML background and don't need one

Need advanced RAG, security, or agentic workflows? See Prompt Engineering Mastery. This book is your foundation.

THE DIFFERENCE ONE BOOK MAKES:

Before: "Summarize this document." → Generic, wrong length, missing key points, unusable.

After: "Summarize for a technical lead. 3 bullets. Format: [Decision Required] + [Risk if Delayed]. Source only." → Consistent, useful, exactly right.

The difference is not intelligence. It is structure. This book teaches the structure.

17 CHAPTERS — YOUR COMPLETE LEARNING PATH:

• Start: Ch.2 Your First Prompts · Ch.3 Token Limits · Ch.4 Basic Patterns
• Build: Ch.5 Intermediate · Ch.6 Advanced · Ch.7–10 Writing/Code/Analysis/Creative
• Systematize: Ch.11 Multi-Turn · Ch.12 Your Template Library · Ch.13 Testing
• Master: Ch.14 Mistakes · Ch.15 Tools · Ch.16 Real Workflows · Ch.17 Next Steps

APPENDIX A: Prompt Review Checklists · APPENDIX B: 40 Reusable Prompt Starters for writing, analysis, code, research, and creative work.""",
    "B0GSC87H47": """Your AI system is not giving inconsistent results because the model is bad. It is giving inconsistent results because the prompt is underspecified. That is not a model problem — it is a design problem, and it has a design solution.

THIS BOOK IS FOR YOU IF:

• You build AI-powered features and need prompts reliable enough to ship
• You're paying more in API costs than you should and want the math
• Your RAG system answers confidently but incorrectly too often
• You want the craft of prompting, not a list of tips

Looking for advanced RAG, agentic workflows, or security engineering? That's Prompt Engineering Mastery. This book covers the fundamental craft that makes every system work reliably.

THE THREE NUMBERS THAT EXPLAIN WHY THIS BOOK EXISTS:

• $875/month saved at 1M daily API calls — from prompt token optimization alone. No model change. (Chapter 13)
• 70% → 94% RAG faithfulness — by adding one precisely worded grounding instruction. Same model, same retriever. (Chapter 16)
• 60% less manual review — by specifying output format and adding refusal boundaries. (Chapter 16)

17 CHAPTERS: THE COMPLETE PROMPTING CRAFT

• Foundations: LLM behavior · design principles · instruction following · context management
• Output Design: Structured outputs · role prompts · code prompts · creative prompts
• Systems: Prompt chaining · adaptive strategies · A/B testing · cost optimization
• Production: Error recovery · tools · case studies with real ROI · advanced techniques

Works with GPT-4, GPT-4o, Claude, Gemini, and every major frontier model. Patterns are model-agnostic by design.

"The best practitioners treat prompts as versioned artifacts. They document why each instruction exists. They test against representative inputs. They measure success with objective criteria. Fortune 500 companies now employ dedicated prompt engineers because the ROI is measurable: a single well-crafted prompt can eliminate hundreds of hours of downstream rework." — Chapter 1""",
    # Published listing mistakenly uses author bio as product description (live on Amazon)
    "B0GSL5DCHN": """Picu Bianca-Maria is an independent technical author and Python developer working on production AI systems, LLM infrastructure, and the operational discipline that separates a working demo from software a business can rely on.

She writes and publishes alone — no publisher, no editorial team, no marketing budget. Eighteen books built in the hours around other work, along with the software that accompanies them: seven production Python codebases with 283 automated tests, and a local retrieval application that answers questions from a book by quoting it with sources rather than generating prose around it.

That last decision is not incidental. It is the principle her books argue for throughout: a system you cannot audit is a system you cannot trust, and fluent output is not the same thing as correct output. Building the tools taught her the failure modes she writes about more sharply than writing alone would have.

Her books cover LLM engineering and production AI, prompt engineering, AI agents, and practical AI for teachers, lawyers, real estate agents, and knowledge workers. She also writes dark romantasy under the Harbor Light series.

Readers have found her work from the United Kingdom, Brazil, the United States, and India, without advertising. If a book was useful to you, a review is how the next reader finds it.""",
    # Author-pasted authoritative Amazon description
    "B0GHPVL52F": """Friday. 4:52 PM. Your agent — the one that looked brilliant in staging — sends the wrong answer to a real customer, calls the wrong tool on live data, and leaves your team reconstructing what happened from incomplete logs. This is how production agent failures actually happen: not spectacular model breakdowns, but quiet engineering failures the system was never designed to survive.

THIS BOOK IS FOR YOU IF:

• You have a working agent and need to make it production-ready
• You work with LangChain, LlamaIndex, AutoGen, CrewAI, or custom stacks
• You need tool safety, monitoring, and security — not another "getting started" tutorial
• You are responsible for agent systems where failures have real business consequences

WHAT BREAKS IN PRODUCTION — AND HOW THIS BOOK FIXES IT

• Tool misuse → Chapter 3–4: safety contracts, input validation, write-access controls
• Planning loops that never terminate → Chapter 5–6: bounded planners, loop guards, step limits
• State corruption across sessions → Chapter 9: state design patterns, consistency guarantees
• Zero observability when things break → Chapter 11: structured logging, session replay, alerting
• Prompt injection and data leakage → Chapter 13: security hardening, access control, adversarial defense

THE PRODUCTION READINESS LADDER

The core framework of this book: a clear path from Demo-Capable → Assisted → Guarded → Trusted → Scaled. Most teams fail not because they lack capability, but because they jump from Level 1 to Level 5 without earning each level of operational maturity.

17 CHAPTERS + 2 APPENDICES — Design Review Checklists · Release Approval Checklists · Reusable Templates

Compatible with OpenAI, Anthropic, and open-source models. Works with LangChain, LlamaIndex, AutoGen, and CrewAI.

The teams mastering production agent engineering in 2026 will define what reliable AI means in their organizations. The teams skipping it will spend Q3 fixing what they shipped in Q1.""",
}


def plain_to_amazon_html(title: str, plain: str) -> str:
    """Convert plain Amazon description to KDP-safe HTML tags."""
    parts: list[str] = [f"<h2>{html.escape(title)}</h2>"]
    blocks = re.split(r"\n\s*\n", plain.strip())
    for block in blocks:
        lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        bullets = [ln for ln in lines if re.match(r"^[•\-\*]\s+", ln)]
        if len(bullets) == len(lines) and bullets:
            parts.append("<ul>")
            for ln in bullets:
                item = re.sub(r"^[•\-\*]\s+", "", ln)
                parts.append(f"<li>{html.escape(item)}</li>")
            parts.append("</ul>")
            continue
        # Heading-like ALL CAPS short lines
        if len(lines) == 1 and lines[0].isupper() and len(lines[0]) < 80:
            parts.append(f"<h3>{html.escape(lines[0])}</h3>")
            continue
        if len(lines) == 1 and lines[0].endswith(":") and len(lines[0]) < 80:
            parts.append(f"<h3>{html.escape(lines[0].rstrip(':'))}</h3>")
            continue
        # First line bold hook when short
        if len(lines) == 1:
            parts.append(f"<p><b>{html.escape(lines[0])}</b></p>" if len(lines[0]) < 160 else f"<p>{html.escape(lines[0])}</p>")
        else:
            # mix: first as bold if looks like section header
            first = lines[0]
            rest = lines[1:]
            if first.isupper() or first.endswith(":"):
                parts.append(f"<h3>{html.escape(first.rstrip(':'))}</h3>")
                bulletish = [ln for ln in rest if re.match(r"^[•\-\*]\s+", ln) or "→" in ln]
                if len(bulletish) == len(rest) and rest:
                    parts.append("<ul>")
                    for ln in rest:
                        item = re.sub(r"^[•\-\*]\s+", "", ln)
                        parts.append(f"<li>{html.escape(item)}</li>")
                    parts.append("</ul>")
                else:
                    parts.append(f"<p>{html.escape(' '.join(rest))}</p>")
            else:
                parts.append(f"<p>{html.escape(' '.join(lines))}</p>")
    return "".join(parts)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    missing: list[str] = []
    for series, books in config.TECH_BOOKS.items():
        for book in books:
            asin = book["asin"]
            plain = (DESCRIPTIONS.get(asin) or "").strip()
            if not plain:
                missing.append(f"{asin} {book['title']}")
                continue
            payload = {
                "title": book["title"],
                "asin": asin,
                "series": series,
                "amazon_link": book["amazon_link"],
                "description_plain": plain,
                "html_description": plain_to_amazon_html(book["title"], plain),
                "source": f"https://www.amazon.com/dp/{asin}",
                "source_note": "Published Amazon product description (author paste / live listing)",
            }
            (OUT / f"{asin}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            (OUT / f"{asin}.html").write_text(
                payload["html_description"] + "\n",
                encoding="utf-8",
            )
            written += 1
            print(f"OK {asin} ({len(plain)} chars)")
    print(f"Wrote {written} tech descriptions → {OUT}")
    if missing:
        print("MISSING descriptions (add to DESCRIPTIONS dict):")
        for m in missing:
            print(f"  - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
