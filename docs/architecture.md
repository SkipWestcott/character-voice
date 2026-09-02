# Architecture

Character Voice is organized as a small command layer around reusable audio-processing and TTS execution scripts.

The architecture separates **what the user does** from **how the operation is implemented**.

## Workflow

```text
Audio Source
    ↓
command/reference
    ↓
execute/audio_analyze.py
execute/reference_builder.py
execute/audio_clean.py
    ↓
Reference Candidate
    ↓
config/local.env
    ↓
command/run
    ↓
execute/generate_tts.py
    ↓
Generated Audio
```

## Repository Layers

### `command/`

Human-facing entry points.

Current commands:

```text
command/setup
command/status
command/reference
command/run
```

The command layer handles configuration loading, basic validation, and dispatch.

It should remain thin.

### `execute/`

Implementation logic.

Current components include:

```text
execute/audio_analyze.py
execute/audio_clean.py
execute/reference_builder.py
execute/generate_tts.py
```

These scripts perform the actual audio inspection, reference preparation, candidate construction, and TTS generation.

### `config/`

Configuration templates and local machine settings.

```text
config/defaults.env
config/machine.example.env
config/local.env
```

`config/local.env` is machine-specific and ignored by Git.

Source code should not contain private machine paths.

### `docs/`

Documents the workflow, methodology, installation requirements, and public/private boundary.

Documentation should describe behavior that exists in the repository rather than planned functionality.

## Reference Pipeline

Reference processing is intentionally independent from Qwen3-TTS.

The pipeline can:

1. inspect a source recording
2. create reference candidates
3. inspect the resulting candidates
4. select a candidate for TTS testing

Reference preparation does not require loading the Qwen model.

This allows audio decisions to be made before expensive TTS generation.

## TTS Layer

`execute/generate_tts.py` provides the repository's integration with the installed Qwen3-TTS package.

The project does not reimplement the model.

The executor:

1. loads the configured Qwen Python environment
2. loads the configured model
3. creates a voice-cloning prompt from the configured reference
4. generates speech
5. writes the resulting waveform

The integration should follow the API exposed by the installed Qwen package.

Do not invent or assume model parameters.

## Configuration Boundary

Machine-specific resources enter the system through environment configuration:

```text
QWEN_TTS_PYTHON
QWEN_TTS_MODEL
REFERENCE_AUDIO
REFERENCE_TEXT
OUTPUT_DIR
```

This keeps the execution code independent of:

* usernames
* hostnames
* absolute filesystem layouts
* private recordings
* character-specific data

## Audio Data Boundary

The repository contains processing logic, not private audio.

A typical local workflow is:

```text
Private source recording
        ↓
Local reference candidates
        ↓
Selected local reference
        ↓
Local TTS generation
        ↓
Local generated audio
```

These files should remain outside version control.

## Reversibility

The source recording is never modified by the reference pipeline.

Processing creates new candidate files.

This makes it possible to compare:

```text
original
direct
minimal
conservative
experimental
```

without destroying the original input.

## Extensibility

New processing techniques should normally be added as explicit operations or presets rather than silently changing an existing baseline.

For example:

```text
minimal
conservative
experimental-denoise
experimental-declip
```

An experimental technique should not redefine what an existing preset means.

Likewise, new TTS backends should remain isolated from the existing Qwen integration rather than adding backend-specific behavior throughout the command layer.

## Design Rule

The repository should make the following separation obvious:

```text
Commands
    → orchestration

Execution
    → implementation

Configuration
    → machine-specific resources

Audio
    → local/private data

Model
    → external Qwen3-TTS installation
```

A new machine should primarily require new configuration.

A new audio experiment should primarily require a new candidate or processing operation.

A change to the TTS backend should primarily affect the TTS execution layer.
