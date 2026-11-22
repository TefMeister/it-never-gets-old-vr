#!/usr/bin/env python3
"""picture_mood.py -- give a picture one of our Fallout moods (for the main menu, the splash, Mod Organizer's look).

    python picture_mood.py <in.png> <out.png> --mood <name> [--seed 1955]
    python picture_mood.py <in.png> <out folder> --all        (every mood, numbered, for Tefa to pick)
    add --pixel 4 for the retro pixel look (the menu picture since 2026-11-22: tw-vivid + --pixel 4)

Moods (Tefa 2026-11-20, from the poster tries):
  tw-vivid    Two Wastelands, vivid: Fallout 3 green in the shadows, New Vegas amber in the light, colour kept,
              old-film lines (scratches, dust, faint scan lines, grain). Tefa's favourite on the first poster.
  tw-dark     the same, darker and calmer: room for the menu words to read over it.
  fo3-green   Fallout 3's washed-out olive green over everything.
  bleak       drained, dusty sepia, dark edges, heavy grain: an old print found in a vault.
Only our own maths on the picture; the picture itself is Tefa's.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageFilter

W = np.array([0.299, 0.587, 0.114], dtype=np.float32)
GREEN = np.array([0.80, 1.00, 0.68], dtype=np.float32)    # Fallout 3
AMBER = np.array([1.10, 0.92, 0.58], dtype=np.float32)    # New Vegas


def lum(img):
    return img @ W


def saturate(img, k):
    l = lum(img)[..., None]
    return l + (img - l) * k


def contrast(img, k):
    return img + k * (img - 0.5) * (1 - np.abs(2 * img - 1))


def bloom(img, amount):
    pil = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
    blur = np.asarray(pil.filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255
    hi = np.clip(blur - 0.55, 0, None) / 0.45
    return 1 - (1 - np.clip(img, 0, 1)) * (1 - hi * amount)


def vignette(img, k):
    h, w, _ = img.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    return img * (1 - k * np.clip(d - 0.5, 0, None) ** 1.5)[..., None]


def two_wastelands(img, keep, mix):
    img = saturate(img, keep)
    l = lum(img)
    t = np.clip((l - 0.25) / 0.6, 0, 1)[..., None]
    tint = GREEN * (1 - t) + AMBER * t
    return img * (1 - mix) + (img * tint) * mix + (l[..., None] * tint - l[..., None]) * 0.25


def film_lines(img, rng, strength=1.0):
    h, w, _ = img.shape
    lines = np.zeros((h, w), dtype=np.float32)
    for _ in range(14):
        x = rng.uniform(0, w)
        y0 = 0 if rng.random() < 0.5 else int(rng.integers(0, h // 2))
        y1 = h if rng.random() < 0.6 else int(rng.integers(y0 + h // 6, h))
        val, width, period = rng.choice([0.22, 0.16, -0.18]) * strength, int(rng.choice([1, 1, 2])), rng.uniform(40, 120)
        for y in range(y0, y1):
            xi = int(x + 1.5 * np.sin(y / period))
            if 0 <= xi < w - width:
                lines[y, xi:xi + width] += val
    for _ in range(40):
        x, y0, ln = rng.integers(0, w), rng.integers(0, h), rng.integers(h // 15, h // 2)
        lines[y0:min(h, y0 + ln), x] += rng.choice([0.08, -0.07]) * strength
    for _ in range(260):
        x, y, s = rng.integers(0, w - 4), rng.integers(0, h - 4), rng.integers(1, 4)
        lines[y:y + s, x:x + s] += rng.choice([-0.35, 0.3]) * strength
    lines = np.asarray(Image.fromarray(((lines + 1) * 127.5).clip(0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.5))).astype(np.float32) / 127.5 - 1
    img = img + lines[..., None]
    img = img * (1 - 0.06 * ((np.arange(h) % 3) == 0))[:, None, None]
    return img + rng.normal(0, 0.025, (h, w)).astype(np.float32)[..., None]


def mood(img, name, rng):
    if name == "tw-vivid":
        img = two_wastelands(img, 0.85, 0.4)
        img = saturate(contrast(0.03 + img * 0.95, 0.22), 1.2)
        img = vignette(bloom(img, 0.3), 0.35)
        return film_lines(img, rng)
    if name == "tw-dark":
        img = two_wastelands(img, 0.7, 0.5)
        img = saturate(contrast(0.02 + img * 0.78, 0.18), 1.05)
        img = vignette(bloom(img, 0.2), 0.55)
        return film_lines(img, rng, 0.7)
    if name == "fo3-green":
        img = saturate(img, 0.35)
        l = lum(img)
        img = img * 0.35 + np.stack([l * 0.86, l * 1.02, l * 0.70], -1) * 0.65
        img = contrast(0.05 + img * 0.88, 0.15)
        return vignette(bloom(img, 0.35), 0.35)
    if name == "bleak":
        img = saturate(img, 0.3)
        img = img * 0.4 + (img * np.array([1.06, 0.98, 0.82], dtype=np.float32)) * 0.6
        img = contrast(0.07 + img * 0.78, 0.12)
        img = vignette(img, 0.55)
        return film_lines(img, rng, 0.8)
    raise SystemExit("unknown mood: " + name)


MOODS = ["tw-vivid", "tw-dark", "fo3-green", "bleak"]


MENU_SIZE = (1920, 1080)   # the game's menu picture size; --pixel works at this size so a block is that many screen pixels


def pixelate(im, block):
    """Retro pixel look (Tefa 2026-11-22, "nr 1" = block 4): average each block x block square, then blow it back up hard-edged."""
    im = im.resize(MENU_SIZE, Image.LANCZOS)
    small = im.resize((MENU_SIZE[0] // block, MENU_SIZE[1] // block), Image.BOX)
    return small.resize(MENU_SIZE, Image.NEAREST)


def run(src, dst, name, seed, pixel=0):
    img = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255
    out = np.clip(mood(img, name, np.random.default_rng(seed)), 0, 1)
    pic = Image.fromarray((out * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.3))
    if pixel > 1:
        pic = pixelate(pic, pixel)
    pic.save(dst)
    print("written:", dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--mood", choices=MOODS)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--seed", type=int, default=1955)
    ap.add_argument("--pixel", type=int, default=0, help="retro pixel squares this many screen pixels wide (4 = Tefa's pick)")
    a = ap.parse_args()
    if a.all:
        os.makedirs(a.dst, exist_ok=True)
        for i, m in enumerate(MOODS, 1):
            run(a.src, os.path.join(a.dst, f"{i} {m}.png"), m, a.seed, a.pixel)
    else:
        run(a.src, a.dst, a.mood, a.seed, a.pixel)


if __name__ == "__main__":
    main()
