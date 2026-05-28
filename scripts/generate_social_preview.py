#!/usr/bin/env python3
"""Generate the social preview image used for launch posts."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "social-preview.png"
WIDTH = 1280
HEIGHT = 640

FONT_DIR = Path("C:/Windows/Fonts")
BOLD_FONT = FONT_DIR / "segoeuib.ttf"
BODY_FONT = FONT_DIR / "segoeui.ttf"
MONO_FONT = FONT_DIR / "CascadiaMono.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    fallback = BODY_FONT
    return ImageFont.truetype(str(path if path.exists() else fallback), size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, typeface: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        left, _, right, _ = draw.textbbox((0, 0), trial, font=typeface)
        if right - left <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def shadow(image: Image.Image, box: tuple[int, int, int, int], radius: int) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=(43, 35, 25, 28))
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    image.alpha_composite(layer)


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)

    image = Image.new("RGBA", (WIDTH, HEIGHT), "#f4efe5")
    draw = ImageDraw.Draw(image)

    # Soft paper field with a few quiet editorial rules.
    draw.rectangle((0, 0, WIDTH, 10), fill="#1f1a14")
    draw.line((72, 122, 720, 122), fill="#d7c8b3", width=1)
    draw.line((72, 590, 720, 590), fill="#d7c8b3", width=1)

    margin = 72
    title_font = font(BOLD_FONT, 44)
    eyebrow_font = font(BOLD_FONT, 22)
    headline_font = font(BOLD_FONT, 58)
    body_font = font(BODY_FONT, 25)
    small_font = font(BODY_FONT, 22)
    mono_font = font(MONO_FONT, 21)

    # Left editorial block.
    rounded_rect(draw, (margin, 74, 240, 116), 18, "#1f1a14")
    draw.text((96, 84), "SKILL", fill="#f4efe5", font=eyebrow_font)
    draw.text((262, 84), "Claude / Codex", fill="#4b4032", font=eyebrow_font)

    draw.text((margin, 152), "advise-project-approach", fill="#1f1a14", font=title_font)

    headline = "Stop choosing your tech stack from vibes."
    y = 246
    for line in wrap_text(draw, headline, headline_font, 570):
        draw.text((margin, y), line, fill="#1f1a14", font=headline_font)
        y += 62

    body = "A skill that researches comparable real projects before recommending your stack, architecture, and build plan."
    y += 2
    for line in wrap_text(draw, body, body_font, 570):
        draw.text((margin + 2, y), line, fill="#5f5344", font=body_font)
        y += 32

    command_box = (margin, 532, 718, 572)
    rounded_rect(draw, command_box, 14, "#fffaf1", "#d7c8b3", 1)
    draw.text(
        (margin + 18, 541),
        "npx skills@latest add AaravKashyap12/advise-project-approach",
        fill="#1f1a14",
        font=mono_font,
    )

    # Right repo/result card.
    card = (744, 92, 1208, 556)
    shadow(image, (card[0] + 8, card[1] + 10, card[2] + 8, card[3] + 10), 24)
    rounded_rect(draw, card, 24, "#fffaf1", "#d7c8b3", 1)

    draw.text((784, 132), "What the skill returns", fill="#1f1a14", font=font(BOLD_FONT, 30))
    draw.line((784, 180, 1168, 180), fill="#ded0bc", width=1)

    items = [
        ("01", "Comparable projects", "real repos, docs, references"),
        ("02", "Stack recommendation", "fit over fashion"),
        ("03", "Architecture direction", "tradeoffs included"),
        ("04", "Wrong-turn warning", "when the advice expires"),
    ]

    y = 215
    for num, label, note in items:
        rounded_rect(draw, (784, y, 832, y + 40), 13, "#eadcc7")
        draw.text((796, y + 6), num, fill="#1f1a14", font=font(BOLD_FONT, 20))
        draw.text((852, y - 2), label, fill="#1f1a14", font=font(BOLD_FONT, 25))
        draw.text((852, y + 28), note, fill="#756956", font=font(BODY_FONT, 19))
        y += 72

    # Bottom mode chips.
    chip_y = 500
    x = 784
    for chip in ["pre-build", "mid-build", "post-build"]:
        left, top, right, bottom = draw.textbbox((0, 0), chip, font=font(BOLD_FONT, 19))
        w = right - left + 30
        rounded_rect(draw, (x, chip_y, x + w, chip_y + 38), 16, "#1f1a14")
        draw.text((x + 15, chip_y + 7), chip, fill="#fffaf1", font=font(BOLD_FONT, 19))
        x += w + 10

    # Small repo hint.
    draw.text((784, 532), "github.com/AaravKashyap12/advise-project-approach", fill="#756956", font=font(MONO_FONT, 15))

    image.convert("RGB").save(OUT, quality=96)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
