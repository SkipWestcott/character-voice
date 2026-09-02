# Voice Design Methodology

Character Voice treats voice design as an iterative audio experiment rather than a single preprocessing step.

The goal is to find a combination of reference material and generation settings that produces a consistent, useful character voice.

## Core Workflow

```text id="w9g1x3"
Reference Selection
        ↓
Reference Preparation
        ↓
Candidate Evaluation
        ↓
Voice Clone
        ↓
Generated Takes
        ↓
Evaluation
        ↓
Selection
```

Each stage should remain independently adjustable.

## 1. Reference Selection

Start with a recording that represents the intended speaker or character.

Prefer a recording that is:

* intelligible
* representative of the desired voice
* free of major technical defects
* long enough for the intended cloning method
* naturally performed rather than heavily processed

Do not assume that a longer recording is automatically better.

Do not assume that a technically perfect recording is automatically the best reference.

The actual TTS result determines whether a reference is useful.

## 2. Reference Analysis

Analyze the source before processing it:

```bash id="8pjrbi"
./command/reference analyze <SOURCE_AUDIO>
```

The analyzer provides basic technical measurements.

These measurements help identify obvious problems, but they do not measure speaker similarity or character quality.

In particular, silence estimates should not be treated as automatic speech detection.

## 3. Reference Preparation

Build comparable candidates:

```bash id="9qf5bn"
./command/reference build \
  --input <SOURCE_AUDIO> \
  --output <REFERENCE_DIR>
```

The current candidates are:

```text id="i4k0hx"
reference_direct.wav
reference_minimal.wav
reference_conservative.wav
```

The Direct candidate provides the unfiltered baseline.

Minimal provides deterministic format preparation.

Conservative applies restrained low-frequency cleanup.

The source recording remains unchanged.

## 4. Candidate Evaluation

Candidates should be evaluated through the actual voice-cloning task.

For each candidate, use the same controlled text whenever possible.

Evaluate independently:

### Speaker identity

Does the generated voice sound like the intended speaker?

### Consistency

Does the voice remain recognizable across different text?

### Intelligibility

Are words rendered clearly and accurately?

### Audio quality

Are there unwanted artifacts, noise, distortion, pumping, or metallic sounds?

### Delivery

Does the generated voice have the intended rhythm, emphasis, emotion, and character?

A candidate can perform well on one dimension and poorly on another.

## 5. Generation

Once a reference candidate has been selected, configure it locally and generate speech:

```bash id="wxyb5u"
./command/run "Synthetic example dialogue."
```

For normal ICL voice cloning, the reference transcript must correspond to the reference audio.

Speaker-embedding-only cloning can be tested with:

```bash id="tmyqv7"
./command/run \
  --x-vector-only \
  "Synthetic example dialogue."
```

Generation settings should be recorded when comparing experiments.

## 6. Multiple Takes

A single generated take is not necessarily representative.

When the generation process is stochastic, produce multiple takes using the same reference and text.

Compare the takes for:

* identity consistency
* pronunciation
* delivery
* artifacts
* prosody

A good reference should remain useful across more than one generated sentence or take.

## 7. Parameter Experiments

Change one meaningful variable at a time.

Examples include:

* reference candidate
* reference level
* generation settings
* reference duration
* processing technique

Do not change several variables simultaneously and then attribute the result to one of them.

Reference-level experiments should use separate candidates rather than modifying the source.

## 8. Level Testing

Reference level can be tested independently from restoration.

For example, controlled gain variants can be created and compared:

```text id="a1pxi4"
reference
    ├── level variant A
    ├── level variant B
    └── level variant C
```

The repository should not assume that one particular level is universally optimal.

A level that works for one voice or recording may not work for another.

## 9. Processing Experiments

If restoration is necessary, use the narrowest operation that addresses the observed problem.

Do not automatically apply:

* denoising
* dereverberation
* declipping
* de-essing
* EQ
* normalization
* generative enhancement

The current implementation is intentionally limited to deterministic preparation and restrained low-frequency cleanup.

Future processing techniques should remain separate experimental candidates.

## 10. Generated Audio as a Reference

Generated audio can be tested as a reference in a separate experiment, but it should never silently replace the original recording.

Generated material can introduce:

* pronunciation changes
* timing changes
* artifacts
* altered vocal texture
* character drift

Keep generated-reference experiments clearly separated from original-reference experiments.

## 11. Selection

The final reference should be selected based on observed performance in the intended TTS task.

A useful selection record should identify:

```text id="7bq5c3"
Reference candidate
Generation settings
Test text
Take/result
Speaker similarity
Intelligibility
Audio quality
Delivery
Notes
```

The winning candidate is not necessarily the one with:

* the highest level
* the longest duration
* the lowest noise
* the most processing
* the most polished waveform

It is the candidate that produces the most useful voice.

## Design Principle

Voice design is an empirical process.

The pipeline should make experiments **comparable, reversible, and explicit** rather than hiding decisions inside an automatic cleanup chain.
::
