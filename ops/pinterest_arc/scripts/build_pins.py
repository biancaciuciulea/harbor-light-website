#!/usr/bin/env python3
"""Compose Harbor Light ARC Pinterest pins (1000x1500) — cover-forward for conversion.

Design law (Pinterest mobile):
- Real book cover dominates (~70%+ of frame)
- One short hook (≤8 words), huge type
- Full-width CTA strip
- Tiny brand only
- Atmosphere from blurred cover / dark harbor — not purple AI slop
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "refs"
OUT = ROOT / "pins"
W, H = 1000, 1500

# Harbor Light brand (site.css) — not purple, not cream-terracotta
BG = (10, 12, 15)
INK = (245, 240, 230)
ACCENT = (196, 165, 116)
STEEL = (126, 184, 201)
MUTED = (168, 160, 148)
CTA_INK = (18, 14, 10)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\garabd.ttf" if bold else r"C:\Windows\Fonts\gara.ttf",
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def _sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def _center_crop(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Cover-fit crop to exact size."""
    src_w, src_h = img.size
    target_ratio = tw / th
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize((tw, th), Image.Resampling.LANCZOS)


def _blurred_cover_bg(cover_path: Path, darken: float = 0.42) -> Image.Image:
    """Atmosphere = the actual cover, blurred + darkened (matches search intent)."""
    img = Image.open(cover_path).convert("RGB")
    bg = _center_crop(img, W, H)
    bg = bg.filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(darken)
    bg = ImageEnhance.Contrast(bg).enhance(1.2)
    return bg


def _mood_bg(name: str, darken: float = 0.45) -> Image.Image:
    path = REFS / name
    if not path.exists():
        return Image.new("RGB", (W, H), BG)
    img = Image.open(path).convert("RGB")
    bg = _center_crop(img, W, H)
    bg = ImageEnhance.Brightness(bg).enhance(darken)
    bg = ImageEnhance.Contrast(bg).enhance(1.15)
    return bg


def _fit_cover_tall(path: Path, max_w: int, max_h: int) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return img


def _shadowed(cover: Image.Image, pad: int = 22) -> Image.Image:
    shadow = Image.new("RGBA", (cover.width + pad * 2, cover.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", cover.size, (0, 0, 0, 170))
    shadow.paste(sh, (pad + 8, pad + 12), sh)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    shadow.paste(cover, (pad, pad), cover)
    return shadow


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _center_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font,
    fill,
    max_width: int = 920,
    line_gap: int = 6,
) -> int:
    lines = _wrap(draw, text, font, max_width)
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text(((W - tw) / 2, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def _bottom_gradient(canvas: Image.Image, start_y: int = 900) -> Image.Image:
    """Dark fade so hook + CTA stay readable over cover art."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for i in range(H - start_y):
        t = i / max(1, H - start_y)
        alpha = int(230 * (t**1.15))
        y = start_y + i
        draw.line([(0, y), (W, y)], fill=(8, 10, 12, alpha))
    return Image.alpha_composite(canvas.convert("RGBA"), overlay)


def _full_cta(draw: ImageDraw.ImageDraw, label: str, y: int = 1385) -> None:
    """Full-width high-contrast CTA strip — readable at mobile thumb size."""
    bar_h = 78
    draw.rectangle([0, y, W, y + bar_h], fill=ACCENT)
    font = _sans(36, bold=True)
    tw = draw.textlength(label, font=font)
    bbox = draw.textbbox((0, 0), label, font=font)
    th = bbox[3] - bbox[1]
    draw.text(((W - tw) / 2, y + (bar_h - th) / 2 - 2), label, font=font, fill=CTA_INK)


def compose_cover_pin(
    *,
    out_name: str,
    cover_name: str,
    hook: str,
    cta: str = "FREE ARC  →",
    eyebrow: str | None = None,
) -> Path:
    """Cover-dominant pin: large real cover + short hook + full CTA."""
    cover_path = REFS / cover_name
    base = _blurred_cover_bg(cover_path, darken=0.38)
    canvas = base.convert("RGBA")

    # Dominant cover — near edge-to-edge (high contrast on mobile feed)
    cover = _fit_cover_tall(cover_path, 920, 1080)
    stamped = _shadowed(cover, pad=16)
    cx = (W - stamped.width) // 2
    cy = 36
    canvas.alpha_composite(stamped, (cx, cy))

    # Gradient under text zone
    canvas = _bottom_gradient(canvas, start_y=1020)
    draw = ImageDraw.Draw(canvas)

    # Tiny brand — top corner, not competing with cover
    brand_f = _sans(15, bold=True)
    draw.text((22, 14), "PICU BIANCA-MARIA", font=brand_f, fill=ACCENT)

    # Optional tiny eyebrow above hook
    text_y = 1205
    if eyebrow:
        text_y = _center_text(draw, eyebrow.upper(), 1180, _sans(18, bold=True), STEEL, max_width=900)
        text_y += 2

    # Huge hook — max ~8 words, mobile-readable
    head_f = _font(52, bold=True)
    _center_text(draw, hook, text_y, head_f, INK, max_width=940, line_gap=2)

    _full_cta(draw, cta, y=1385)

    out = OUT / out_name
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    return out


def compose_series_pin(
    *,
    out_name: str,
    hook: str,
    cta: str = "FREE ARC  →",
) -> Path:
    """Series start: Book 1 cover dominant + START HERE hook."""
    return compose_cover_pin(
        out_name=out_name,
        cover_name="book1-en.jpg",
        hook=hook,
        cta=cta,
        eyebrow="Harbor Light · Start Here",
    )


def compose_recruit_pin(
    *,
    out_name: str,
    hook: str,
) -> Path:
    """ARC recruit: 2×2 cover grid + join CTA (covers sell the genre)."""
    base = _mood_bg("bg_iron_chain.jpg", darken=0.35)
    canvas = base.convert("RGBA")

    covers = [
        REFS / "book1-en.jpg",
        REFS / "book2-en.jpg",
        REFS / "book3-en.jpg",
        REFS / "book4-en.jpg",
    ]
    cell_w, cell_h = 400, 500
    gap = 14
    grid_w = cell_w * 2 + gap
    ox = (W - grid_w) // 2
    oy = 55

    for i, path in enumerate(covers):
        col, row = i % 2, i // 2
        img = Image.open(path).convert("RGBA")
        fitted = _center_crop(img, cell_w, cell_h).convert("RGBA")
        # thin gold rule
        framed = Image.new("RGBA", (cell_w + 4, cell_h + 4), (*ACCENT, 220))
        framed.paste(fitted, (2, 2), fitted)
        x = ox + col * (cell_w + gap)
        y = oy + row * (cell_h + gap)
        canvas.alpha_composite(framed, (x, y))

    canvas = _bottom_gradient(canvas, start_y=1020)
    draw = ImageDraw.Draw(canvas)
    draw.text((28, 18), "PICU BIANCA-MARIA", font=_sans(16, bold=True), fill=ACCENT)

    _center_text(draw, "HARBOR LIGHT · BOOKS 1–4", 1145, _sans(20, bold=True), STEEL)
    _center_text(draw, hook, 1185, _font(46, bold=True), INK, max_width=920, line_gap=4)
    _full_cta(draw, "JOIN ARC TEAM  →", y=1385)

    out = OUT / out_name
    canvas.convert("RGB").save(out, "PNG", optimize=True)
    return out


def compose_trope_pin(
    *,
    out_name: str,
    cover_name: str,
    trope: str,
    hook: str,
) -> Path:
    """Trope pin WITH real cover — never text-only atmosphere."""
    return compose_cover_pin(
        out_name=out_name,
        cover_name=cover_name,
        hook=hook,
        cta="FREE ARC  →",
        eyebrow=trope,
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    # 01 — Series gateway (highest-volume pin)
    made.append(
        compose_series_pin(
            out_name="01_series_start_here.png",
            hook="Free dark mafia ARC",
        )
    )
    # 02 — Book 1
    made.append(
        compose_cover_pin(
            out_name="02_book1_bound_by_blood.png",
            cover_name="book1-en.jpg",
            hook="He draws the contract",
            eyebrow="Bound by Blood · Book 1",
        )
    )
    # 03 — Book 2
    made.append(
        compose_cover_pin(
            out_name="03_book2_soft_marks.png",
            cover_name="book2-en.jpg",
            hook="His name is already marked",
            eyebrow="Soft Marks · Book 2",
        )
    )
    # 04 — Book 3
    made.append(
        compose_cover_pin(
            out_name="04_book3_soft_hour.png",
            cover_name="book3-en.jpg",
            hook="Clinic under the empire",
            eyebrow="Soft Hour · Book 3",
        )
    )
    # 05 — Book 4
    made.append(
        compose_cover_pin(
            out_name="05_book4_soft_gate.png",
            cover_name="book4-en.jpg",
            hook="HEA that still costs",
            eyebrow="Soft Gate · Book 4",
        )
    )
    # 06 — Recruit (cover grid)
    made.append(
        compose_recruit_pin(
            out_name="06_arc_team_recruit.png",
            hook="Join the ARC Team",
        )
    )
    # 07–10 — Trope pins WITH covers (Book 1 as conversion default)
    made.append(
        compose_trope_pin(
            out_name="07_trope_dark_mafia.png",
            cover_name="book1-en.jpg",
            trope="Dark Mafia Romance",
            hook="Loyalty seals. Marriage pact.",
        )
    )
    made.append(
        compose_trope_pin(
            out_name="08_trope_slow_burn.png",
            cover_name="book1-en.jpg",
            trope="Slow Burn Romance",
            hook="Heat earned. Never rushed.",
        )
    )
    made.append(
        compose_trope_pin(
            out_name="09_trope_forced_proximity.png",
            cover_name="book2-en.jpg",
            trope="Forced Proximity",
            hook="Shared walls. No escape.",
        )
    )
    made.append(
        compose_trope_pin(
            out_name="10_trope_dual_pov.png",
            cover_name="book1-en.jpg",
            trope="Dual POV Romance",
            hook="Her dark. His steel.",
        )
    )

    print(f"Wrote {len(made)} pins → {OUT}")
    for p in made:
        print(f"  {p.name}  ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
