---
name: xhs-album-review

description: End-to-end workflow for publishing a music album review note to Rednote (小红书). Use when the user wants to (1) research an album/band via Apple Music/iTunes + web search, (2) assemble 3 images (official cover, band photo, auto-generated tracklist card), (3) write a structured review, and (4) save the note to the Rednote creator studio. By default the note ends up in the draft box; the final "发布" button is clicked only when the user explicitly says "直接发布不需要经过人工同意". Covers album metadata lookup, cover art download, tracklist image generation, and the browser-automation quirks of the Rednote publisher (React-controlled inputs, tiptap editor, draft-box save flow).

---

# XHS Album Review

Produce a 3-image album-review note and save it to the Rednote creator-studio draft box. The note ends in the draft box by default. The red "发布" button is clicked only when the user's command explicitly says "直接发布不需要经过人工同意" (or an equally unambiguous direct-publish instruction). When in doubt, save the draft and ask.

## Required inputs from the user

* Artist name + album title (e.g. `Karmanjakah - Diamond Morning`).
* Optionally: the user's own review notes. If provided, use them as the seed for expansion (see `modules/03-write-review.md`): preserve every core opinion verbatim in meaning, then flesh out into a full 2–3 paragraph review. Never reverse the verdict.

## Workflow

Each step lives in its own module file. Read the module for the step you are on, then execute it. Do not try to hold the whole pipeline in memory.

At the start of a run, create one working folder per album: `<project-root>/<artist>-<album-slug>/`. Every artifact (cover, band photo, tracklist card, review.md, tracks.json) lands in that folder. If the browser upload in Step 4 fails mid-way, everything is already on disk.

| Step | What happens | Read this module |
| --- | --- | --- |
| 1 | Resolve album on Apple Music, pull tracklist via iTunes Lookup API, download cover, gather band facts/genre/similar artists, find band photo. | `modules/01-collect-album-info.md` |
| 2 | Assemble the 3 images: official cover, band press photo, generated tracklist card. | `modules/02-build-images.md` |
| 3 | Write the review using the fixed template. If the user supplied notes, expand them. Then run the de-AI pass. **Save review.md to the working folder before touching the browser.** | `modules/03-write-review.md` + `modules/deai-rules.md` |
| 4 | Open the Rednote creator studio, upload the 3 images from the working folder, fill title and body, insert topic chips via the topic picker. Save to draft by default; publish directly only on the "直接发布不需要经过人工同意" command. | `modules/04-upload-draft.md` |
| 5 | Confirm the draft landed and report the working folder path, image paths, and save time to the user. | `modules/05-verify.md` |

## Hard safety rules and known pitfalls

Read `modules/safety-and-pitfalls.md` before touching the browser. It contains the red lines (no cookies, no credentials, no mass-publish) and the DOM-level gotchas that have already burned us once.

**The default end state is a saved draft, never a live post.** The red "发布" button may be clicked only when the user's command in this run explicitly contains the phrase "直接发布不需要经过人工同意" (or an equally unambiguous direct-publish instruction). Anything else, including "发了吧", "你看着办", "looks good", ends in the draft box. When in doubt, save the draft and ask.

## Module map on disk

```
xhs-album-review-skill/
├── SKILL.md                          # this file (router)
├── SKILL.zh-CN.md                    # Chinese mirror
├── README.md                          # English readme
├── README.zh-CN.md                   # Chinese readme
├── modules/
│   ├── 01-collect-album-info.md       # Step 1
│   ├── 02-build-images.md            # Step 2
│   ├── 03-write-review.md             # Step 3
│   ├── deai-rules.md                  # de-AI checklist referenced by Step 3
│   ├── 04-upload-draft.md             # Step 4
│   ├── 05-verify.md                   # Step 5
│   └── safety-and-pitfalls.md        # safety red lines + known pitfalls
└── scripts/
    ├── build_tracklist.py
    └── tracks.example.json
```
