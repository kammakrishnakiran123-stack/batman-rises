#!/usr/bin/env python3
"""Summarize an Apple Health export.xml into daily CSVs, streaming so large files fit in memory.

Usage:
  health_summary.py export.xml OUT_DIR [--since YYYY-MM-DD]

Outputs (all local):
  OUT_DIR/daily.csv     date, steps, steps_7d_avg, active_kcal, resting_hr, sleep_hours
  OUT_DIR/summary.md    plain-language summary of the period

De-duplication: each metric uses one source (the one with the most records for that metric).
Summing every source would double-count steps from an iPhone and an Apple Watch.
This is an informational summary, not medical advice.
"""
import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import mean

METRICS = {
    "HKQuantityTypeIdentifierStepCount": "steps",
    "HKQuantityTypeIdentifierActiveEnergyBurned": "active_kcal",
    "HKQuantityTypeIdentifierRestingHeartRate": "resting_hr",
    "HKCategoryTypeIdentifierSleepAnalysis": "sleep",
}


def parse_day(stamp: str) -> date:
    return date.fromisoformat(stamp[:10])  # "2024-01-01 08:00:00 -0500" -> local calendar day


def read_records(xml_path: Path, since):
    """Yield (metric, source, day, value, extra) for the metrics we track."""
    for _, elem in ET.iterparse(xml_path, events=("end",)):
        if elem.tag == "Record":
            rtype = elem.get("type")
            if rtype in METRICS:
                day = parse_day(elem.get("startDate", ""))
                if since is None or day >= since:
                    source = elem.get("sourceName", "unknown")
                    if rtype == "HKCategoryTypeIdentifierSleepAnalysis":
                        value = elem.get("value", "")
                        if "Asleep" in value:
                            start = elem.get("startDate", "")
                            end = elem.get("endDate", "")
                            hours = (_to_dt(end) - _to_dt(start)).total_seconds() / 3600
                            yield METRICS[rtype], source, day, hours
                    else:
                        try:
                            yield METRICS[rtype], source, day, float(elem.get("value", "0"))
                        except ValueError:
                            pass
            elem.clear()
        elif elem.tag in ("Workout", "ActivitySummary", "Correlation"):
            elem.clear()


def _to_dt(stamp: str):
    from datetime import datetime
    return datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S %z")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xml", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--since", type=date.fromisoformat, default=None)
    args = ap.parse_args()
    if not args.xml.is_file():
        sys.exit(f"Not found: {args.xml}")

    # Pass 1: find the dominant source per metric (streaming, keeps only counts).
    # Pass 2 would re-read the file, so collect everything once and filter in memory per metric.
    raw = defaultdict(list)            # metric -> list of (source, day, value)
    source_counts = defaultdict(Counter)
    for metric, source, day, value in read_records(args.xml, args.since):
        raw[metric].append((source, day, value))
        source_counts[metric][source] += 1
    if not raw:
        sys.exit("No matching records found. Check the file and the --since date.")

    dominant = {m: c.most_common(1)[0][0] for m, c in source_counts.items()}
    daily = defaultdict(dict)          # day -> metric -> value
    for metric, rows in raw.items():
        keep = [(d, v) for s, d, v in rows if s == dominant[metric]]
        if metric == "steps" or metric == "active_kcal" or metric == "sleep":
            totals = defaultdict(float)
            for d, v in keep:
                totals[d] += v
            for d, v in totals.items():
                daily[d][metric] = int(round(v)) if metric in ("steps", "active_kcal") else round(v, 2)
        else:  # resting heart rate: average of the day's readings
            buckets = defaultdict(list)
            for d, v in keep:
                buckets[d].append(v)
            for d, vs in buckets.items():
                daily[d][metric] = round(mean(vs), 1)

    days = sorted(daily)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    step_series = {d: daily[d].get("steps") for d in days}
    with (args.out_dir / "daily.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "steps", "steps_7d_avg", "active_kcal", "resting_hr", "sleep_hours"])
        for i, d in enumerate(days):
            window = [step_series[x] for x in days[max(0, i - 6): i + 1] if step_series[x] is not None]
            avg = round(mean(window), 0) if window and step_series[d] is not None else ""
            w.writerow([d.isoformat(), daily[d].get("steps", ""), avg,
                        daily[d].get("active_kcal", ""), daily[d].get("resting_hr", ""),
                        daily[d].get("sleep", "")])

    steps = [v for v in step_series.values() if v is not None]
    sleep = [daily[d]["sleep"] for d in days if "sleep" in daily[d]]
    rhr = [daily[d]["resting_hr"] for d in days if "resting_hr" in daily[d]]
    lines = [f"# Health summary ({days[0]} to {days[-1]}, {len(days)} days with data)", "",
             "Informational only, not medical advice. Discuss concerns with a clinician.", ""]
    if steps:
        lines.append(f"- Average steps per day: {mean(steps):,.0f}")
    if sleep:
        lines.append(f"- Average sleep: {mean(sleep):.1f} h (on {len(sleep)} nights)")
    if rhr:
        lines.append(f"- Average resting heart rate: {mean(rhr):.0f} bpm")
    lines.append("")
    lines.append("Sources used: " + ", ".join(f"{m}={s}" for m, s in sorted(dominant.items())))
    (args.out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.out_dir}/daily.csv and summary.md ({len(days)} days)")


if __name__ == "__main__":
    main()
