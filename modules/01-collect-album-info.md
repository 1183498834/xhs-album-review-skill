# Step 1 — Collect album & band data

Do **not** rely on NetEase Cloud Music's web search for indie/international bands. Coverage is sparse and the search wall forces a login modal. Use these sources instead.

## 1.1 Resolve the album on Apple Music

`general_search` for `<artist> <album> apple music` and open the Apple Music album URL. Extract the numeric `id` from the URL (`/album/.../<id>`).

## 1.2 Pull full metadata + tracklist via the iTunes Lookup API

No auth needed, CORS-friendly:

```
https://itunes.apple.com/lookup?id=<album_id>&country=us&entity=song
```

Sort tracks by `trackNumber`; keep `trackName`, `trackTimeMillis`. Deluxe/vinyl editions may include bonus tracks beyond the digital tracklist. Trust the API, not the first snippet.

Save the resulting track list as `tracks.json` for Step 2.

## 1.3 Download cover art

The API returns `artworkUrl100` on the collection record. It points to `mzstatic.com`. Rewrite the size suffix:

* `/100x100bb.jpg` → `/1200x1200bb.jpg`

Download to the per-album working folder you created at the start of this run (see Step 3, "Save locally"): `<project-root>/<artist>-<album-slug>/cover.jpg`.

## 1.4 Band facts, genre tags, similar artists

`general_search` against Last.fm, Metal Storm, Prog Propaganda, the band's own site. Capture:

* City/country, formation year, current lineup (guitar / bass / drums / vocals), how they describe their own sound.
* Genre tags (e.g. `Progressive Metal / Djent / Melodic Thall`).
* FFO / similar bands (3–5 names).
* Any scene nickname critics use (e.g. "happy thall").

## 1.5 Band photo

`image_search` for `<band> members band photo`. Prefer press shots that match the album cover's aesthetic. Save to the same per-album folder: `<artist>-<album-slug>/band-photo.jpg`.

## Output of this step

Before moving to Step 2 you should have on disk:

* `<album>_cover.jpg` (1200×1200 official cover)
* `<band>_photo.jpg` (band press photo)
* `tracks.json` (full track list with durations)
* Notes on band facts, genre, similar bands to feed into the review template in Step 3.
