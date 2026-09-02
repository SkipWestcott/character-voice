# AGENTS.md

## Purpose

Character Voice is a local toolkit for character voice development using Qwen3-TTS.

The project is concerned primarily with:

- audio preparation
- reference construction
- voice cloning
- voice design
- generated speech
- listening and evaluation
- reproducible local workflows

Treat the audio behavior of the system as the primary product surface.

## Core Workflows

There are three distinct workflows.

    Clean:
    Audio -> Reference

    Clone:
    Reference + Transcript -> Generated Speech

    Design:
    Voice Description + Text -> Generated Speech

Do not collapse these workflows into a single generic path.

### Clean

Clean prepares source audio for use as a reference.

Relevant components include:

- `execute/audio_analyze.py`
- `execute/audio_clean.py`
- `execute/reference_builder.py`

Cleaning should improve the usability of source material without introducing unnecessary character or voice changes.

### Clone

Clone reproduces a voice from reference material.

Clone normally requires:

- reference audio
- reference transcript
- Clone model

The primary executor is:

- `execute/generate_tts.py`

The command entry point is:

- `command/run`

Do not change Clone behavior merely to accommodate Design.

### Design

Design creates a voice from a natural-language voice description.

Generated Design audio is an experimental result and is not automatically promoted to a Clone reference.

Design requires:

- VoiceDesign model
- voice description
- synthesis text

Design does not require:

- reference audio
- reference transcript
- an existing character voice

The primary executor is:

- `execute/generate_design.py`

The command entry point is:

- `command/design`

Do not route Design through the Clone executor.

Do not require reference configuration for Design.

## Voice Design Is Iterative

Voice Design should be treated as an exploration process:

    Description
        |
        v
    Generate
        |
        v
    Listen
        |
        v
    Evaluate
        |
        v
    Revise
        |
        v
    Generate Again

A single generated take should not automatically be treated as the canonical voice.

When useful, generate multiple takes and compare them.

## Evaluate Identity Separately From Delivery

When assessing generated speech, distinguish:

### Identity

- distinctiveness
- consistency
- vocal texture
- character fit
- apparent age
- register

### Delivery

- pacing
- emphasis
- pauses
- articulation
- emotional intensity
- conversational naturalness

A good performance does not necessarily indicate a good character voice.

A strong character identity does not necessarily produce good delivery.

When debugging a result, identify which of these is actually failing before changing the voice description or generation implementation.

## Audio First

Changes to generation code should be evaluated by listening to generated audio.

Do not assume that a technically successful generation is a successful voice result.

Useful evaluation questions include:

- Did the generated voice follow the requested characteristics?
- Is the identity distinctive?
- Is the delivery natural?
- Did the output introduce artifacts?
- Does the result remain useful across different text?
- Does a change improve the intended property without damaging another one?

When comparing settings or descriptions, change meaningful variables deliberately and keep comparisons controlled.

## Qwen Integration

Qwen-specific model loading and generation behavior belongs in executor modules.

Keep the command layer thin.

Current generation executors:

- `execute/generate_tts.py` — Clone
- `execute/generate_design.py` — Design

Do not spread Qwen-specific implementation details through unrelated commands.

Do not invent Qwen generation parameters. Verify the installed API before exposing new settings.

## Configuration

Tracked configuration must remain machine-neutral.

Use:

- `config/defaults.env` for tracked defaults
- `config/machine.example.env` for configuration examples
- `config/local.env` for machine-specific configuration

`config/local.env` is ignored by Git.

Never add private:

- audio
- transcripts
- character descriptions
- generated takes
- machine paths
- hostnames
- IP addresses
- credentials
- environment-specific secrets

to tracked files.

## Repository Safety

Before changing an existing workflow, inspect its current behavior.

Preserve working Clone and Clean functionality while adding Design.

Do not silently replace an existing workflow with a different implementation.

If a change affects generated audio, test the affected workflow before considering the change complete.

## Testing

Prefer this progression:

1. static or syntax validation
2. CLI validation
3. mocked execution where practical
4. real local generation
5. audio inspection
6. listening/evaluation
7. regression test of unaffected workflows

A successful Python process is not sufficient validation for an audio-generation change.

## Documentation

Keep documentation aligned with the actual architecture.

If adding or removing a workflow, update diagrams that describe the workflow structure.

In particular, do not leave diagrams implying that every workflow begins with audio if Design does not.

## Git

Do not commit or push automatically.

First:

1. inspect the changes
2. run local validation
3. run relevant audio tests
4. review the diff
5. present the changes for human review

The GitHub repository is the distribution surface for the toolkit. The audio-generation behavior is the primary concern.

## Local Agent Bootstrap

Before changing code, establish the local runtime.

    pwd
    git status --short
    find command execute -maxdepth 2 -type f | sort
    ./command/status

Local configuration contains machine-specific paths and must remain outside
tracked files. Important settings are:

    QWEN_TTS_PYTHON
    QWEN_TTS_MODEL
    QWEN_TTS_DESIGN_MODEL
    REFERENCE_AUDIO
    REFERENCE_TEXT
    OUTPUT_DIR

Use the configured Qwen Python rather than assuming the system Python has
qwen_tts installed.

## Agent Change Procedure

For a non-trivial change:

1. inspect the existing implementation;
2. identify the workflow boundary being changed;
3. make the smallest coherent change;
4. run static validation;
5. run the affected workflow;
6. inspect generated audio and listen to it when applicable;
7. review the diff;
8. update documentation when behavior changes;
9. stop for human review before committing or pushing.

A successful Python invocation is not sufficient validation for audio changes.
The generated speech is the primary product surface.

Useful validation commands include:

    python -m py_compile execute/*.py
    git diff --check
    ./command/status

For synthesis changes, perform an actual `./command/design` or `./command/run`
test and inspect the resulting WAV.

Generated validation audio is disposable unless intentionally tracked.

## Local Audio Diagnostics

When debugging synthesis, separate these questions:

- Did the command execute?
- Did the model load?
- Was a valid WAV produced?
- Does the WAV have the expected format?
- Does the voice sound correct?
- Does the voice remain consistent across different text?

Use standard local audio tools when available, for example:

    file output/example.wav
    ffprobe output/example.wav

Do not infer voice quality from logs alone.

## Practical Qwen Rule

The installed Qwen package and local model installation are the source of truth.

Before introducing a Qwen-specific parameter or behavior:

1. inspect the installed package;
2. inspect the actual callable signature;
3. confirm the local model path;
4. run a real synthesis test.

Do not guess undocumented parameters.

Keep Qwen-specific behavior isolated in the execution layer rather than
spreading provider-specific logic through command wrappers.

## Agent Git Rule

Do not automatically commit or push changes.

Before requesting review, inspect:

    git status
    git diff --stat
    git diff
    git diff --check

Do not commit private reference recordings, local environment files, model
weights, credentials, or machine-specific configuration.
