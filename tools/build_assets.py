#!/usr/bin/env python3
"""Build web-optimized image assets for the TokenWise site from the raw app
screenshots.

Reads raw macOS screenshots (per language) and emits compact WebP versions into
`assets/{en,zh}/`, plus a favicon and a 1200x630 Open Graph card.

Usage:
    python tools/build_assets.py --src /path/to/appstore/screenshots/raw
    (--src defaults to the sibling TokenWise repo's appstore raw folder)
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ASSETS = os.path.join(REPO, "assets")
ICON = os.path.join(REPO, "..", "TokenWise", "TokenWise", "Assets.xcassets",
                    "AppIcon.appiconset", "icon_256.png")
PINGFANG = "/System/Library/Fonts/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
BG = (11, 13, 16)  # #0b0d10

# raw file -> (output name, target width in px). Height follows aspect ratio.
SHOTS = {
    "S1.png": ("overview", 760),       # menu-bar popover (tall/narrow)
    "S2.png": ("analysis", 1600),      # detail window · analysis
    "S3.png": ("conversations", 1600), # detail window · conversation
    "S4.png": ("settings", 1200),      # settings · general
}


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def resize_to_width(im, w):
    if im.width <= w:
        return im
    h = round(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS)


def build_shots(src):
    for lang in ("en", "zh"):
        outdir = os.path.join(ASSETS, lang)
        os.makedirs(outdir, exist_ok=True)
        for raw, (name, width) in SHOTS.items():
            p = os.path.join(src, lang, raw)
            if not os.path.exists(p):
                print("  skip %s/%s (missing %s)" % (lang, raw, p))
                continue
            # macOS window captures carry an alpha shadow — composite onto the
            # frame bg so the baked shadow blends and there is no black fringe.
            src_im = Image.open(p).convert("RGBA")
            flat = Image.new("RGB", src_im.size, BG)
            flat.paste(src_im, mask=src_im.split()[-1])
            im = resize_to_width(flat, width)
            out = os.path.join(outdir, name + ".webp")
            im.save(out, "WEBP", quality=88, method=6)
            print("  -> %s  %dx%d  %.0fKB" %
                  (os.path.relpath(out, REPO), im.width, im.height,
                   os.path.getsize(out) / 1024))


def build_icon_and_favicon():
    os.makedirs(ASSETS, exist_ok=True)
    icon = Image.open(ICON).convert("RGBA")
    icon.resize((256, 256), Image.LANCZOS).save(os.path.join(ASSETS, "icon.png"))
    icon.resize((64, 64), Image.LANCZOS).save(os.path.join(ASSETS, "favicon.png"))
    print("  -> assets/icon.png, assets/favicon.png")


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, im.size[0] - 1, im.size[1] - 1], radius=radius, fill=255)
    im = im.convert("RGBA")
    im.putalpha(mask)
    return im


def build_og():
    """1200x630 branded share card: gradient + icon + wordmark + tagline."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), BG)
    # soft radial-ish glow via a blurred violet blob
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 640, -260, W + 260, 360], fill=(34, 26, 74))
    gd.ellipse([-260, H - 320, 420, H + 260], fill=(20, 30, 66))
    from PIL import ImageFilter
    card = Image.blend(card, glow.filter(ImageFilter.GaussianBlur(160)), 0.9)
    d = ImageDraw.Draw(card)
    # app icon
    try:
        ic = rounded(Image.open(ICON).convert("RGBA").resize((132, 132), Image.LANCZOS), 30)
        card.paste(ic, (96, 150), ic)
    except Exception as e:
        print("  og icon skipped:", e)
    # wordmark + tagline
    d.text((250, 168), "TokenWise", font=font(HELVETICA, 92), fill=(245, 247, 250))
    d.text((252, 292), "AI coding token usage, right in your menu bar.",
           font=font(HELVETICA, 40), fill=(150, 160, 176))
    d.text((252, 356), "Claude Code · Codex · OpenCode · Gemini",
           font=font(HELVETICA, 32), fill=(120, 130, 146))
    # accent underline
    d.rounded_rectangle([252, 250, 252 + 150, 250 + 6], radius=3, fill=(138, 124, 255))
    card.save(os.path.join(ASSETS, "og.png"))
    print("  -> assets/og.png  1200x630")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(
        REPO, "..", "TokenWise", "appstore", "screenshots", "raw"),
        help="raw screenshots root containing en/ and zh/")
    args = ap.parse_args()
    print("building shots from", args.src)
    build_shots(args.src)
    build_icon_and_favicon()
    build_og()
    print("done.")


if __name__ == "__main__":
    main()
