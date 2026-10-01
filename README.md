# Walktober

A step-challenge scoreboard for Ross, AJ, Adam and Kev. Each walker moves along a track that starts at 0% on the left and has room past 100% based on
this October's steps as a percent of their own October 2025 total. Rows re-sort by percent, and the
replay button plays the month back day by day.

## Files

- `index.html` is the whole page. It reads `data.json` and has no build step.
- `data.json` holds the people, their 2025 baselines, and `history`, a list of daily cumulative totals.
- `faces/` holds the head cutouts (transparent PNGs).
- `tools/add_snapshot.py` adds or corrects a day's totals.

## Characters

Each person in `data.json` has a `character`: `skeleton`, `mummy`, `witch` or `cat`. Swap them by editing that one word. Right now: Kev is the skeleton, Ross the mummy, AJ the witch and Adam the black cat. Each walks a graveyard lane, with pumpkin and tombstone markers at the next two % milestones. Last October's totals sit on the tombstones at the bottom.

## Updating by hand

```
python3 tools/add_snapshot.py ross=12345 aj=23456 adam=11111 kev=22222
python3 tools/add_snapshot.py --date 2026-10-05 kev=60000    # fix one person on a past day
git add data.json && git commit -m "Update steps" && git push
```

Totals are cumulative for the month. Re-running a date replaces that day.

## Preview

```
python3 -m http.server 8000     # then open http://localhost:8000
```

Add `?demo` to the URL to see made-up data, which is useful for checking the layout and the replay.

## Publishing

Turn on GitHub Pages (Settings → Pages → deploy from the `main` branch, root folder).

## Later: automatic updates

`data.json` already stores each person's Garmin user ID. Whatever does the fetching only needs to call
`add_snapshot.py` with the totals from Garmin's challenge endpoint, so the page itself will not change.
