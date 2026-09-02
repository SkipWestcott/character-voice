# Installation

Character Voice runs locally and uses an existing Qwen3-TTS installation.

The repository does not install or redistribute Qwen3-TTS model weights.

## Requirements

* Linux
* Python 3
* Qwen3-TTS
* FFmpeg
* NVIDIA GPU with CUDA support recommended for practical TTS generation

The reference-analysis utilities use Python's standard library. Reference preparation uses FFmpeg.

## Clone

```bash
git clone https://github.com/SkipWestcott/character-voice.git
cd character-voice
```

## Configure

Create the local machine configuration:

```bash
./command/setup
```

This creates:

```text
config/local.env
```

Edit that file with paths appropriate to the machine.

Example:

```bash
QWEN_TTS_PYTHON=/path/to/qwen-tts-venv/bin/python
QWEN_TTS_MODEL=/path/to/Qwen3-TTS-12Hz-1.7B-Base
REFERENCE_AUDIO=/path/to/private/reference.wav
REFERENCE_TEXT="Transcript of the reference recording."
OUTPUT_DIR=/path/to/output
```

`config/local.env` is ignored by Git.

## Verify the Environment

Run:

```bash
./command/status
```

This checks the configured Python runtime, model path, reference, transcript, CUDA availability, GPU information, and Qwen installation.

Resolve any reported configuration errors before attempting generation.

## Prepare a Reference

Analyze the source before processing:

```bash
./command/reference analyze <SOURCE_AUDIO>
```

Build the standard reference candidates:

```bash
./command/reference build \
  --input <SOURCE_AUDIO> \
  --output <REFERENCE_DIR>
```

This produces:

```text
reference_direct.wav
reference_minimal.wav
reference_conservative.wav
```

The original source is not modified.

Select the candidate that performs best in the actual TTS task rather than automatically choosing the most processed version.

## Configure the Selected Reference

Once a candidate has been selected, set its path in:

```text
config/local.env
```

For example:

```bash
REFERENCE_AUDIO=/path/to/reference_direct.wav
```

For normal ICL voice cloning, also provide the transcript:

```bash
REFERENCE_TEXT="Transcript of the reference recording."
```

The transcript should correspond to the reference audio.

## Generate Speech

Run:

```bash
./command/run "This is a synthetic example."
```

Generated audio is written to the configured output location.

For speaker-embedding-only cloning:

```bash
./command/run \
  --x-vector-only \
  "This is a synthetic example."
```

This mode does not require reference transcript text.

## Reference Preparation Without Qwen

The reference utilities do not require the Qwen model.

For example:

```bash
./command/reference analyze <SOURCE_AUDIO>
```

and:

```bash
./command/reference build \
  --input <SOURCE_AUDIO> \
  --output <REFERENCE_DIR>
```

only require Python and FFmpeg.

## Private Data

Keep private material outside the repository.

Do not commit:

* source recordings
* reference candidates
* generated audio
* private transcripts
* character dialogue
* character information
* model weights
* local configuration
* credentials

The repository is intended to contain the reusable workflow, not the private voice project built with it.

## Troubleshooting

### Python executable not found

Check:

```bash
./command/status
```

Then verify that `QWEN_TTS_PYTHON` points to an existing Python executable.

### Model not found

Verify:

```bash
QWEN_TTS_MODEL=/path/to/Qwen3-TTS-12Hz-1.7B-Base
```

points to the locally installed model directory.

### Reference not found

Verify:

```bash
REFERENCE_AUDIO=/path/to/private/reference.wav
```

points to an existing file.

### Missing reference transcript

Normal ICL voice cloning requires:

```bash
REFERENCE_TEXT="..."
```

Alternatively use:

```bash
./command/run --x-vector-only "..."
```

### CUDA unavailable

Run:

```bash
./command/status
```

The status command reports whether CUDA is available.

CPU execution may not provide practical generation performance depending on the model and hardware.

## Installation Principle

The repository should be portable across machines.

Moving to another machine should primarily require changing:

```text
config/local.env
```

rather than modifying project source code.
