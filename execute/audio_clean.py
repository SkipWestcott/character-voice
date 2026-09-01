#!/usr/bin/env python3
"""Conservative deterministic WAV cleaning using ffmpeg.

The original is never modified. Processing is intentionally restrained; use
separate candidates for any stronger denoise, dereverb, declip, EQ, or ML
restoration experiments.
"""
import argparse, shutil, subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Create a conservative voice-reference candidate.")
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--preset", choices=["minimal", "conservative"], default="conservative")
    p.add_argument("--highpass", type=float, default=None, help="Optional high-pass cutoff in Hz.")
    p.add_argument("--trim-start", type=float, default=0.0)
    p.add_argument("--trim-duration", type=float, default=None)
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required for audio cleaning")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    filters = []
    if a.preset == "conservative":
        # Very-low-frequency/DC cleanup only. This is intentionally not a
        # broadband denoiser or generative enhancer.
        filters.append("highpass=f=20")
    if a.highpass:
        filters.append(f"highpass=f={a.highpass:g}")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    if a.trim_start: cmd += ["-ss", str(a.trim_start)]
    cmd += ["-i", str(a.input)]
    if a.trim_duration is not None: cmd += ["-t", str(a.trim_duration)]
    if filters: cmd += ["-af", ",".join(filters)]
    cmd += ["-c:a", "pcm_s16le", str(a.output)]
    subprocess.run(cmd, check=True)
    print(a.output)

if __name__ == "__main__": main()
