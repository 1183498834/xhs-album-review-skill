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
