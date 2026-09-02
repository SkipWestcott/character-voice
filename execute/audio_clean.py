#!/usr/bin/env python3
"""Deterministic WAV preparation for voice-reference candidates.

The original is never modified. Processing is intentionally restrained.
Stronger denoise, dereverb, declipping, EQ, or ML restoration should remain
separate experimental candidates.
"""

import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create a voice-reference candidate."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--preset",
        choices=["minimal", "conservative"],
        default="conservative",
    )
    parser.add_argument(
        "--highpass",
        type=float,
        default=None,
        help="Optional high-pass cutoff in Hz.",
    )
    parser.add_argument("--trim-start", type=float, default=0.0)
    parser.add_argument("--trim-duration", type=float, default=None)
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required for audio cleaning")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    filters = []

    if args.preset == "conservative":
        filters.append("highpass=f=20")

    if args.highpass is not None:
        filters.append(f"highpass=f={args.highpass:g}")

    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
    ]

    if args.trim_start:
        cmd += ["-ss", str(args.trim_start)]

    cmd += ["-i", str(args.input)]

    if args.trim_duration is not None:
        cmd += ["-t", str(args.trim_duration)]

    if filters:
        cmd += ["-af", ",".join(filters)]

    # Both presets produce deterministic PCM WAV output.
    cmd += ["-c:a", "pcm_s16le", str(args.output)]

    subprocess.run(cmd, check=True)
    print(args.output)


if __name__ == "__main__":
    main()