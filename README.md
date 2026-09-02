# Character Voice

A local toolkit for preparing, cloning, and designing character voices with Qwen3-TTS.

## Workflows

Character Voice has three distinct workflows:

Clean:
Audio -> Reference

Clone:
Reference + Transcript -> Generated Speech

Design:
Voice Description + Text -> Generated Speech

- Clean prepares an existing recording for use as a reference.
- Clone reproduces a voice from reference audio and its transcript.
- Design creates a voice from a natural-language description without requiring reference audio.

## Design

Voice Design is useful when the desired character voice does not yet have a reference recording.

Example:

    ./command/design \
      --instruct "A calm, articulate middle-aged male voice with a warm low register and restrained authority." \
      --text "Hello. This is a test."

Optional language and output path:

    ./command/design \
      --instruct "A calm, articulate middle-aged male voice with a warm low register and restrained authority." \
      --text "Hello. This is a test." \
      --language English \
      --output output/example.wav

Design is intentionally iterative:

    Voice Description
           |
           v
    VoiceDesign Model
           |
           v
    Generated Take
           |
           v
    Evaluation
           |
           v
    Revise Description
           |
           v
    Generate Again

A useful voice description can specify:

- apparent age
- register
- vocal texture
- resonance
- articulation
- speaking energy
- emotional character
- authority or softness
- pacing or delivery tendencies

A good description does not necessarily produce a fixed or perfectly deterministic voice. Generate multiple takes when identity or delivery is important.

## Clone

Clone requires reference audio and, unless using x-vector-only mode, a transcript of that reference.

Example:

    ./command/run "Synthetic example dialogue."

Clone is appropriate when a specific recorded voice should be reproduced.

## Clean

The cleaning and reference-building tools prepare recordings for cloning:

    Audio
      |
      v
    Analysis
      |
      v
    Cleaning / Restoration
      |
      v
    Reference Candidates
      |
      v
    Evaluation

The cleaning pipeline does not create a character identity by itself. Its purpose is to produce better reference material for the Clone workflow.

## Configuration

Copy the machine template:

    cp config/machine.example.env config/local.env

Then configure the paths for the local Qwen installation.

The tracked defaults contain no machine-specific paths or private audio. config/local.env is ignored by Git and should remain local.

Important settings include:

    QWEN_TTS_PYTHON=/path/to/qwen-tts-venv/bin/python
    QWEN_TTS_MODEL=/path/to/models/Qwen3-TTS-12Hz-1.7B-Base
    QWEN_TTS_DESIGN_MODEL=/path/to/models/Qwen3-TTS-12Hz-1.7B-VoiceDesign
    REFERENCE_AUDIO=/path/to/private/reference.wav
    REFERENCE_TEXT="Transcript of the reference recording."
    OUTPUT_DIR=/path/to/output

Clone and Design use separate model configuration because they are different Qwen3-TTS workflows.

## Status

Check the local environment:

    ./command/status

Status reports readiness for both Clone and Design independently.

## Project Structure

    command/
      design
      reference
      run
      setup
      status

    execute/
      audio_analyze.py
      audio_clean.py
      design
      generate_design.py
      generate_tts.py
      reference_builder.py
      run
      status

    config/
      defaults.env
      machine.example.env
      local.env          # local only, ignored by Git

    docs/
      architecture.md
      evaluation.md
      installation.md
      machines.md
      privacy.md
      reference-pipeline.md
      restoration.md
      voice-design.md

## Privacy

Private recordings, transcripts, character descriptions, generated audio, and machine-specific configuration should remain outside the public repository.

The repository should contain reusable tooling and documentation, not character-specific assets or private production data.
