#!/usr/bin/env python3
"""Small, dependency-light WAV inspection utility for voice references."""
import argparse, json, math, wave
from pathlib import Path
from array import array


def analyze(path: Path):
    with wave.open(str(path), 'rb') as w:
        channels = w.getnchannels(); rate = w.getframerate(); width = w.getsampwidth(); frames = w.getnframes()
        raw = w.readframes(frames)
    if width not in (1, 2, 3, 4):
        raise SystemExit(f"Unsupported PCM sample width: {width}")
    if width == 2:
        vals = array('h'); vals.frombytes(raw)
        if vals.itemsize != 2: vals.byteswap()
        samples = [v / 32768.0 for v in vals]
    else:
        # Fall back to peak-only parsing for uncommon widths.
        samples = []
        step = width
        for i in range(0, len(raw) - step + 1, step):
            b = raw[i:i+step]
            n = int.from_bytes(b, 'little', signed=False)
            n -= 1 << (width*8-1)
            samples.append(n / float(1 << (width*8-1)))
    if not samples:
        raise SystemExit("No audio samples found")
    peak = max(abs(x) for x in samples)
    rms = math.sqrt(sum(x*x for x in samples) / len(samples))
    silence_threshold = 10 ** (-50 / 20)
    silent_ratio = sum(abs(x) < silence_threshold for x in samples) / len(samples)
    clipped_ratio = sum(abs(x) >= 0.999 for x in samples) / len(samples)
    return {
        "path": str(path),
        "sample_rate": rate,
        "channels": channels,
        "duration_seconds": frames / rate if rate else 0,
        "sample_width_bytes": width,
        "peak_dbfs": round(20 * math.log10(max(peak, 1e-12)), 2),
        "rms_dbfs": round(20 * math.log10(max(rms, 1e-12)), 2),
        "crest_factor_db": round(20 * math.log10(max(peak, 1e-12) / max(rms, 1e-12)), 2),
        "silence_ratio_estimate": round(silent_ratio, 4),
        "clipped_ratio_estimate": round(clipped_ratio, 6),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("audio", type=Path)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    result = analyze(a.audio)
    if a.json: print(json.dumps(result, indent=2))
    else:
        for k, v in result.items(): print(f"{k}: {v}")

if __name__ == "__main__": main()
