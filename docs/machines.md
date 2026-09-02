# Machine Configuration

Character Voice is intended to run on different local machines without requiring source-code changes for machine-specific paths.

Machine-specific settings belong in:

```text
config/local.env
```

This file is ignored by Git.

## Configuration

The current runtime configuration includes:

```bash id="3w6jkg"
QWEN_TTS_PYTHON=/path/to/qwen-tts-venv/bin/python
QWEN_TTS_MODEL=/path/to/Qwen3-TTS-12Hz-1.7B-Base
REFERENCE_AUDIO=/path/to/private/reference.wav
REFERENCE_TEXT="Transcript of the reference recording."
OUTPUT_DIR=/path/to/output
```

These values identify the local Python environment, model, private reference, transcript, and generated-audio destination.

Do not place machine-specific absolute paths in source code.

## Python Environment

`QWEN_TTS_PYTHON` identifies the Python executable used to run Qwen3-TTS.

For example:

```bash id="rx2f4y"
QWEN_TTS_PYTHON=/home/user/venvs/qwen-tts/bin/python
```

The configured environment must contain the installed `qwen_tts` package and its runtime dependencies.

## Model

`QWEN_TTS_MODEL` points to the locally installed Qwen3-TTS model directory.

Model weights are not stored in this repository.

For example:

```bash id="8om8e5"
QWEN_TTS_MODEL=/models/Qwen3-TTS-12Hz-1.7B-Base
```

The path is machine-specific.

## Reference Audio

`REFERENCE_AUDIO` points to the private reference recording or selected reference candidate.

For example:

```bash id="4a8rzc"
REFERENCE_AUDIO=/private/voice-references/character_reference.wav
```

Keep the actual recording outside the public repository.

The reference can be an original recording or one of the candidates produced by the reference pipeline.

## Reference Transcript

Normal ICL voice cloning requires the transcript corresponding to the reference audio:

```bash id="o7w4n1"
REFERENCE_TEXT="Transcript of the reference recording."
```

The transcript should describe what is actually spoken in the reference.

Do not put private character dialogue into tracked configuration files.

## Output Directory

`OUTPUT_DIR` controls where generated speech is written when an explicit output path is not supplied.

For example:

```bash id="a8qkqk"
OUTPUT_DIR=/private/voice-output
```

Generated audio should normally remain outside the repository.

## Hardware

The project is designed with NVIDIA/CUDA acceleration as the primary practical execution path.

Hardware availability should be detected and reported rather than assumed.

Run:

```bash id="h4n9yt"
./command/status
```

The status command reports:

* Python availability
* model availability
* reference availability
* transcript availability
* PyTorch version
* CUDA availability
* detected GPU
* detected GPU memory
* Qwen package location

A specific GPU model should not be hard-coded into the project.

## CUDA

CUDA availability depends on the local PyTorch installation and NVIDIA driver environment.

The repository does not install or manage the host NVIDIA driver.

If CUDA is unavailable, `./command/status` should make that visible before generation is attempted.

## Portability Principle

A different machine should require configuration changes rather than source-code edits.

The intended separation is:

```text id="e4x9eq"
Repository
    ├── commands
    ├── audio processing
    ├── TTS integration
    └── documentation

Local machine
    ├── Python environment
    ├── model weights
    ├── private references
    └── generated audio
```

This keeps the repository reusable while allowing each local voice project to use its own hardware, models, references, and output locations.
