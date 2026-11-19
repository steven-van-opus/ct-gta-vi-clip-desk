#!/usr/bin/env python3
"""Check a vertical clip before posting: size, duration, audio and loudness."""
import argparse, json, re, subprocess, sys


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def loudness(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("clip")
    p.add_argument("--min", type=float, default=7)
    p.add_argument("--max", type=float, default=60)
    a = p.parse_args()
    info = probe(a.clip)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    duration = float(info["format"]["duration"])
    rows = []
    rows.append(("size", f"{video['width']}x{video['height']}", video["width"] == 1080 and video["height"] == 1920))
    rows.append(("duration", f"{duration:.1f}s", a.min <= duration <= a.max))
    rows.append(("audio", "present" if audio else "missing", bool(audio)))
    lufs = loudness(a.clip) if audio else None
    rows.append(("loudness", f"{lufs} LUFS" if lufs is not None else "n/a", lufs is not None and -17 <= lufs <= -11))
    failed = False
    for name, value, ok in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<9} {value}")
        failed |= not ok
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
