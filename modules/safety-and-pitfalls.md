# Safety rules and known pitfalls

Read this before touching the browser in Step 4.

## Hard safety rules

* Never read or exfiltrate cookies, localStorage, session tokens, or saved passwords.
* If the page demands login, call `interaction.request_action` with `type="browserControl"` and let the user scan the QR code themselves. Do not type credentials.
* **Draft by default. Publish only on explicit command.** The default end state is a saved draft in the box. The red "发布" button may be clicked only when the user's command in this run explicitly contains the phrase "直接发布不需要经过人工同意" (or an equally unambiguous direct-publish instruction). Anything less is draft-only. When in doubt, save the draft and ask.
* Do not mass-publish. One note per run, draft or publish.

## Known pitfalls (hard-won)

* The "上传图片" button is a div, not a file input. `bu.upload(button_ref, path)` raises `Node is not a file input element`. Always target the hidden `<input type=file>` directly.
* Direct `bu.type()` into the title input gets wiped when focus leaves the field. Use the native setter + dispatchEvent dance in `04-upload-draft.md`.
* The tiptap editor ignores programmatic `innerText = ...`. Must use `document.execCommand('insertText', ...)`.
* NetEase Cloud Music's web search forces a login modal on every reload and has thin coverage of non-Chinese/indie metal. Prefer Apple Music + general search for discography facts.
* Album tracklists from Apple Music snippets are often truncated. Always trust the iTunes Lookup API (`entity=song`), which returns the complete tracklist including bonus tracks.
* "暂存离开" is the draft-save button, not "leave without saving". Click it explicitly.

## Platform risk rules (AI/template detection — read before any publish)

Rednote's detection is not only text-based: it also scores structure repetition (same skeleton across notes), image-template repetition (same card design), account behavior (publish frequency, mechanical interaction), and information density. Rules:

* **Publish cadence.** At most 1 note per day; prefer 1+ days between notes. Never queue several notes for the same session. Frequent same-slot publishing is an "AI 托管/批量运营" behavior signal and can freeze the account before content is even judged.
* **Honest labeling.** If the body was substantially written by AI, check the platform's "笔记含AI合成内容" declaration when publishing. Unlabeled AI content gets auto-tagged by the platform and may be throttled; honest labeling is the officially encouraged path and keeps the note out of the "AI 造假" category. The de-AI pass reduces the chance of a false positive, it does not license skipping the declaration.
* **No fake interaction.** Never self-comment, self-like, or use alt accounts to boost a note. The platform flags mechanical interaction (instant likes/saves, scripted comments) separately from content.
* **No fabricated detail.** All album facts must come from Step 1 research; do not invent listening details, quotes, or experiences to "look human". Fabrication = AI 造假 and is the fastest way to get a note removed.
* **False-positive appeal.** If a fully human note gets tagged "疑似AI生成", do NOT rewrite it to dodge detection; use the appeal channel (7-day window, attach original drafts/screenshots). Appeals are processed within ~3 working days.
* **Rotate everything that can repeat.** Skeleton variant (A/B/C), title style, card theme, section order, opener and closer — all must differ from the account's previous note. See `deai-rules.md` sections G/H.
