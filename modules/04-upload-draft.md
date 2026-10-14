# Step 4 — Upload to Xiaohongshu draft box

## Browser backend selection (read first)

Pick the browser backend by what the user asked for in this run:

| User said | Backend | How to invoke |
| --- | --- | --- |
| (nothing — default) | **Built-in Browser Use** (isolated browser, no user cookies) | `computer_use_tool` with `plane="bu"`, `import seed_browser_use as bu` |
| "use my Chrome / my Edge / my logged-in browser" | **User's own browser** via the `browser-skill` (bsk CLI + extension) | `bsk session start --json`, then `bsk navigate/observe/...` with `--session <id>` |
| "use Edge specifically" or "use Chrome specifically" (but no bsk extension attached) | **Desktop automation**, launch that exact browser | `computer_use_tool` with `plane="cu"`, `import seed_computer_use as cu`, then `cu.launch_app("Microsoft Edge")` / `cu.launch_app("Google Chrome")` |

Decision rules:

1. **Default = built-in `bu`.** It is isolated, scriptable, and does not touch the user's real browser profile. Use it unless the user explicitly names another browser.
2. **If the user mentions their logged-in browser** ("我 Chrome 已经登录了小红书", "用我 Edge 里的账号"), prefer the `browser-skill` bsk CLI path. It reuses the existing login session and avoids a fresh QR handoff. If `bsk` is not installed or the daemon is not connected, fall back to `plane="cu"` and ask the user to scan the QR once in that browser.
3. **If the user names a specific browser brand** without mentioning login state, use `plane="cu"` and launch that brand explicitly. Do not silently substitute the built-in browser.
4. **Never mix backends mid-flow.** Once you choose `bu`, `cu`, or `bsk`, stay on it for the whole Step 4. Switching backends loses tab focus and pending uploads.
5. The Xiaohongshu-specific quirks below (React title input, tiptap editor, hidden file input, topic picker) are DOM-level and apply to all three backends. Only the invocation syntax changes.

## Filling the publisher (DOM-level steps, same on all backends)

The publisher is a React app with a tiptap editor. Naive `type()` calls get wiped on blur.

1. Switch to the existing Xiaohongshu tab (or open `https://creator.xiaohongshu.com/publish/publish`).

2. Click the **"上传图文"** tab (not the default "上传视频" tab).

3. **Do not click the red "上传图片" button to upload.** It is not a `<input type=file>`. Instead:

```
bu.upload_file("input[type=file]", r"E:\path\to\img1.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img2.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img3.jpg")
```

After the first upload the page switches to edit mode and the old input may unmount; re-query `input[type=file]` each time.

4. **Title.** The title `<input>` is React-controlled. A plain `bu.type()` loses its value on blur. Use:

```
const inp = document.querySelector('input[placeholder*=标题]');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(inp, 'THE TITLE');
inp.dispatchEvent(new Event('input', {bubbles:true}));
inp.dispatchEvent(new Event('change', {bubbles:true}));
```

5. **Body.** The editor is a tiptap `ProseMirror` div. Focus it and use `execCommand`. Pass the body **without** any `#tag` strings:

```
const ed = document.querySelector('.tiptap.ProseMirror');
ed.focus();
ed.innerHTML = '';
document.execCommand('insertText', false, 'THE BODY WITHOUT HASHTAGS');
```

6. **Insert hashtags via the topic picker, never as plain text.**

Pasting `#metal #djent` as literal characters into the body produces plain black text that does NOT link anywhere. Xiaohongshu only renders a clickable topic chip when the tag is created through the in-editor topic flow. To insert each tag:

   - Place the caret at the very end of the body text (on the same line, not after a newline).
   - Type a single space, then type `#`. A topic-suggestion dropdown appears after ~400 ms.
   - Type the tag keyword, wait for the suggestion list to settle, then press `Enter` to pick the top match (or click the desired row).
   - A blue/highlighted topic chip is now inserted. **Do not press Enter or add a newline.** Type exactly one space and immediately start the next tag with `#`. All 5–8 tags must sit on one continuous line, separated only by single spaces, never one tag per line.
   - Alternative path: click the **"话题"** toolbar button below the editor (next to "用户" / "表情"), type the keyword in the popup, and pick the result. After each tag is inserted, type a space in the editor and continue with the next, no newlines.
   - **Verify**: after insertion the tag must look like a distinct highlighted span, not plain body text. If it renders as black text starting with `#`, it was inserted wrong and will not open the topic page when tapped. Also verify all tags are on the same line with no line breaks between them.

7. **Replacing an existing image.** Hover the thumbnail; a `.close-btn.hoverShow` X appears on the corner. Click the one whose index matches the image you want to remove, then re-upload.

8. **Final action: draft by default, publish only on explicit command.**

   This is a hard gate. Do not guess.

   - **Default (99% of runs): save as draft.** Click the **"暂存离开"** button (bottom-right, left of the red "发布" button). The UI shows a "保存成功" toast and the draft list confirms the new entry. Stop there. Report to the user that the note is in the draft box and they need to review and press "发布" themselves.
   - **Exception: direct publish.** Only when the user's command in this run explicitly contains the phrase **"直接发布不需要经过人工同意"** (or an equivalent unambiguous statement that they want it published immediately without review), you may click the red **"发布"** button. Before clicking, state out loud (in your reply) that you are about to publish directly because the user gave that explicit instruction, then click.
   - **Anything less explicit is draft-only.** Phrases like "发了吧", "你看着办", "应该可以发", "存草稿然后发" do NOT count as permission to publish. If you are unsure, save the draft and ask the user.

   There is no other path to publishing. Never click "发布" to "save a step", never click it because the draft already looks good, never click it because the user said "thanks" or "looks good".
