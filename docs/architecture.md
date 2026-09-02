# Architecture

## Overview

Character Voice is a portable command-line toolkit for developing AI character
voices with Qwen3-TTS.

The architecture separates three distinct workflows:

                         ┌── Clean ──→ Reference
                         │
Character Voice ─────────┼── Clone ───→ Generated Speech
                         │
                         └── Design ──→ Generated Speech

The workflows share the same repository and command conventions but do not
represent the same operation.

- Clean prepares reference audio.
- Clone uses reference audio and its transcript to generate speech.
- Design generates speech from a natural-language voice description without
  requiring reference audio.

Design does not currently feed automatically into Clone.

## Command Boundary

The public interface is contained in `command/`.

Current commands:

    command/reference
    command/run
    command/design

The command layer should remain small.

Its responsibilities are:

- expose stable user-facing commands,
- establish the repository root,
- forward arguments,
- and invoke the corresponding implementation.

It should not contain model-specific inference logic.

## Execution Boundary

Workflow orchestration lives in `execute/`.

Current implementations:

    execute/reference
    execute/run
    execute/design
    execute/status

The execution layer is responsible for:

- loading tracked and local configuration,
- validating prerequisites,
- selecting the configured runtime,
- selecting the appropriate model,
- invoking the backend,
- and reporting failures clearly.

The execution layer should not contain character-specific identity data.

## Model Integration

Python model integration is kept separate from the shell command interface.

Current Qwen generation implementations include:

    execute/generate_tts.py
    execute/generate_design.py

This separation allows the command interface and workflow structure to remain
stable if the model backend changes.

Qwen-specific API calls should remain isolated to the generation implementation.

Do not spread Qwen imports, model-specific parameters, or inference details into
the public command wrappers unless there is a concrete reason to do so.

## Clean Workflow

Clean is the reference-audio preparation stage.

Conceptually:

    source audio
         ↓
    analyze / inspect
         ↓
    clean / normalize
         ↓
    reference candidates

The resulting reference is an input to Clone.

Clean does not synthesize character speech.

Reference processing should remain independent of the generation backend where
practical.

## Clone Workflow

Clone uses an existing reference recording and its transcript.

Conceptually:

    reference audio ─────┐
                         ├──→ Qwen Clone ──→ generated speech
    reference transcript ┘

    synthesis text ────────────────────────→

The reference audio establishes the source voice.

The reference transcript allows the cloning model to associate the recording
with its spoken content.

Clone configuration includes:

    QWEN_TTS_MODEL
    REFERENCE_AUDIO
    REFERENCE_TEXT

Clone should not require VoiceDesign-specific configuration.

## Design Workflow

Design creates a voice from a natural-language description.

Conceptually:

    voice description ──┐
                       ├──→ Qwen VoiceDesign ──→ generated speech
    synthesis text ────┘

Design configuration includes:

    QWEN_TTS_DESIGN_MODEL

It does not require:

    REFERENCE_AUDIO
    REFERENCE_TEXT

This distinction is intentional.

Design is useful when the desired voice does not yet have a reference recording,
or when exploring possible character identities before committing to a reference.

## Design Iteration

Design is naturally iterative:

    description
        ↓
    generation
        ↓
    listening
        ↓
    evaluation
        ↓
    revised description
        ↓
    generation

The generated audio is an experimental result.

It is not automatically treated as a reference recording.

A future workflow may allow a deliberately selected Design result to become input
to Clone, but that is outside the current architecture.

Do not implement Design → Clone automatically unless explicitly requested.

## Identity and Delivery

Voice identity and line delivery should be treated as separate concerns.

Identity describes relatively persistent vocal characteristics:

- apparent age,
- pitch or register,
- vocal weight,
- brightness,
- texture,
- resonance,
- articulation,
- and other recognizable qualities.

Delivery describes how the character performs a particular line:

- emotional state,
- energy,
- confidence,
- pacing,
- restraint,
- conversational style,
- emphasis,
- and similar performance qualities.

This distinction matters during Design iteration.

If identity is correct but delivery is wrong, revise the delivery instruction before
discarding the voice design.

If identity is wrong, revise the voice description itself.

The implementation should not assume that one universal prompt structure is
correct for every character.

## Configuration Boundary

Configuration is divided between portable defaults and machine-specific values.

Tracked:

    config/defaults.env
    config/machine.example.env

Local and ignored:

    config/local.env

The principal configuration variables are:

    QWEN_TTS_PYTHON
    QWEN_TTS_MODEL
    QWEN_TTS_DESIGN_MODEL
    REFERENCE_AUDIO
    REFERENCE_TEXT
    OUTPUT_DIR

The model paths for Clone and Design are intentionally separate.

Machine-specific paths must not be embedded in tracked implementation.

Character-specific reference recordings and private transcripts must also remain
outside the public repository unless explicitly intended to be public.

## Backend Isolation

The repository should treat Qwen3-TTS as an implementation dependency rather than
as the definition of the public interface.

The desired dependency direction is:

    command
       ↓
    execute
       ↓
    generation backend
       ↓
    Qwen3-TTS

Not:

    command
       ↓
    Qwen-specific inference details

This keeps the workflow understandable and makes future backend replacement or
addition possible.

## Audio Boundary

Generated audio is the primary behavioral artifact.

A successful synthesis operation should produce a usable WAV file with expected
audio properties.

Technical validation and perceptual evaluation are separate:

    technical validation
        ↓
    valid, playable audio

    perceptual evaluation
        ↓
    identity / naturalness / adherence / delivery

Both matter.

The architecture should not introduce processing that changes the character voice
without a clear reason.

Reference normalization, generated-output processing, and voice-design behavior
should remain distinguishable operations.

## Status and Diagnostics

`command/status` provides environment diagnostics.

It should answer whether the local machine is capable of running the configured
workflows.

Relevant checks include:

- configuration,
- configured model directories,
- Python availability,
- PyTorch availability,
- CUDA availability,
- visible GPU,
- VRAM,
- and Qwen package availability.

Clone and Design readiness are evaluated independently.

A machine can therefore be:

- Clone-ready,
- Design-ready,
- ready for both,
- or ready for neither.

Status is diagnostic; it should not perform model generation.

## Runtime Model Loading

The current command-line implementation may start a new Python process and load a
model for each generation.

This is acceptable for the current architecture.

Repeated model loading may become a performance concern during iterative Design,
but persistent model workers, daemons, caches, or sessions are not currently part
of the architecture.

If persistent inference is introduced later, it should preserve the existing
command semantics and be treated as an explicit runtime architecture change.

## Privacy Boundary

The repository is intended to remain generic and portable.

Public source should not contain:

- private reference recordings,
- private transcripts,
- personal recordings,
- private dialogue,
- machine-specific home directories,
- credentials,
- API keys,
- local model cache paths,
- identifying infrastructure details,
- or character-specific secrets.

Local configuration and generated audio should remain outside version control when
they contain private material.

The architecture therefore separates:

    public implementation
            +
    local environment
            +
    private character assets

rather than embedding all three together.

## Testing Boundary

Testing should proceed from inexpensive checks to real inference.

Typical progression:

    shell syntax
        ↓
    Python syntax
        ↓
    argument validation
        ↓
    environment/status validation
        ↓
    actual model generation
        ↓
    WAV validation
        ↓
    listening / perceptual evaluation

Changes to shared infrastructure should include regression testing for every
affected workflow.

A successful model load or process exit is not evidence that the resulting voice
is correct.

## Architectural Principles

Preserve these principles when extending the repository:

1. Keep Clean, Clone, and Design conceptually distinct.
2. Keep the public command layer small.
3. Keep model-specific code isolated.
4. Keep machine-specific configuration local.
5. Keep private character assets out of tracked source.
6. Do not turn one character's successful settings into global defaults.
7. Treat generated audio as the final behavioral artifact.
8. Evaluate voice changes by listening, not only by technical tests.
9. Prefer the smallest change that satisfies the requirement.
10. Do not introduce persistent infrastructure without a concrete need.
11. Keep documentation synchronized with actual implementation.
12. Do not automatically commit or push repository changes.
