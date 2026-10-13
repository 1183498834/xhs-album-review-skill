# xhs-album-review-skill

An Agent Skill for publishing a 3-image album review note to **Xiaohongshu (小红书 / Little Red Book)** — end-to-end, from artist + album name to a saved draft in the creator studio.

> English instructions live in 
>
> [SKILL.md](SKILL.md)
>
> . 中文说明见 
>
> [SKILL.zh-CN.md](SKILL.zh-CN.md)
>
> .

## What it does

Given an artist and album (e.g. `Karmanjakah - Diamond Morning`), the skill:



1. Resolves the album on Apple Music and pulls the **full tracklist** via the public iTunes Lookup API (no auth).

2. Downloads the official 1200×1200 cover art from Apple's `mzstatic` CDN.

3. Finds band facts, genre tags, and similar bands via web search.

4. Finds a band press photo via image search.

5. Generates a custom tracklist card (dark navy, two-column layout for ≥6 tracks, per-track durations).

6. Fills the Xiaohongshu publisher UI — title, body, 3 images — and saves to the **draft box**. The final red "发布" (Publish) button is left for the human.

## Why not NetEase Cloud Music?

NetEase's web search forces a login modal on every reload and has thin coverage of indie / international metal. Apple Music + the iTunes Lookup API gives a complete, machine-readable tracklist without any wall.

## Layout



```
xhs-album-review-skill/
├── SKILL.md                # English instructions (loaded by the agent)
├── SKILL.zh-CN.md          # Chinese mirror
├── README.md               # this file
└── scripts/
    ├── build_tracklist.py      # render the 1080x1440 tracklist card
    └── tracks.example.json     # example tracklist input
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
✍️ The review            → first-person listening notes, user's opinion preserved verbatim in meaning
#hashtags                → 5–8 tags
```

## Hard rules baked into the skill



* Never press the final red **Publish** button. Save to draft only.

* Never touch cookies, localStorage, session tokens, or passwords.

* If Xiaohongshu demands login, hand the browser to the user via QR scan — do not type credentials.

* Never rely on `bu.type()` for the title (React wipes it on blur) — use the native-input-setter + dispatchEvent pattern.

* Never rely on `innerText = ...` for the tiptap editor — use `document.execCommand('insertText', ...)`.

* The "上传图片" button is a `<div>`, not a file input. Always target the hidden `<input type=file>` directly.

* **Hashtags are not pasted as text.** Raw `#tag` in the body is just black characters and won't link to the topic page. Insert each tag by typing `#` in the editor and picking from the topic-suggestion dropdown (or via the "话题" toolbar button). The result must be a highlighted blue chip, not plain text.

## Requirements



* The agent runtime must support `browser-use-automation` / `computer_use_tool` with `plane="bu"`.

* Python 3.9+ with `Pillow` for the tracklist card.

* No API keys needed.

## License

MIT — do whatever, no warranty.