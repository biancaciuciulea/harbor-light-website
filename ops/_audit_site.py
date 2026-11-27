"""One-shot functional audit for harbor-light-website/docs."""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

RO_PAT = re.compile(
    r"Română|română|limba rom|lang=[\"']ro|hreflang=[\"']ro|-ro\.html|/ro/",
    re.I,
)
HREF_PAT = re.compile(r"""(?:href|src)=["']([^"'#]+)""", re.I)
AMAZON_BAD = re.compile(r"amazon\.(de|fr|es|it|co\.uk)/dp/", re.I)
AMAZON_OK = re.compile(r"amazon\.com/dp/", re.I)


def public_html() -> list[Path]:
    return sorted(
        p
        for p in DOCS.rglob("*.html")
        if "paste" not in p.parts and p.is_file()
    )


def rel(p: Path) -> str:
    return str(p.relative_to(DOCS)).replace("\\", "/")


def main() -> int:
    htmls = public_html()
    print(f"Public HTML files: {len(htmls)}")

    print("\n=== 1. RO purge (excl paste/) ===")
    ro_hits = []
    for p in htmls:
        text = p.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if RO_PAT.search(line) or "căutări în română" in line.lower() or "Pentru căutări" in line:
                ro_hits.append((rel(p), i, line.strip()[:140]))
    if not ro_hits:
        print("PASS: no Romanian public chrome hits")
    else:
        print(f"FAIL/NOTE: {len(ro_hits)} hits")
        for h in ro_hits[:40]:
            print(f"  {h[0]}:{h[1]}: {h[2]}")

    print("\n=== 2. Cap1 sample inventory ===")
    samples = sorted(DOCS.glob("harbor-light-sample*.html"))
    for s in samples:
        print(f"  {s.name}")

    print("\n=== 3. ARC hubs Free Ch1 wiring ===")
    for hub in [
        DOCS / "arc.html",
        DOCS / "de" / "arc.html",
        DOCS / "fr" / "arc.html",
        DOCS / "es" / "arc.html",
        DOCS / "it" / "arc.html",
    ]:
        text = hub.read_text(encoding="utf-8", errors="replace")
        ch1 = re.findall(r'arc-hub-ch1[^>]+href="([^"]+)"[^>]*>\s*([^<]+)', text)
        books = re.findall(r'data-book="(\d+)"', text)
        print(f"  {rel(hub)}: books={books} ch1={[(h, t.strip()) for h, t in ch1]}")
        # English chrome leak on non-EN
        if hub.parent.name in {"de", "fr", "es", "it"}:
            for bad in ("Free Chapter", "Request ARC", "Apply for", "Join ARC", "Submit the form"):
                if bad in text:
                    print(f"    WARN English chrome: {bad!r}")

    print("\n=== 4. GAS form endpoints ===")
    arc_forms = sorted((DOCS / "arc").glob("*.html"))
    gas = set()
    missing = []
    for p in arc_forms:
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'action="(https://script\.google\.com/[^"]+)"', text)
        if m:
            gas.add(m.group(1))
        else:
            missing.append(rel(p))
    print(f"  forms={len(arc_forms)} unique_endpoints={len(gas)}")
    for g in gas:
        print(f"  {g}")
    if missing:
        print(f"  FAIL missing GAS: {missing}")
    else:
        print("  PASS: all ARC forms POST to GAS")

    print("\n=== 5. Broken local href/src (spot key pages + all samples/arc) ===")
    key = []
    for name in [
        "index.html",
        "harbor-light.html",
        "arc.html",
        "music.html",
        "content-warnings.html",
        "slow-burn-dark-mafia-romance.html",
        "cinematic-dark-mafia-romance-audiobook.html",
        "mafia-romance-audiobooks.html",
    ]:
        p = DOCS / name
        if p.exists():
            key.append(p)
    key += list((DOCS).glob("harbor-light-sample*.html"))
    key += [DOCS / "de" / "arc.html", DOCS / "fr" / "arc.html", DOCS / "es" / "arc.html", DOCS / "it" / "arc.html"]
    key += list((DOCS / "arc").glob("*.html"))
    # tech pages
    for p in DOCS.glob("*.html"):
        if "tech" in p.name.lower() or "ai-" in p.name.lower():
            key.append(p)
    for sub in ("de", "fr", "es", "it", "en"):
        for name in ("content-warnings.html", "slow-burn-dark-mafia-romance.html", "index.html", "arc.html"):
            p = DOCS / sub / name
            if p.exists():
                key.append(p)

    broken = []
    checked = set()
    for page in key:
        if page in checked or not page.exists():
            continue
        checked.add(page)
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in HREF_PAT.findall(text):
            raw = unquote(raw.strip())
            if raw.startswith(("http://", "https://", "mailto:", "data:", "//", "javascript:")):
                continue
            if raw.startswith("#"):
                continue
            # Strip query/hash so ?book=1 language switches are not false 404s
            raw_path = raw.split("?", 1)[0].split("#", 1)[0]
            if not raw_path:
                continue
            target = (page.parent / raw_path).resolve()
            # stay under docs
            try:
                target.relative_to(DOCS.resolve())
            except ValueError:
                continue
            if not target.exists():
                broken.append((rel(page), raw, str(target)))

    if not broken:
        print("PASS: no broken local refs on key pages")
    else:
        print(f"FAIL: {len(broken)} broken refs")
        for b in broken[:60]:
            print(f"  {b[0]} -> {b[1]}")

    print("\n=== 6. Amazon CTAs on public pages (excl paste, excl episode body may have local) ===")
    bad_amazon = []
    ok_count = 0
    for p in htmls:
        if "paste" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        # Only count href attributes for site CTAs
        for href in re.findall(r'href=["\'](https?://[^"\']+)["\']', text, re.I):
            if AMAZON_BAD.search(href):
                bad_amazon.append((rel(p), href))
            elif AMAZON_OK.search(href):
                ok_count += 1
    print(f"  amazon.com/dp hrefs: {ok_count}")
    if not bad_amazon:
        print("  PASS: no amazon.<tld>/dp in href CTAs")
    else:
        print(f"  FAIL/NOTE: {len(bad_amazon)} local-tld Amazon hrefs")
        for b in bad_amazon[:30]:
            print(f"    {b[0]}: {b[1]}")

    print("\n=== 7. Sample lang switchers: RO links? ===")
    for s in samples:
        text = s.read_text(encoding="utf-8", errors="replace")
        ro_links = re.findall(r'href=["\']([^"\']*ro[^"\']*)["\']', text, re.I)
        # filter noise
        ro_links = [h for h in ro_links if re.search(r"-ro\.html|/ro/|lang=ro|Română", h, re.I)]
        if "Română" in text or ro_links:
            print(f"  WARN {s.name}: RO={ro_links[:5]} Română={'Română' in text}")

    print("\n=== 8. Cover assets referenced by ARC hubs ===")
    for hub in [DOCS / "arc.html", DOCS / "de" / "arc.html", DOCS / "it" / "arc.html"]:
        text = hub.read_text(encoding="utf-8", errors="replace")
        for src in re.findall(r'src="(\.\./assets/harbor/[^"]+|./assets/harbor/[^"]+|assets/harbor/[^"]+)"', text):
            target = (hub.parent / src).resolve()
            ok = target.exists()
            print(f"  {rel(hub)} {src} -> {'OK' if ok else 'MISSING'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
