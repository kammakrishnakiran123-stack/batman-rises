#!/usr/bin/env python3
"""Search and cut SRT transcripts (standard library only). Pair with whisper's .srt output.

Usage:
  transcript_tools.py search TRANSCRIPT.srt "query words"
  transcript_tools.py window TRANSCRIPT.srt START END OUT.srt [--pad 0.3]

START/END accept HH:MM:SS, HH:MM:SS.mmm, or plain seconds.
'window' keeps cues that overlap the padded window, shifts them so the clip starts at 0,
and writes an SRT for the clip. Pair it with ffmpeg (see SKILL.md) to render captions.
"""
import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

TIME = r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})"
CUE = re.compile(rf"{TIME} --> {TIME}")


@dataclass
class Cue:
    index: int
    start: float
    end: float
    text: str


def to_seconds(stamp: str) -> float:
    if re.fullmatch(r"\d+(\.\d+)?", stamp):
        return float(stamp)
    parts = stamp.replace(",", ".").split(":")
    if len(parts) != 3:
        raise ValueError(f"Bad timestamp: {stamp}")
    h, m, s = parts
    return int(h) * 3600 + int(m) * 60 + float(s)


def fmt(seconds: float) -> str:
    seconds = max(0.0, seconds)
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(path: Path):
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace").strip())
    cues = []
    for block in blocks:
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = CUE.search(line)
            if m:
                g = [int(x) for x in m.groups()]
                start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                text = " ".join(lines[i + 1:]).strip()
                cues.append(Cue(len(cues) + 1, start, end, text))
                break
    if not cues:
        sys.exit(f"No cues parsed from {path}. Is it an SRT file?")
    return cues


def search(cues, query: str):
    words = [w.lower() for w in query.split() if w]
    hits = [c for c in cues if all(w in c.text.lower() for w in words)]
    for c in hits:
        print(f"[{fmt(c.start)} -> {fmt(c.end)}] {c.text}")
    print(f"{len(hits)} match(es)")
    return hits


def window(cues, start: float, end: float, pad: float, out: Path):
    lo, hi = max(0.0, start - pad), end + pad
    picked = [c for c in cues if c.end > lo and c.start < hi]
    lines = []
    for n, c in enumerate(picked, 1):
        s = max(c.start, lo) - lo
        e = min(c.end, hi) - lo
        lines += [str(n), f"{fmt(s)} --> {fmt(e)}", c.text, ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} with {len(picked)} cue(s); clip runs {fmt(0)} to {fmt(hi - lo)}")
    print(f"Clip window in the source: {fmt(lo)} -> {fmt(hi)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("srt", type=Path)
    s.add_argument("query")
    w = sub.add_parser("window")
    w.add_argument("srt", type=Path)
    w.add_argument("start")
    w.add_argument("end")
    w.add_argument("out", type=Path)
    w.add_argument("--pad", type=float, default=0.3)
    args = ap.parse_args()

    cues = parse_srt(args.srt)
    if args.cmd == "search":
        search(cues, args.query)
    else:
        window(cues, to_seconds(args.start), to_seconds(args.end), args.pad, args.out)


if __name__ == "__main__":
    main()
