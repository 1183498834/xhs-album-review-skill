# Step 5 — Verify

After Step 4, confirm what happened:

* If the note was saved to draft: the draft list shows the new entry with the correct title and a fresh timestamp.
* If the note was published directly (only on explicit user command): the creator studio shows a success toast and the note appears under "已发布".

Report back to the user:

* The working folder path (e.g. `E:\xhs\<artist>-<album-slug>\`).
* The files inside it: `review.md`, `cover.jpg`, `band-photo.jpg`, `tracklist.jpg`, `tracks.json`.
* Whether the note is currently in the draft box or was published directly.
* The save/publish time.
* If it is in draft: remind the user they can open it on their phone to review, edit, and press "发布" themselves.
* If Step 4 failed partway: tell the user the local files are already saved and they can re-run the upload or paste the text manually.
