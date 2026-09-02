#!/usr/bin/env python3
"""Build comparable voice-reference candidates without altering the source."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ANALYZE = ROOT / "audio_analyze.py"
CLEAN = ROOT / "audio_clean.py"


def run(cmd):
    subprocess.run(cmd, check=True)


def analyze(path):
    return subprocess.check_output(
        [sys.executable, str(ANALYZE), str(path), "--json"],
        text=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Build direct, minimal, and conservative reference candidates."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)

    direct = args.output / "reference_direct.wav"
    minimal = args.output / "reference_minimal.wav"
    conservative = args.output / "reference_conservative.wav"

    # Direct: convert to WAV without applying audio filters.
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(args.input),
            "-c:a",
            "pcm_s16le",
            str(direct),
        ]
    )

    # Minimal: deterministic WAV preparation only.
    run(
        [
            sys.executable,
            str(CLEAN),
            str(args.input),
            str(minimal),
            "--preset",
            "minimal",
        ]
    )

    # Conservative: restrained low-frequency cleanup.
    run(
        [
            sys.executable,
            str(CLEAN),
            str(args.input),
            str(conservative),
            "--preset",
            "conservative",
        ]
    )

    candidates = [direct, minimal, conservative]

    report = {
        "input": str(args.input),
        "candidates": [str(path) for path in candidates],
        "selection_note": (
            "Evaluate speaker similarity, content consistency, and audio "
            "quality separately; do not assume the most processed candidate "
            "is best."
        ),
    }

    (args.output / "build.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    for path in candidates:
        (args.output / f"{path.stem}.json").write_text(analyze(path))

    print(args.output)


if __name__ == "__main__":
    main()