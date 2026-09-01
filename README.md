# Character Voice

**Create reusable local AI character voices from short audio references, prepare reference candidates, and generate speech with Qwen3-TTS.**

Character Voice is a local workflow for experimenting with voice references and cloned speech. It separates reference preparation, voice generation, and evaluation so that different recordings and processing choices can be compared without modifying the original audio.

The project is designed to be generic. Private character recordings, generated audio, dialogue, and model data should remain outside the repository.

## Workflow

```text
Audio Sample
     ↓
Reference Preparation
     ↓
Reference Candidates
     ↓
Voice Clone
     ↓
Generated Takes
     ↓
Evaluation
```

The important principle is that **reference quality and generated delivery are separate problems**. A technically cleaner recording is not automatically a better voice reference.

## Current Capabilities

### Reference preparation

Build comparable reference candidates from an existing recording:

```bash
./command/reference build \
  --input <SOURCE_AUDIO> \
  --output <REFERENCE_DIR>
```

The builder currently produces:

```text
reference_direct.wav
reference_minimal.wav
reference_conservative.wav
```

#### Direct

The source is converted to the project's canonical WAV representation without applying audio filters.

The source recording itself is never modified.

#### Minimal

The source is converted to deterministic PCM WAV output without intentional audio filtering.

For a source that is already compatible with the target WAV format, this may be effectively identical to Direct.

#### Conservative

The source is converted to PCM WAV and receives restrained low-frequency cleanup.

The current conservative filter is a 20 Hz high-pass. It is intentionally mild rather than a general-purpose restoration chain.

### Audio analysis

Inspect a WAV reference:

```bash
./command/reference analyze <AUDIO_FILE>
```

Machine-readable output:

```bash
./command/reference analyze <AUDIO_FILE> --json
```

The analyzer reports:

* sample rate
* channel count
* duration
* sample width
* peak level
* RMS level
* crest factor
* estimated low-level/silent sample ratio
* estimated clipping ratio

These measurements are diagnostic. They do not determine which reference sounds best.

### Reference cleaning

Individual candidates can also be created directly:

```bash
./command/reference clean \
  <INPUT_AUDIO> \
  <OUTPUT_WAV> \
  --preset conservative
```

Available presets:

```text
minimal
conservative
```

Optional operations include:

* high-pass filtering
* trimming from the beginning
* limiting output duration

These operations are explicit rather than automatically applied.

### Voice cloning

Once a reference has been selected, configure it locally in:

```text
config/local.env
```

Then generate speech:

```bash
./command/run "Synthetic example dialogue."
```

The configured reference audio and reference transcript are used by Qwen3-TTS for voice cloning.

The Qwen3-TTS Base voice-cloning API requires reference text for normal ICL voice cloning. Speaker-embedding-only operation is also available through:

```bash
./command/run --x-vector-only "Synthetic example dialogue."
```

### Runtime status

Check the local environment:

```bash
./command/status
```

This reports the configured Python runtime, model, reference, transcript, CUDA availability, GPU information, and Qwen installation.

## Installation

### Requirements

The project currently targets:

* Linux
* Python 3
* Qwen3-TTS
* FFmpeg
* NVIDIA/CUDA acceleration recommended for practical generation

The Qwen3-TTS model weights are **not distributed with this repository**.

Clone the repository:

```bash
git clone https://github.com/SkipWestcott/character-voice.git
cd character-voice
```

Create the local configuration:

```bash
./command/setup
```

Edit:

```text
config/local.env
```

Set the paths appropriate for your machine:

```bash
QWEN_TTS_PYTHON=/path/to/qwen-tts-venv/bin/python
QWEN_TTS_MODEL=/path/to/Qwen3-TTS-12Hz-1.7B-Base
REFERENCE_AUDIO=/path/to/private/reference.wav
REFERENCE_TEXT="Transcript of the reference recording."
OUTPUT_DIR=/path/to/output
```

Then check the environment:

```bash
./command/status
```

## Reference Selection

Do not assume that the most processed recording is the best reference.

A useful evaluation compares candidates on separate dimensions:

1. **Speaker similarity** — does the generated voice resemble the intended speaker?
2. **Content consistency** — is the requested text rendered clearly and faithfully?
3. **Audio quality** — are there unwanted artifacts, noise, pumping, or bandwidth problems?
4. **Delivery** — does the generated performance have the desired character and prosody?

Generate comparable takes when testing references. Keep the reference and generation settings associated with each experiment.

A good technical measurement does not necessarily predict the best TTS result.

## Experimental Method

When tuning a voice:

* Keep the original recording unchanged.
* Analyze the source before deciding to process it.
* Change one meaningful variable at a time.
* Keep alternate reference candidates separate.
* Compare the same test text across candidates.
* Use multiple takes when generation is stochastic.
* Evaluate speaker identity separately from delivery quality.
* Do not assume longer, louder, cleaner, or more processed is better.
* Keep project-specific character decisions outside the generic tooling.

Reference level experiments should also remain separate candidates rather than being baked into the generic pipeline.

## Current Presets

The available reference presets are intentionally limited:

| Preset         | Behavior                                            |
| -------------- | --------------------------------------------------- |
| `direct`       | Canonical WAV conversion with no filtering          |
| `minimal`      | Deterministic PCM WAV preparation                   |
| `conservative` | Minimal preparation plus restrained 20 Hz high-pass |

The project does **not currently implement** a general-purpose denoising, dereverberation, declipping, de-essing, EQ, or generative restoration pipeline.

Those techniques may be added later as separate experimental processing stages. They should not silently become part of the default reference workflow.

## Configuration

Machine-specific configuration belongs in:

```text
config/local.env
```

This file is ignored by Git.

The repository should not require source-code changes when moved to another machine. Paths to Python, models, references, and output directories are local configuration.

## Privacy

This repository contains the reusable mechanism, not a private character project.

Do not commit:

* source recordings
* generated private audio
* private dialogue
* character lore
* private prompts
* private reference transcripts
* model weights
* credentials or tokens
* local environment files
* caches
* runtime logs

Keep private audio and generated results in directories outside the repository.

## Project Structure

```text
character-voice/
├── command/
│   ├── reference
│   ├── run
│   ├── setup
│   └── status
├── config/
│   ├── defaults.env
│   └── machine.example.env
├── execute/
│   ├── audio_analyze.py
│   ├── audio_clean.py
│   ├── generate_tts.py
│   └── reference_builder.py
├── docs/
│   ├── architecture.md
│   ├── evaluation.md
│   ├── installation.md
│   ├── machines.md
│   ├── privacy.md
│   ├── reference-pipeline.md
│   ├── restoration.md
│   └── voice-design.md
└── README.md
```

## Documentation

* [Installation](docs/installation.md)
* [Reference Pipeline](docs/reference-pipeline.md)
* [Audio Restoration](docs/restoration.md)
* [Voice Design](docs/voice-design.md)
* [Evaluation](docs/evaluation.md)
* [Architecture](docs/architecture.md)
* [Machine Configuration](docs/machines.md)
* [Privacy](docs/privacy.md)

## License

MIT
