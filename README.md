# xhs-album-review-skill

An Agent Skill for publishing a 3-image album review note to **Xiaohongshu (小红书 / Little Red Book)**, end-to-end: from artist + album name to a saved draft in the creator studio.

> English instructions live in [SKILL.md](SKILL.md). 中文说明见 [SKILL.zh-CN.md](SKILL.zh-CN.md).

## What it does

Given an artist and album (e.g. `Karmanjakah - Diamond Morning`), the skill:

1. Resolves the album on Apple Music and pulls the **full tracklist** via the public iTunes Lookup API (no auth).
2. Downloads the official 1200×1200 cover art from Apple's `mzstatic` CDN.
3. Finds band facts, genre tags, and similar bands via web search.
4. Finds a band press photo via image search.
5. Generates a custom tracklist card (dark navy, two-column layout for ≥6 tracks, per-track durations).
6. Writes the review: if the user supplied notes, expand them; if not, write first-person listening notes. Then run the draft through an inline de-AI checklist. **Saves the final note body as `review.md` and keeps all 3 images in a per-album folder on disk before touching the browser**, so a browser crash or failed upload never loses the work.
7. Fills the Xiaohongshu publisher UI (title, body, 3 images, topic chips) and saves to the **draft box**. The final red "发布" button is left for the human.

## Why not NetEase Cloud Music?

NetEase's web search forces a login modal on every reload and has thin coverage of indie / international metal. Apple Music + the iTunes Lookup API gives a complete, machine-readable tracklist without any wall.

## Layout

The skill is modular. Each step is its own file under `modules/`, so you can maintain one feature without touching the rest.

During a run, the agent creates a per-album working folder on disk:

```
<project-root>/<artist>-<album-slug>/
├── review.md          # final note body, saved before touching the browser
├── cover.jpg         # 1200x1200 official cover
├── band-photo.jpg    # band press photo
├── tracklist.jpg     # generated tracklist card
└── tracks.json        # full tracklist pulled from iTunes API
```

If the browser upload fails, these files are already on disk and the user can re-run or paste manually.

```
xhs-album-review-skill/
├── SKILL.md                          # entry: router, required inputs, step table
├── SKILL.zh-CN.md                    # Chinese mirror
├── README.md
├── modules/
│   ├── 01-collect-album-info.md     # Step 1: Apple Music, iTunes API, cover, band facts, photo
│   ├── 02-build-images.md            # Step 2: 3 images, tracklist card script
│   ├── 03-write-review.md            # Step 3: fixed template + review writing rules
│   ├── deai-rules.md                 # de-AI checklist (referenced by Step 3)
│   ├── 04-upload-draft.md            # Step 4: browser automation, DOM filling, topic picker
│   ├── 05-verify.md                  # Step 5: confirm draft, report to user
│   └── safety-and-pitfalls.md        # hard safety rules + known pitfalls
└── scripts/
    ├── build_tracklist.py             # render the 1080x1440 tracklist card
    └── tracks.example.json            # example tracklist input
```

## Quick start

```
pip install pillow

python scripts/build_tracklist.py \
    --cover Karmanjakah_Diamond_morning_cover.jpg \
    --tracks scripts/tracks.example.json \
    --out tracklist.jpg \
    --artist Karmanjakah \
    --album "Diamond Morning" \
    --year 2026
```

## The note body structure

Fixed format requested by the user:

```
🎸 About the band       → city, country, formed year, lineup, self-description
🎛️ Genre                → genre tags + any scene nickname (e.g. "happy thall")
🎧 If you like           → 3–5 similar bands
💿 The record            → release date, self-released/label, position in discography
✍️ The review            → expanded from user notes OR written from scratch, then de-AI checked
#hashtags                → 5–8 tags, all on ONE line, inserted via the topic picker
```

## Hard rules baked into the skill

* **Draft by default, publish only on explicit command.** The default end state is a saved draft in the creator studio. The red "发布" button may be clicked only when the user's command in that run explicitly contains the phrase "直接发布不需要经过人工同意" (or an equally unambiguous direct-publish instruction). Anything less is draft-only. When in doubt, save the draft and ask.
* Never touch cookies, localStorage, session tokens, or passwords.
* If Xiaohongshu demands login, hand the browser to the user via QR scan. Do not type credentials.
* Never mass-publish. One note per run.
* Never rely on `bu.type()` for the title (React wipes it on blur). Use the native-input-setter + dispatchEvent pattern.
* Never rely on `innerText = ...` for the tiptap editor. Use `document.execCommand('insertText', ...)`.
* The "上传图片" button is a `<div>`, not a file input. Always target the hidden `<input type=file>` directly.
* **Hashtags are not pasted as text.** Raw `#tag` in the body is just black characters. Insert each tag by typing `#` in the editor and picking from the topic-suggestion dropdown. All tags sit on one line, separated by single spaces, never one per line.

## Browser backend

The skill does **not** hard-code one browser. It picks the backend based on what the user asks for in that run:

| User says | Backend |
| --- | --- |
| (nothing — default) | Built-in Browser Use (`computer_use_tool`, `plane="bu"`) |
| "use my Chrome / my Edge / my logged-in browser" | User's own browser via `browser-skill` (bsk CLI + extension) |
| "use Edge" / "use Chrome" explicitly | Desktop automation (`computer_use_tool`, `plane="cu"`), launch that brand |

The DOM-level quirks (React title input, tiptap editor, hidden `<input type=file>`, topic-picker hashtags) are identical across all three backends. The skill never switches backends mid-flow.

## Requirements

* The agent runtime must support `computer_use_tool` (both `plane="bu"` for the built-in browser and `plane="cu"` for desktop automation). The `browser-skill` (bsk CLI) path is optional, only needed when the user wants to reuse their own logged-in browser profile.
* Python 3.9+ with `Pillow` for the tracklist card.
* No API keys needed.

## License

MIT.
