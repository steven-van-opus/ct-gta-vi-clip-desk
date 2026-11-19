# GTA VI Clip Desk (Creators Toolbox version)

A small Claude Code plugin for turning **authorized** GTA VI footage into reviewed 9:16 clips. It runs a rights check first, keeps a moment log, cuts vertical files with ffmpeg, writes three hook options per clip and checks each file before you post it yourself.

Unofficial fan tooling. Not affiliated with Rockstar Games, Take-Two or Anthropic. It does not promise views or income: clipping campaigns pay only on their own live rates, budgets and approval rules.

Guide page: https://creatorstoolbox.com/products/ct-gta-vi-clip-desk

## Install

In Claude Code:

```
/plugin marketplace add steven-van-opus/ct-gta-vi-clip-desk
/plugin install ct-gta-vi-clip-desk@ct-gta-vi-clip-desk
```

You also need `ffmpeg` and `ffprobe` on your PATH. Python 3.9+ with no extra packages.

## First prompt

```
Use clip-desk. My footage is my own capture at ~/Videos/gta6-night1.mp4.
Fill the brief, log 6 moments, cut the best 3 as blur layout with hooks, and run precheck on each.
```

## What is inside

| Path | What it does |
| --- | --- |
| `skills/clip-desk/SKILL.md` | The desk routine: rights gate, brief, moment log, cut, hooks, pre-post check, scoreboard |
| `scripts/cut916.py` | 1080x1920 cut in `blur`, `fill` or `stack` (webcam on top) layout, loudness normalized to about -14 LUFS, optional burned-in hook |
| `scripts/precheck.py` | PASS or FAIL for size, duration, audio and integrated loudness |
| `examples/` | A fictional brief, moment log and hook sheet |

## Run the scripts yourself

```
python3 scripts/cut916.py night1.mp4 --start 00:12:40 --end 00:13:02 --layout blur --hook "There's a pool behind this motel sign" --out desk/clips/clip-01.mp4
python3 scripts/precheck.py desk/clips/clip-01.mp4 --min 10 --max 45
```

If your ffmpeg build lacks `drawtext`, the hook is saved next to the clip as `.hook.txt` so you can add it in your editor.

## Rules the desk keeps

- Only your own capture, a campaign brief that allows the clip, or written permission.
- Credit the creator in every post. Keep required overlays.
- No leaks, piracy bait, GTA Online money or cheat claims, or posing as Rockstar.
- You approve and post every clip. Nothing is uploaded automatically.

## Credit

Inspired by [gtavi-claudecode by Bodila51](https://github.com/Bodila51/gtavi-claudecode) (MIT). This repository is an independent Creators Toolbox version with its own workflow, scripts and examples. For campaign-based clipping with OpusClip, see [How to get paid clipping GTA VI with OpusClip](https://creatorstoolbox.com/blog/clipping-gta-vi-with-opusclip) on Creators Toolbox.

MIT license.
