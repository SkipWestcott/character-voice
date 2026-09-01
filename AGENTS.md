# AGENTS.md

## Character Voice — Agent Guide

This repository provides tools for working with local AI voice generation.

The core workflow is:

```text
Audio Sample
    ↓
Reference Preparation
    ↓
Voice Variant
    ↓
Text-to-Speech
    ↓
Generated Audio
```

An agent working in this repository should understand the distinction between **source audio**, **reference audio**, **voice variants**, and **generated speech**.

---

## Core Capabilities

### 1. Analyze Audio

Inspect an audio file before processing it.

Useful measurements include:

* sample rate
* channels
* duration
* peak level
* RMS level
* crest factor
* silence ratio
* clipping ratio

Use analysis to understand the source before deciding how to process it.

Do not assume that a file needs processing simply because it can be processed.

---

### 2. Clean Reference Audio

Create a processed reference from an existing recording.

Typical operations include:

```text
Trim Silence
Remove DC Offset
High-Pass Filter
Noise Reduction
Dereverberation
Declipping
De-Essing
Gentle EQ
Level Adjustment
```

Processing should produce a **new file**.

Never modify the original recording.

The goal is not maximum audio quality. The goal is a reference that preserves the characteristics of the speaker while removing problems that interfere with voice cloning.

---

## Reference Presets

Reference creation supports different levels of processing.

### `direct`

Use the original recording without processing.

```text
Source → Reference
```

Use this when the recording is already clean.

### `minimal`

Apply basic cleanup while making minimal changes to the recording.

```text
Source → Minimal Cleanup → Reference
```

Use this when the recording is generally clean but needs minor preparation.

### `conservative`

Apply gentle processing intended to improve the reference while preserving the original voice characteristics.

```text
Source → Conservative Cleanup → Reference
```

This is the preferred starting point when the source needs cleanup.

### `aggressive`

Use stronger restoration for heavily degraded recordings.

```text
Source → Strong Restoration → Reference
```

Only use or document this preset if it is implemented by the current code.

---

## Reference Experiments

Voice cloning quality depends on the reference audio.

When results are poor, do not immediately assume the TTS model or generation parameters are the problem.

Test different references.

For example:

```text
Original
   ├── Direct
   ├── Minimal
   └── Conservative
             ↓
       Generate Each
             ↓
       Compare Results
```

A cleaner recording is not necessarily a better voice reference.

A longer recording is not necessarily a better voice reference.

A louder recording is not necessarily a better voice reference.

Evaluate references by their **generated voice similarity and quality**, not by how polished they sound in an audio editor.

---

## 3. Create Voice Variants

A voice variant is a reusable representation of a voice reference used for generation.

Conceptually:

```text
Reference Audio → Voice Variant
```

Create multiple variants when comparing:

* different source recordings
* different cleanup approaches
* different reference lengths
* different reference levels
* different processing chains

Keep experimental variants separate so results can be compared.

---

## 4. Generate Speech

Use a voice variant and text to generate speech.

```text
Voice Variant + Text
          ↓
    Generated Audio
```

Generation is probabilistic.

When a delivery is close but not ideal:

* generate another take
* adjust generation parameters
* keep the best take
* compare against other references

Do not assume that the first generated take represents the maximum quality of a voice variant.

---

## 5. Compare Takes

Treat generated audio as experimental output.

Compare:

### Voice

* speaker similarity
* timbre
* pitch characteristics
* vocal texture
* consistency

### Speech

* intelligibility
* pronunciation
* rhythm
* pacing
* emphasis

### Delivery

* emotion
* energy
* character
* naturalness
* adherence to the requested performance

A voice can be correct while the delivery is wrong.

Do not change the reference simply because one generated take has poor delivery.

---

## Audio Processing Philosophy

Prefer **small, testable changes**.

When experimenting:

```text
Original
   ↓
Candidate A
Candidate B
Candidate C
   ↓
Generate
   ↓
Compare
```

Do not stack many untested processing operations and then assume an improvement came from the entire chain.

Preserve successful candidates.

Record what changed.

---

## Level Experiments

Reference level can affect generation behavior.

When testing levels, treat level as an experimental variable rather than permanently normalizing every reference.

For example:

```text
Reference
 ├── Original Level
 ├── -3 dB
 ├── -6 dB
 ├── -9 dB
 ├── -12 dB
 ├── -15 dB
 └── -18 dB
```

Compare the generated results.

Do not assume LUFS normalization is required for voice cloning.

---

## TTS Backend

The current primary backend is:

**Qwen3-TTS 1.7B Base**

The integration should remain isolated from the rest of the audio workflow so that other TTS backends can be added later.

The agent should inspect the actual installed Qwen3-TTS API and existing scripts before creating new integration code.

Do not guess API parameters when the installed package or existing working scripts can be inspected.

---

## Local Audio Environment

The project is designed for local execution.

The typical environment may include:

```text
Python
PyTorch
CUDA
NVIDIA GPU
Qwen3-TTS
FFmpeg
SoX
```

Not every machine will have identical hardware or optional acceleration libraries.

Detect or configure these resources rather than hardcoding them.

---

## ComfyUI

ComfyUI can be part of the surrounding local workflow.

It is not the conceptual definition of the voice system.

The important pipeline is:

```text
Audio → Reference → Voice Variant → TTS → Audio
```

Keep core audio and TTS functionality usable independently of ComfyUI where practical.

---

## Useful Agent Operations

When asked to work with a voice, an agent should be able to reason about tasks such as:

```text
Analyze this recording
Clean this recording
Create a reference
Create alternate references
Compare reference candidates
Test reference levels
Create a voice variant
Generate speech
Generate multiple takes
Compare takes
Adjust generation parameters
Iterate on the voice
```

When a result is unsatisfactory, determine **which stage is responsible** before changing everything:

```text
Source Audio
     ↓
Reference Processing
     ↓
Voice Variant
     ↓
Generation
     ↓
Delivery
```

Change one stage at a time when possible.

---

## Important Rules

### Preserve Originals

Never overwrite source recordings.

### Preserve Candidates

Do not delete experimental references or successful generated takes merely because another candidate is preferred.

### Separate Identity From Delivery

Reference audio primarily affects **who the voice sounds like**.

Generation settings and text affect **how the voice performs**.

Evaluate those separately.

### Prefer Evidence

If a technique has been tested successfully, record the actual procedure.

If something is only theoretical or planned, label it accordingly.

Do not turn an experimental observation into a universal rule.

### Inspect Before Changing

Before modifying the audio pipeline:

1. Inspect the current implementation.
2. Inspect existing working scripts.
3. Inspect available CLI commands.
4. Test the smallest useful change.
5. Compare the result.

Do not replace a working implementation with an assumed one.

---

## Private Data

Voice recordings and character-specific data are local project data.

Do not place private recordings, generated character audio, or character-specific dialogue into the public repository.

Use synthetic examples and placeholders when documenting workflows.

---

## Agent Goal

The objective is not simply to produce speech.

The objective is to provide a **repeatable workflow for designing, testing, and refining a voice**:

```text
Record
  ↓
Analyze
  ↓
Clean
  ↓
Create Reference
  ↓
Create Voice Variant
  ↓
Generate
  ↓
Compare
  ↓
Adjust
  ↓
Repeat
```

Treat the repository as an experimental voice-design toolkit, not just a text-to-speech wrapper.
