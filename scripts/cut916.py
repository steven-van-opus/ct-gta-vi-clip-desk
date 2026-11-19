#!/usr/bin/env python3
"""Cut a source video into a 1080x1920 clip. Standard library plus ffmpeg on PATH."""
import argparse, pathlib, shutil, subprocess, sys

W, H = 1080, 1920


def has_drawtext():
    out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    return " drawtext " in out


def escape(text):
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019").replace("%", "\\%")


def build_filter(layout, cam_crop, hook, font):
    if layout == "fill":
        chain = f"[0:v]scale=-2:{H},crop={W}:{H}[v]"
    elif layout == "blur":
        chain = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=20:2[bg];"
                 f"[b]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[v]")
    elif layout == "stack":
        if not cam_crop:
            sys.exit("--layout stack needs --cam-crop w:h:x:y (the webcam area in the source)")
        top = H // 3
        chain = (f"[0:v]split[a][b];[a]crop={cam_crop},scale={W}:{top}:force_original_aspect_ratio=increase,crop={W}:{top}[cam];"
                 f"[b]scale=-2:{H - top},crop={W}:{H - top}[game];[cam][game]vstack[v]")
    else:
        sys.exit(f"unknown layout {layout}")
    if hook and has_drawtext():
        fontopt = f":fontfile='{font}'" if font else ""
        chain = chain[:-3] + "[pre];" + (
            f"[pre]drawtext=text='{escape(hook)}'{fontopt}:fontsize=64:fontcolor=white:box=1:boxcolor=black@0.65:"
            f"boxborderw=24:x=(w-text_w)/2:y=h*0.12[v]")
    return chain


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source")
    p.add_argument("--start", required=True, help="hh:mm:ss or seconds")
    p.add_argument("--end", required=True)
    p.add_argument("--layout", default="blur", choices=["blur", "fill", "stack"])
    p.add_argument("--cam-crop", help="w:h:x:y of the webcam in the source, for --layout stack")
    p.add_argument("--hook", default="")
    p.add_argument("--font", default="")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is not installed")
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", a.start, "-to", a.end, "-i", a.source,
           "-filter_complex", build_filter(a.layout, a.cam_crop, a.hook, a.font), "-map", "[v]", "-map", "0:a?",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    if a.hook and not has_drawtext():
        out.with_suffix(".hook.txt").write_text(a.hook + "\n")
        print(f"ffmpeg has no drawtext; hook saved to {out.with_suffix('.hook.txt')}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
