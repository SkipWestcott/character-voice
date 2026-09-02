# Reference Audio Pipeline

Voice-reference preparation is an experiment, not a mandatory cleanup chain.

The goal is to produce comparable candidates while preserving the original recording.

## Pipeline

```text
Source Recording
      │
      ├── DIRECT
      │
      ├── MINIMAL
      │
      └── CONSERVATIVE
             │
             ▼
        Analyze Candidates
             │
             ▼
       Generate Test Takes
             │
             ▼
          Evaluate
```

The source recording is never modified.

## Candidates

### DIRECT

The source is converted to the canonical WAV representation without intentional audio filtering.

For example, an MP3 source becomes a real PCM WAV file.

Direct is the baseline against which processing changes should be evaluated.

### MINIMAL

The source is converted to deterministic PCM WAV output without intentional audio filtering.

For sources that already match the target representation, Minimal may be effectively identical to Direct.

The distinction is conceptual: Direct establishes the unfiltered baseline, while Minimal represents basic format preparation.

### CONSERVATIVE

The source is converted to PCM WAV and receives restrained low-frequency cleanup.

The current implementation applies a 20 Hz high-pass filter.

This is deliberately mild. It is not a general-purpose restoration chain.

## Analyze Before Processing

Inspect the source before deciding whether processing is necessary:

```bash
./command/reference analyze <SOURCE_AUDIO>
```

For machine-readable output:

```bash
./command/reference analyze <SOURCE_AUDIO> --json
```

Current measurements include:

* sample rate
* channels
* duration
* sample width
* peak dBFS
* RMS dBFS
* crest factor
* estimated low-level/silence ratio
* estimated clipping ratio

These measurements are diagnostic rather than prescriptive.

In particular, the silence estimate is not speech detection. A high value does not automatically justify trimming.

## Build Candidates

Build the standard candidate set with:

```bash
./command/reference build \
  --input <SOURCE_AUDIO> \
  --output <REFERENCE_DIR>
```

The output contains:

```text
reference_direct.wav
reference_minimal.wav
reference_conservative.wav
```

Analysis JSON is also generated for each candidate.

## Evaluate Candidates

Candidate selection should be based on the actual TTS task.

Compare candidates using the same controlled text and, when appropriate, multiple generated takes.

Evaluate independently:

### Speaker similarity

Does the generated voice resemble the intended speaker or character?

### Content consistency

Is the requested text rendered clearly and faithfully?

### Audio quality

Are there clicks, pumping, metallic artifacts, excessive noise, or bandwidth problems?

### Delivery

Does the generated speech have the desired timing, emphasis, prosody, and character?

A candidate can perform well on one dimension and poorly on another.

## Processing Principle

Do not assume that:

* louder is better
* longer is better
* cleaner is better
* more processed is better
* less silence is better
* a technically superior waveform produces a better cloned voice

The reference is ultimately evaluated by how well it works in the intended TTS system.

## Level Experiments

Reference level experiments are separate from restoration.

If testing different levels, create separate candidates and record the gain used for each.

Do not bake a project-specific level into the generic pipeline.

For example, a private experiment may compare several controlled gain settings, but the repository should not assume that any particular dB value is universally optimal.

## Future Extensions

Additional processing can be added later as independent candidates.

Potential techniques include:

* broadband denoising
* dereverberation
* declipping
* de-essing
* gentle EQ
* speech-aware trimming
* bandwidth restoration
* ML-based enhancement

These should remain optional and independently testable.

They should not replace the direct baseline or become automatic defaults merely because they produce a more polished waveform.
