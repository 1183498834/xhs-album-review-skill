# Step 3 — Write the review

The note body uses a **variable skeleton**, not a fixed template. Rednote treats repeated "same sections, same order, same closer" structures across an account's notes as 模板化/同质化 content (see `modules/deai-rules.md` section G). Every run must visibly differ from the account's previous notes.

## Skeleton options (pick ONE variant per run, rotate across runs)

Variant A — band-first:
```
🎸 About the band
<city, country, formed year, founding story, current lineup, how they describe their own sound>

🎛️ Genre
<genre tags, e.g. Progressive Metal / Djent / Melodic Thall. Include any scene nickname critics use, e.g. "happy thall".>

🎧 If you like
<3–5 similar bands — only if you actually found good matches; otherwise omit this section entirely>

💿 The record
<album title, release date, self-released or label, position in their discography, track count>

✍️ The review
<see "Review writing rules" below>
```

Variant B — record-first (open on the album/sound, band facts woven in later):
```
💿 开场先讲这张唱片（封面、总时长、整体气质、第一耳朵的印象）

✍️ 乐评主体（2–3 段，见 Review writing rules）

🎸 关于乐队（把背景放后面：来自哪里、阵容、他们怎么描述自己的声音）

🎛️ 风格（标签 + 圈子叫法）
```

Variant C — bare (no emoji sections at all, plain paragraphs with blank-line separation; the most human-looking option and the least template-like):
```
第一段直接进听感/场景，不介绍背景
第二段展开曲目细节
第三段乐队背景/风格信息，或对比前作
（可保留一行"如果你喜欢"的清单，或干脆省略）
```

Selection rules:

1. **Do not use the same variant in consecutive runs.** If the account already published a note using Variant A with the 🎸🎛️🎧💿✍️ order, the next note must use B or C.
2. **Emoji section headers are optional, not required.** Variant A's emojis are one styling choice, not a template obligation. When in doubt, prefer fewer decorations.
3. **Omit empty sections.** No FFO matches → no "If you like" section. No founding story found → start the band paragraph with lineup facts instead. Never pad a section to keep the skeleton intact.
4. **Opening and closer must differ from the previous note.** If the previous note opened with band background, open this one with a listening moment. If it closed on a concrete track, close this one on the overall impression or a question.

## Information-section writing rules (About the band / Genre / If you like / The record)

These four sections are where AI slop leaks in first: they read like a résumé or a press release — uniform short lines, parallel triads, name-dropping with no texture. Apply the anti-slop rules **at generation time**, not as an afterthought. Every rule in `deai-rules.md` section K applies here too.

**About the band — narrate, don't list.**

* Vary the opening every time: sometimes the founding story, sometimes the lineup quirk, sometimes the city and local scene. Never default to "成立于X年，来自Y地" as the fixed first sentence.
* Use the real specifics from Step 1: actual member names, actual years, actual records, what critics actually call them. Never invent anecdotes or scene nicknames the search didn't return.
* One paragraph, 3–5 sentences, visibly varied length — a punchy short sentence next to a long one. Not three equal-length lines.
* Avoid résumé verbs stacked three times ("担任…、负责…、主打…") and corporate filler ("致力于…、深耕…").

**Genre — the tag, then what it actually sounds like.**

* A bare tag row ("Progressive Metal / Djent / Ambient") is fine as a label, but the sentence after it must ground the tag in sound ("切分 riff 底下垫着一层亮堂的 ambience").
* If a scene nickname exists (e.g. "happy thall"), say who uses it; never coin one.
* No "一种融合了 A、B、C 的风格" triad construction.

**If you like — names with reasons, unevenly.**

* 3–5 names, each with a *why* that varies in length and angle: one by riff character, one by vocal mood, one by structure. Never five identically shaped lines.
* Only include bands Step 1 actually surfaced. Nothing fits → omit the whole section (deai-rules G3).

**The record — facts in a human order.**

* Release date, label/self-release, position in the discography, track count — but not as a bullet list. Weave the 1–2 facts that matter most into prose; imply the rest.
* No "《X》是乐队第Y张专辑，于Z年发行" formula every time. Vary the order and the wording.

**Universal no-go list for these sections**

* No parallel triads as filler; no uniform sentence lengths; no résumé/press-release tone.
* No invented facts, quotes, or scene nicknames — fabricated specificity is worse than honest vagueness (deai-rules J).
* No "值得一提的是 / 值得注意的是 / 毋庸置疑" bridges into any of these sections.

Do NOT append "#hashtags" as plain text here — tags are inserted via the in-editor topic picker in Step 4, not pasted.

Planned tags (5–8) are kept in a separate list for Step 4. Do not write them into the body string.

## Review writing rules

1. **If the user provided their own review notes:** use them as the seed. Preserve every core opinion, verdict, and specific observation verbatim in meaning. Then **expand** the notes into a full 2–3 paragraph review: flesh out the listening context, connect their points to specific tracks or sonic details, and add transitions so it reads like a continuous piece rather than bullet points. Do not reverse their verdict or insert opinions they did not state.

2. **If the user did not provide notes:** write 2–3 paragraphs in a first-person listening voice from scratch. Ground every claim in the album's actual tracks, production, and band facts gathered in Step 1. Avoid AI-review clichés ("锁进年度备选", "直接点收藏", "个人评分 X/10", "循环播放").

3. **Density check.** Every review must contain at least 3 concrete, only-a-listener-could-know details — timestamped moments, specific instrumental/production observations, track-to-track transitions, listening context (commute/late night/loud speakers), comparisons to previous work, version facts (durations, track count, mixing/mastering, label). Do not invent details you did not verify. See `deai-rules.md` section H.

4. **De-AI + human-touch pass.** After the review draft is written (whether expanded from user notes or written from scratch), read `modules/deai-rules.md` and apply every rule — including the Chinese pattern list (F), the structure-differentiation rules (G), the anti-slop structure/punctuation/openers rules (K), and the compliance red lines (J) — before inserting the text into the editor. The four information sections (About the band / Genre / If you like / The record) are covered by the "Information-section writing rules" above and section K at generation time. Keep all facts, track names, and the user's original opinions intact. The output must read like a real person wrote it, not a chatbot, and must not repeat the skeleton of the account's previous notes.

5. **Save locally before uploading.** Before touching the browser in Step 4, write the final note body to a file on disk. This is a safety net: if the draft upload fails, crashes, or the user wants to re-do it, the text and images are already on disk.

   Create one folder per album run:

   ```
   <project-root>/<artist>-<album-slug>/
   ```

   Inside it, save:

   * `review.md` — the complete note body (all emoji sections + the review text, **without** the `#hashtags` strings).
   * The 3 images already downloaded in Steps 1 and 2 should also live in this same folder (see `01-collect-album-info.md` and `02-build-images.md` for where to put them).
   * `tracks.json` — the tracklist used for the card.

   Also append a section at the bottom of `review.md` (in a comment or separated by `---`) listing the planned 5–8 tags for Step 4, and the skeleton variant used (A/B/C), so they are not lost if the session restarts and so the next run can avoid repeating the variant.

## Title rules

* 20 characters or fewer.
* No repeating the previous note's title pattern; rotate between factual ("《Album》乐评"), judgmental ("没有吉他的 djent，靠吹的"), and experiential ("通勤路上把这张听完了") styles.
* No clickbait filler ("震惊""必看""全网首发") — those trigger a different abuse signal.
* If the user supplied a title preference, follow it.

## Tone rules

* First person, specific listening observations, no listicle scaffolding.
* The user's opinions are non-negotiable. The de-AI pass changes wording and rhythm, never the verdict.
* No star ratings or "must-listen" framing unless the user wrote it.
* Always save `review.md` to disk before opening the browser. Do not rely on memory to carry the text into Step 4.
