#!/usr/bin/env python3
"""Record a day's step totals in data.json.

Usage:
  python3 tools/add_snapshot.py ross=12345 aj=23456 adam=11111 kev=22222
  python3 tools/add_snapshot.py --date 2026-10-05 ross=... aj=... adam=... kev=...

Totals are cumulative for the month (not per-day). Running it twice for the
same date replaces that day's entry, so you can correct a typo by re-running.
People you leave out keep their previous total.
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DATA = Path(__file__).resolve().parent.parent / "data.json"
TZ = ZoneInfo("America/New_York")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (default: today, Eastern time)")
    ap.add_argument("--file", default=str(DATA))
    ap.add_argument("totals", nargs="+", help="id=steps, for example ross=12345")
    a = ap.parse_args()

    path = Path(a.file)
    data = json.loads(path.read_text())
    ids = [p["id"] for p in data["people"]]
    now = datetime.now(TZ)
    date = a.date or now.date().isoformat()

    new = {}
    for item in a.totals:
        k, _, v = item.partition("=")
        k = k.strip().lower()
        if k not in ids:
            sys.exit(f"Unknown person '{k}'. Use one of: {', '.join(ids)}")
        try:
            new[k] = int(v.replace(",", ""))
        except ValueError:
            sys.exit(f"'{item}': steps must be a whole number")

    hist = data.setdefault("history", [])
    prior = [h for h in hist if h["date"] < date]
    base = dict(prior[-1]["steps"]) if prior else {i: 0 for i in ids}
    existing = next((h for h in hist if h["date"] == date), None)
    steps = dict(existing["steps"]) if existing else base
    for i in ids:
        steps.setdefault(i, 0)
    steps.update(new)

    for i in ids:
        if steps[i] < base.get(i, 0):
            print(f"warning: {i} is {steps[i]:,}, lower than the previous total {base[i]:,}", file=sys.stderr)

    if existing:
        existing["steps"] = steps
    else:
        hist.append({"date": date, "steps": steps})
        hist.sort(key=lambda h: h["date"])
    data["updated"] = now.isoformat(timespec="seconds")
    path.write_text(json.dumps(data, indent=2) + "\n")

    print(f"Recorded {date}:")
    for p in data["people"]:
        pct = steps[p["id"]] / p["baseline"] * 100
        print(f"  {p['name']:<5} {steps[p['id']]:>9,}  {pct:5.1f}%")


if __name__ == "__main__":
    main()
