#!/usr/bin/env python3
"""Build comparable voice-reference candidates without altering the source."""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZE = ROOT / "audio_analyze.py"
CLEAN = ROOT / "audio_clean.py"


def run(cmd): subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser(description="Build direct, minimal, and conservative reference candidates.")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--preset", choices=["minimal", "conservative"], default="conservative")
    a = p.parse_args()
    if not a.input.exists(): raise SystemExit(f"Input not found: {a.input}")
    a.output.mkdir(parents=True, exist_ok=True)
    direct = a.output / "reference_direct.wav"
    minimal = a.output / "reference_minimal.wav"
    conservative = a.output / "reference_conservative.wav"
    # Keep a direct copy so every comparison has an untouched baseline.
    import shutil; shutil.copy2(a.input, direct)
    shutil.copy2(a.input, minimal)
    run([sys.executable, str(CLEAN), str(a.input), str(conservative), "--preset", a.preset])
    report = {"input": str(a.input), "candidates": [str(direct), str(minimal), str(conservative)],
              "selection_note": "Evaluate speaker similarity, content consistency, and audio quality separately; do not assume the most processed candidate is best."}
    (a.output / "build.json").write_text(json.dumps(report, indent=2) + "\n")
    for f in (direct, minimal, conservative):
        r = subprocess.check_output([sys.executable, str(ANALYZE), str(f), "--json"], text=True)
        (a.output / (f.stem + ".json")).write_text(r)
    print(a.output)

if __name__ == "__main__": main()
