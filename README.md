# xhs-album-review-skill

> An Agent Skill that turns an artist + album name into a ready-to-publish 3-image album review note for **Rednote (小红书)**, and saves it to the creator studio draft box.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Agent%20Skill-lightgrey.svg)]()

[English](README.md) | [中文](README.zh-CN.md)

---

## What it does

Give the skill an artist and album (e.g. `Karmanjakah - Diamond Morning`). It:

1. **Resolves the album** on Apple Music and pulls the full tracklist via the public iTunes Lookup API (no auth, no login wall).
2. **Downloads cover art** at 1200×1200 from Apple's CDN.
3. **Gathers band facts** — city, lineup, genre tags, similar bands — via web search.
4. **Finds a band press photo** via image search.
5. **Generates a custom tracklist card** (dark navy, two-column for ≥6 tracks, per-track durations) with Pillow.
6. **Writes the review** — if you supplied your own notes, it expands them into a full 2–3 paragraph review while preserving your verdict; if not, it writes a first-person listening note from scratch. Then it runs the draft through a built-in de-AI checklist so it doesn't read like a chatbot.
7. **Saves everything locally** to a per-album folder (`review.md`, cover, band photo, tracklist card) *before* touching the browser, so a crash never loses the work.
8. **Fills the Rednote publisher UI** — title, body, 3 images, clickable topic chips — and saves to the draft box. The red **发布** button is yours to press.

## Why not NetEase Cloud Music?

NetEase's web search forces a login modal on every reload and has thin coverage of indie / international metal. Apple Music + the iTunes Lookup API gives a complete, machine-readable tracklist without any wall.

## Project layout

```
xhs-album-review-skill/
├── SKILL.md                          # entry: router, required inputs, step table
├── SKILL.zh-CN.md                    # Chinese mirror
├── README.md                          # this file
├── README.zh-CN.md                    # Chinese readme
├── modules/
│   ├── 01-collect-album-info.md       # Step 1: Apple Music, iTunes API, cover, band facts, photo
│   ├── 02-build-images.md            # Step 2: 3 images, tracklist card script
│   ├── 03-write-review.md             # Step 3: fixed template + review writing rules
│   ├── deai-rules.md                  # de-AI checklist (referenced by Step 3)
│   ├── 04-upload-draft.md            # Step 4: browser automation, DOM filling, topic picker
│   ├── 05-verify.md                   # Step 5: confirm draft, report to user
│   └── safety-and-pitfalls.md        # hard safety rules + known pitfalls
└── scripts/
    ├── build_tracklist.py             # render the 1080×1440 tracklist card
    └── tracks.example.json             # example tracklist input
```

Each step is its own module file, so you can maintain one feature (e.g. the topic-picker quirks) without touching the rest.

## Per-album output folder

Every run creates a folder on disk:

```
<project-root>/<artist>-<album-slug>/
├── review.md          # final note body, saved before touching the browser
├── cover.jpg          # 1200×1200 official cover
├── band-photo.jpg     # band press photo
├── tracklist.jpg      # generated tracklist card
└── tracks.json        # full tracklist from iTunes API
```

If the browser upload fails, these files are already on disk. You can re-run the upload or paste the text manually.

## Note body template

```
🎸 About the band       → city, country, formed year, lineup, self-description
🎛️ Genre                → genre tags + any scene nickname (e.g. "happy thall")
🎧 If you like           → 3–5 similar bands
💿 The record            → release date, self-released/label, position in discography
✍️ The review            → expanded from your notes OR written from scratch, then de-AI checked
#hashtags                → 5–8 tags, all on ONE line, inserted via the topic picker
```

## Quick start (tracklist card only)

```bash
pip install pillow

python scripts/build_tracklist.py \
    --cover Karmanjakah_Diamond_morning_cover.jpg \
    --tracks scripts/tracks.example.json \
    --out tracklist.jpg \
    --artist Karmanjakah \
    --album "Diamond Morning" \
    --year 2026
```

## Hard rules

- **Draft by default.** The note ends up in the creator-studio draft box. The red **发布** button may be clicked only when the user's command explicitly contains "直接发布不需要经过人工同意". Anything else — "发了吧", "你看着办", "looks good" — ends in the draft box. When in doubt, save the draft and ask.
- Never touch cookies, localStorage, session tokens, or passwords.
- If Rednote demands login, hand the browser to the user via QR scan. Never type credentials.
- Never mass-publish. One note per run.
- **Hashtags are not pasted as text.** Raw `#tag` in the body is just black characters. Each tag is inserted by typing `#` in the editor and picking from the topic-suggestion dropdown. All tags sit on one line, separated by single spaces, never one per line.

## Browser backend

The skill picks the backend based on what the user asks for in that run:

| User says | Backend |
| --- | --- |
| _(nothing — default)_ | Built-in Browser Use (`computer_use_tool`, `plane="bu"`) |
| "use my Chrome / my Edge / my logged-in browser" | User's own browser via `browser-skill` (bsk CLI + extension) |
| "use Edge" / "use Chrome" explicitly | Desktop automation (`computer_use_tool`, `plane="cu"`) |

The DOM-level quirks (React title input, tiptap editor, hidden `<input type=file>`, topic-picker hashtags) are identical across all three. The skill never switches backends mid-flow.

## Requirements

- The agent runtime must support `computer_use_tool` (both `plane="bu"` and `plane="cu"`). The `browser-skill` bsk CLI path is optional.
- Python 3.9+ with `Pillow` for the tracklist card.
- No API keys needed.

## License

MIT — do whatever, no warranty.
