#!/usr/bin/env python3

"""
Generic Qwen3-TTS VoiceDesign executor.

This file deliberately contains no character identity, private dialogue,
private reference filename, local path, hostname, IP, or model checkpoint.
"""

import argparse
import os
from pathlib import Path


def load_config():
    return {
        "model": os.environ.get("QWEN_TTS_DESIGN_MODEL", ""),
        "output_dir": os.environ.get("OUTPUT_DIR", "output"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate character voice audio with Qwen3-TTS VoiceDesign."
    )
    parser.add_argument(
        "--instruct",
        required=True,
        help="Natural-language description of the desired voice.",
    )
    parser.add_argument(
        "--text",
        required=True,
        help="Text to synthesize.",
    )
    parser.add_argument(
        "--language",
        help="Optional language for synthesis.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output WAV path.",
    )
    args = parser.parse_args()

    cfg = load_config()

    if not cfg["model"]:
        parser.error("QWEN_TTS_DESIGN_MODEL is not configured")

    try:
        from qwen_tts import Qwen3TTSModel
    except ImportError as exc:
        raise SystemExit(
            "qwen_tts is not installed in the configured Python environment."
        ) from exc

    output = Path(args.output or cfg["output_dir"])

    if output.suffix.lower() != ".wav":
        output.mkdir(parents=True, exist_ok=True)
        output = output / "generated_design.wav"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)

    print("Loading Qwen3-TTS VoiceDesign model...")

    model = Qwen3TTSModel.from_pretrained(cfg["model"])

    kwargs = {
        "text": args.text,
        "instruct": args.instruct,
        "non_streaming_mode": True,
    }

    if args.language:
        kwargs["language"] = args.language

    wavs, sr = model.generate_voice_design(**kwargs)

    import soundfile as sf

    sf.write(output, wavs[0], sr)
    print(f"Wrote: {output}")


if __name__ == "__main__":
    main()
