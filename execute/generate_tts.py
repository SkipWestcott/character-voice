#!/usr/bin/env python3
"""
Generic Qwen3-TTS voice-clone executor.

This file deliberately contains no character identity, private dialogue,
private reference filename, local path, hostname, IP, or model checkpoint.
"""

import argparse
import os
from pathlib import Path


def load_config():
    return {
        "model": os.environ.get("QWEN_TTS_MODEL", ""),
        "reference": os.environ.get("REFERENCE_AUDIO", ""),
        "reference_text": os.environ.get("REFERENCE_TEXT", ""),
        "x_vector_only": os.environ.get("X_VECTOR_ONLY_MODE", "false").lower()
            in {"1", "true", "yes", "on"},
        "output_dir": os.environ.get("OUTPUT_DIR", "output"),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate character voice audio with Qwen3-TTS.")
    parser.add_argument("text", nargs="?", help="Text to synthesize.")
    parser.add_argument("-o", "--output", help="Output WAV path.")
    parser.add_argument(
        "--reference-text",
        help="Transcript of the reference audio. Required for ICL voice cloning.",
    )
    parser.add_argument(
        "--x-vector-only",
        action="store_true",
        help="Use speaker embedding only; reference transcript is not required.",
    )
    args = parser.parse_args()

    cfg = load_config()

    if not args.text:
        parser.error("text is required")
    if not cfg["model"]:
        parser.error("QWEN_TTS_MODEL is not configured")
    if not cfg["reference"]:
        parser.error("REFERENCE_AUDIO is not configured")

    reference_text = args.reference_text or cfg["reference_text"]
    x_vector_only = args.x_vector_only or cfg["x_vector_only"]

    if not x_vector_only and not reference_text:
        parser.error(
            "Reference transcript is required for ICL voice cloning. "
            "Set REFERENCE_TEXT or use --reference-text. "
            "Alternatively use --x-vector-only."
        )

    try:
        from qwen_tts import Qwen3TTSModel
    except ImportError as exc:
        raise SystemExit(
            "qwen_tts is not installed in the configured Python environment."
        ) from exc

    output = Path(args.output or cfg["output_dir"]) 
    if output.suffix.lower() != ".wav":
        output.mkdir(parents=True, exist_ok=True)
        output = output / "generated.wav"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)

    print("Loading Qwen3-TTS model...")
    model = Qwen3TTSModel.from_pretrained(cfg["model"])

    # The exact generation signature can vary by qwen_tts release.
    # Keep release-specific parameters here rather than in shell wrappers.
    prompt = model.create_voice_clone_prompt(
        ref_audio=cfg["reference"],
        ref_text=reference_text,
        x_vector_only_mode=x_vector_only,
    )

    wavs, sr = model.generate_voice_clone(
        text=args.text,
        voice_clone_prompt=prompt,
    )

    import soundfile as sf
    sf.write(output, wavs[0], sr)
    print(f"Wrote: {output}")


if __name__ == "__main__":
    main()
