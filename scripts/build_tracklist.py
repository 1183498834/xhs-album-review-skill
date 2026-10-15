#!/usr/bin/env python3
"""Build a 1080x1440 tracklist card for Rednote notes.

Cards are theme-aware so that two albums never produce the same-looking card
(a fixed navy layout across an account's notes is a template fingerprint).

Usage:
    python build_tracklist.py \
        --cover cover.jpg \
        --tracks tracks.json \
        --out tracklist.jpg \
        --artist "Karmanjakah" \
        --album "Diamond Morning" \
        --year 2026 \
        [--theme auto|dark|light|warm]

--theme:
    auto  (default) sample the dominant color from the album cover,
          then darken or lighten it for readable text
    dark  deep navy (original fixed theme)
    light off-white card with dark text
    warm  warm charcoal (dark, slightly brown)

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
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

THEMES = {
    "dark":   ((18, 28, 48), (245, 245, 245), (150, 170, 190)),
    "light":  ((245, 243, 238), (30, 30, 30), (110, 110, 110)),
    "warm":   ((40, 30, 26), (245, 240, 235), (190, 165, 150)),
}

def _luma(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def sampled_theme(cover_path):
    """Dominant-ish color from the cover, tuned for text contrast."""
    img = Image.open(cover_path).convert("RGB")
    img = img.resize((48, 48))
    try:
        px = list(img.get_flattened_data())
    except AttributeError:  # Pillow < 11.1
        px = list(img.getdata())
    n = len(px)
    avg = tuple(sum(c[i] for c in px) // n for i in range(3))
    lum = _luma(avg)
    if lum > 150:
        # bright cover -> darken the sampled color for a card background
        bg = tuple(int(c * 0.45) for c in avg)
        fg = (245, 245, 245)
        sub_color = tuple(min(255, int(c * 1.25) + 40) for c in bg)
    else:
        bg = tuple(int(c * 1.15) for c in avg)
        bg = tuple(min(255, c) for c in bg)
        fg = (250, 250, 250)
        sub_color = tuple(min(255, int(c * 1.4) + 60) for c in bg)
    return bg, fg, sub_color


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
    ap.add_argument("--theme", default="auto",
                    choices=["auto", "dark", "light", "warm"])
    args = ap.parse_args()

    if args.theme == "auto":
        bg, fg, sub_color = sampled_theme(args.cover)
    else:
        bg, fg, sub_color = THEMES[args.theme]

    with open(args.tracks, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Accept both the documented {"tracks": [...]} format and the legacy
    # bare-list format ({track, name, duration}).
    if isinstance(data, dict) and "tracks" in data:
        raw_tracks = data["tracks"]
    else:
        raw_tracks = data

    def norm_track(t):
        if "title" in t and "n" in t:
            return {"n": t["n"], "title": t["title"],
                    "duration": t.get("duration", "")}
        return {"n": t.get("track", t.get("n", 0)),
                "title": t.get("name", t.get("title", "")),
                "duration": t.get("duration", "")}

    tracks = [norm_track(t) for t in raw_tracks]

    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    # Title
    title_font = load_font(44, bold=True)
    sub_font = load_font(24)
    d.text((60, 50), args.artist.upper(), font=title_font, fill=fg)
    sub_line = f"{args.album} · {args.year} · {len(tracks)} Tracks" if args.year \
        else f"{args.album} · {len(tracks)} Tracks"
    d.text((60, 110), sub_line, font=sub_font, fill=sub_color)

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
            d.text((x0, y), line, font=track_font, fill=fg)
            dur = t.get("duration", "")
            if dur:
                d.text((x0 + 340, y + 6), dur, font=time_font, fill=sub_color)
            y += 80

    img.save(args.out, quality=92)
    print("OK:", args.out)


if __name__ == "__main__":
    main()
