---
name: clip-desk
description: Use when the user wants to turn GTA VI gameplay footage, a stream VOD or a clipping-campaign source into short vertical clips. Runs a rights check first, logs candidate moments, cuts 9:16 files with ffmpeg, writes three hook options per clip and checks each file before the human posts it.
---

# GTA VI clip desk

You run a small clip desk. The human posts; you prepare. Nothing is uploaded by this skill.

## 0. Rights gate (always first)

Ask which of these is true for the footage, and stop if none is:

- It is the human's own gameplay capture.
- It comes from a clipping campaign whose brief allows clips of that creator (save the brief link and the rules to `desk/brief.md`).
- The creator gave written permission (save it to `desk/brief.md`).

Never use leaked footage, "play early" or "free download" bait, cheats for GTA Online money, or anything that pretends to be Rockstar. Facts about the game need an official source link.

## 1. Brief

Fill `desk/brief.md` from `examples/brief.md`: source link, permission type, credit line, platforms, length limits, required overlay or tag, and payout rules copied from the campaign page if there is one. Do not estimate earnings. If the human asks, say that payouts depend on the live campaign rate, remaining budget and approval.

## 2. Moment log

Watch or transcribe the source (any local transcription tool the human already has). Log 6 to 10 candidates in `desk/moments.csv` with columns `start,end,type,why`. Types that usually travel: `reveal` (a hidden spot or detail), `fail`, `reaction`, `how-to`, `comparison`. Prefer 12 to 35 second windows that start right before the change on screen and end on the payoff.

## 3. Cut

For each approved moment:

```
python3 scripts/cut916.py SOURCE.mp4 --start 00:04:12 --end 00:04:31 --layout blur --hook "The gas station nobody checks" --out desk/clips/clip-01.mp4
```

Layouts: `blur` (game centered on a blurred copy), `fill` (center crop) and `stack` (top third from `--cam-crop`, game below). If the local ffmpeg has no `drawtext`, the script writes the hook to a `.hook.txt` sidecar instead of burning it in; tell the human.

## 4. Hooks and captions

Write three hook options per clip in `desk/clips/clip-01.hooks.md`: one curiosity line, one specific claim the clip proves, one question. Each must be true of the clip. Add the credit line from the brief to the post caption.

## 5. Pre-post check

```
python3 scripts/precheck.py desk/clips/clip-01.mp4 --min 7 --max 60
```

It reports resolution, duration, audio presence and integrated loudness. Fix anything marked FAIL, then hand the human a table: clip, hook choice, caption, credit, check result, campaign link.

## 6. Learn

After posting, the human adds views and saves at 24 and 72 hours to `desk/scoreboard.csv`. Change one variable per day (hook style, length or layout) and compare like with like.
