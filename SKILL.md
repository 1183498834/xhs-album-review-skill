***

name: xhs-album-review

description: End-to-end workflow for publishing a music album review note to Xiaohongshu (Little Red Book) as a draft. Use when the user wants to (1) research an album/band via Apple Music/iTunes + web search, (2) assemble 3 images (official cover, band photo, auto-generated tracklist card), (3) write a structured review, and (4) save the note to the Xiaohongshu creator studio draft box. Covers album metadata lookup, cover art download, tracklist image generation, and the browser-automation quirks of the Xiaohongshu publisher (React-controlled inputs, tiptap editor, draft-box save flow). Final "Publish" button is always left to the user.



***

# XHS Album Review

Produce a 3-image album-review note and save it to the Xiaohongshu creator-studio draft box. Never press the final "Publish" button — hand that back to the user.

## Required inputs from the user



* Artist name + album title (e.g. `Karmanjakah - Diamond Morning`).

* Optionally: the user's own review notes. If provided, preserve their core opinions verbatim in meaning; polish wording, never reverse the verdict.

## Step 1 — Collect album & band data

Do **not** rely on NetEase Cloud Music's web search for indie/international bands — coverage is sparse and the search wall forces a login modal. Use these sources:



1. **Resolve the album on Apple Music.** `general_search` for `<artist> <album> apple music` and open the Apple Music album URL. Extract the numeric `id` from the URL (`/album/.../<id>`).

2. **Pull full metadata + tracklist via the iTunes Lookup API** (no auth, CORS-friendly):



```
https://itunes.apple.com/lookup?id=<album_id>&country=us&entity=song
```

Sort tracks by `trackNumber`; keep `trackName`, `trackTimeMillis`. Note that deluxe/vinyl editions may include bonus tracks beyond the digital tracklist — trust the API, not the first snippet.



1. **Cover art.** The API returns `artworkUrl100` on the collection record. It points to `mzstatic.com`. Rewrite the size suffix:

* `/100x100bb.jpg` → `/1200x1200bb.jpg`

  Download with `Invoke-WebRequest` / `curl` to the working directory.

1. **Band facts, genre tags, similar artists.** `general_search` against Last.fm, Metal Storm, Prog Propaganda, the band's own site. Capture:

* City/country, formation year, current lineup (guitar / bass / drums / vocals), how they describe their own sound.

* Genre tags (e.g. `Progressive Metal / Djent / Melodic Thall`).

* FFO / similar bands (3–5 names).

1. **Band photo.** `image_search` for `<band> members band photo`. Prefer press shots that match the album cover's aesthetic. Save locally.

## Step 2 — Build the 3 images



| # | Image                | Source                                       |
| - | -------------------- | -------------------------------------------- |
| 1 | Official album cover | Apple Music CDN, 1200×1200                   |
| 2 | Band / press photo   | `image_search` result, downloaded            |
| 3 | Tracklist card       | Generated — see `scripts/build_tracklist.py` |

Run:



```
python scripts/build_tracklist.py --cover <cover.jpg> --tracks tracks.json --out tracklist.jpg
```

The script produces a 1080×1440 (3:4) card: dark navy background, centered cover thumbnail, two columns when ≥6 tracks, with per-track duration.

## Step 3 — Write the review

Use this fixed structure in the note body (the user's requested format):



```
🎸 About the band
<city, country, formed year, founding story, current lineup, how they describe their own sound>

🎛️ Genre
<genre tags, e.g. Progressive Metal / Djent / Melodic Thall. Include any scene nickname critics use, e.g. "happy thall".>

🎧 If you like
<3–5 similar bands>

💿 The record
<album title, release date, self-released or label, position in their discography, track count>

✍️ The review
<the user's own notes, polished but not rewritten. If the user didn't provide notes, write 2–3 paragraphs in a first-person listening voice — avoid AI-review clichés ("锁进年度备选", "直接点收藏", "个人评分 X/10").>

---
(do NOT append "#hashtags" as plain text here — tags are inserted via the in-editor topic picker in Step 4, not pasted.)
```

Planned tags (5–8) are kept in a separate list for Step 4. Do not write them into the body string.

Tone rules:



* First person, specific listening observations, no listicle scaffolding.

* Quote the user's opinion verbatim in meaning; smooth grammar only.

* No star ratings or "must-listen" framing unless the user wrote it.

## Step 4 — Upload to Xiaohongshu draft box

Use the `browser-use-automation` skill (`computer_use_tool` with `plane="bu"`). The publisher is a React app with a tiptap editor — naive `type()` calls get wiped on blur.



1. Switch to the existing Xiaohongshu tab (or open `https://creator.xiaohongshu.com/publish/publish`).

2. Click the **"上传图文"** tab (not the default "上传视频" tab).

3. **Do not click the red "上传图片" button to upload.** It is not a `<input type=file>`. Instead:



```
bu.upload_file("input[type=file]", r"E:\path\to\img1.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img2.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img3.jpg")
```

After the first upload the page switches to edit mode and the old input may unmount; re-query `input[type=file]` each time.



1. **Title.** The title `<input>` is React-controlled. A plain `bu.type()` loses its value on blur. Use:



```
const inp = document.querySelector('input[placeholder*=标题]');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(inp, 'THE TITLE');
inp.dispatchEvent(new Event('input', {bubbles:true}));
inp.dispatchEvent(new Event('change', {bubbles:true}));
```



1. **Body.** The editor is a tiptap `ProseMirror` div. Focus it and use `execCommand`. Pass the body **without** any `#tag` strings:



```
const ed = document.querySelector('.tiptap.ProseMirror');
ed.focus();
ed.innerHTML = '';
document.execCommand('insertText', false, 'THE BODY WITHOUT HASHTAGS');
```

1. **Insert hashtags via the topic picker, never as plain text.**

Pasting `#metal #djent` as literal characters into the body produces plain black text that does NOT link anywhere — Xiaohongshu only renders a clickable topic chip when the tag is created through the in-editor topic flow. To insert each tag:

   - Place the caret at the end of the body (or after a newline).
   - Type `#`. A topic-suggestion dropdown appears after ~400 ms.
   - Type the tag keyword, wait for the suggestion list to settle, then press `Enter` to pick the top match (or click the desired row).
   - A blue/highlighted topic chip is now inserted. Type a space and repeat for the next tag.
   - Alternative path: click the **"话题"** toolbar button below the editor (next to "用户" / "表情"), type the keyword in the popup, and pick the result.
   - **Verify**: after insertion the tag must look like a distinct highlighted span, not plain body text. If it renders as black text starting with `#`, it was inserted wrong and will not open the topic page when tapped.



1. **Replacing an existing image.** Hover the thumbnail; a `.close-btn.hoverShow` X appears on the corner. Click the one whose index matches the image you want to remove, then re-upload.

2. **Save as draft.** Click the **"暂存离开"** button (bottom-right, left of the red "发布" button). Do **not** click "发布". The UI shows a "保存成功" toast and the draft list confirms the new entry.

## Step 5 — Verify

After saving, confirm the draft list shows the new entry with the correct title and a fresh timestamp. Report the file paths of the 3 local images and the draft save time to the user.

## Hard safety rules



* Never read or exfiltrate cookies, localStorage, session tokens, or saved passwords.

* If the page demands login, call `interaction.request_action` with `type="browserControl"` and let the user scan the QR code themselves. Do not type credentials.

* The final red **"发布"** button is the user's. Stop at the draft box.

* Do not mass-publish. One draft per run; let the user review on their phone before publishing.

## Known pitfalls (hard-won)



* The "上传图片" button is a div, not a file input — `bu.upload(button_ref, path)` raises `Node is not a file input element`. Always target the hidden `<input type=file>` directly.

* Direct `bu.type()` into the title input gets wiped when focus leaves the field. Use the native setter + dispatchEvent dance above.

* The tiptap editor ignores programmatic `innerText = ...`. Must use `document.execCommand('insertText', ...)`.

* NetEase Cloud Music's web search forces a login modal on every reload and has thin coverage of non-Chinese/indie metal. Prefer Apple Music + general search for discography facts.

* Album tracklists from Apple Music snippets are often truncated. Always trust the iTunes Lookup API (`entity=song`), which returns the complete tracklist including bonus tracks.

* "暂存离开" is the draft-save button, not "leave without saving". Click it explicitly.