# Step 3 — Write the review

Use this fixed structure in the note body:

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
<see "Review writing rules" below>

---
(do NOT append "#hashtags" as plain text here — tags are inserted via the in-editor topic picker in Step 4, not pasted.)
```

Planned tags (5–8) are kept in a separate list for Step 4. Do not write them into the body string.

## Review writing rules

1. **If the user provided their own review notes:** use them as the seed. Preserve every core opinion, verdict, and specific observation verbatim in meaning. Then **expand** the notes into a full 2–3 paragraph review: flesh out the listening context, connect their points to specific tracks or sonic details, and add transitions so it reads like a continuous piece rather than bullet points. Do not reverse their verdict or insert opinions they did not state.

2. **If the user did not provide notes:** write 2–3 paragraphs in a first-person listening voice from scratch. Ground every claim in the album's actual tracks, production, and band facts gathered in Step 1. Avoid AI-review clichés ("锁进年度备选", "直接点收藏", "个人评分 X/10", "循环播放").

3. **De-AI pass.** After the review draft is written (whether expanded from user notes or written from scratch), read `modules/deai-rules.md` and apply every rule before inserting the text into the editor. Keep all facts, track names, and the user's original opinions intact. The output must read like a real person wrote it, not a chatbot.

4. **Save locally before uploading.** Before touching the browser in Step 4, write the final note body to a file on disk. This is a safety net: if the draft upload fails, crashes, or the user wants to re-do it, the text and images are already on disk.

   Create one folder per album run:

   ```
   <project-root>/<artist>-<album-slug>/
   ```

   Inside it, save:

   * `review.md` — the complete note body (all emoji sections + the review text, **without** the `#hashtags` strings).
   * The 3 images already downloaded in Steps 1 and 2 should also live in this same folder (see `01-collect-album-info.md` and `02-build-images.md` for where to put them).
   * `tracks.json` — the tracklist used for the card.

   Also append a section at the bottom of `review.md` (in a comment or separated by `---`) listing the planned 5–8 tags for Step 4, so they are not lost if the session restarts.

## Tone rules

* First person, specific listening observations, no listicle scaffolding.
* The user's opinions are non-negotiable. The de-AI pass changes wording and rhythm, never the verdict.
* No star ratings or "must-listen" framing unless the user wrote it.
* Always save `review.md` to disk before opening the browser. Do not rely on memory to carry the text into Step 4.
