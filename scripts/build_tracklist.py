#!/usr/bin/env python3
"""Build a 1080x1440 tracklist card for Rednote notes.

Usage:
    python build_tracklist.py \
        --cover cover.jpg \
        --tracks tracks.json \
        --out tracklist.jpg \
        --artist "Karmanjakah" \
        --album "Diamond Morning" \
        --year 2026

tracks.json format:
    {
      "tracks": [
        {"n": 1, "title": "Dove", "duration": "4:05"},
        ...
      ]
    }
"""
import argparse
import json
import os
from PIL import Image, ImageDraw, ImageFont

BG = (18, 28, 48)          # deep navy
WHITE = (245, 245, 245)
GRAY = (150, 170, 190)


def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fmt_duration(ms):
    s = int(ms // 1000)
    return f"{s // 60}:{s % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--artist", default="")
    ap.add_argument("--album", default="")
    ap.add_argument("--year", default="")
    args = ap.parse_args()

    with open(args.tracks, "r", encoding="utf-8") as f:
        data = json.load(f)
    tracks = data["tracks"]

    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Title
    title_font = load_font(44, bold=True)
    sub_font = load_font(24)
    d.text((60, 50), args.artist.upper(), font=title_font, fill=WHITE)
    sub = f"{args.album} · {args.year} · {len(tracks)} Tracks" if args.year \
        else f"{args.album} · {len(tracks)} Tracks"
    d.text((60, 110), sub, font=sub_font, fill=GRAY)

    # Cover centered
    cover = Image.open(args.cover).convert("RGB")
    if len(tracks) >= 6:
        cover_size = 480
    else:
        cover_size = 700
    cover = cover.resize((cover_size, cover_size))
    cx = (W - cover_size) // 2
    cy = 170
    img.paste(cover, (cx, cy))

    # Tracks: two columns when >=6
    track_font = load_font(24)
    time_font = load_font(18)
    n = len(tracks)
    two_col = n >= 6
    if two_col:
        left = tracks[: (n + 1) // 2]
        right = tracks[(n + 1) // 2:]
        cols = [(80, left), (560, right)]
    else:
        cols = [(140, tracks)]

    start_y = cy + cover_size + 60
    for x0, group in cols:
        y = start_y
        for t in group:
            line = f"{t['n']}. {t['title']}"
            d.text((x0, y), line, font=track_font, fill=WHITE)
            dur = t.get("duration", "")
            if dur:
                d.text((x0 + 340, y + 6), dur, font=time_font, fill=GRAY)
            y += 80

    img.save(args.out, quality=92)
    print("OK:", args.out)


if __name__ == "__main__":
    main()
