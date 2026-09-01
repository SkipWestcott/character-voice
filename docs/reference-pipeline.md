# Reference Audio Pipeline

Voice-clone reference preparation is treated as an experiment, not a single mandatory cleanup chain.

## Recommended flow

```text
source recording
    ├── DIRECT      → untouched reference candidate
    ├── MINIMAL     → same source, format/transport changes only
    └── RESTORED    → conservative deterministic cleanup
                         ↓
                    analyze candidates
                         ↓
                    generate test takes
                         ↓
                 select the best reference
```

A short clean recording may already be the best reference. Do not assume that a longer or more processed recording is better.

## Extension strategy

If the source recording is too short, an extended reference can be built from a generated or additional recording, then cleaned and compared with the direct source. Keep this as a separate candidate strategy:

- `DIRECT`: original clean recording.
- `RESTORED`: original recording with conservative cleanup.
- `EXTENDED`: additional/generated material followed by cleanup.

Generated material can introduce artifacts or speaker-character changes, so it should not silently replace the original.

## Candidate rule

Keep processing reversible and independently switchable. The pipeline should make it easy to compare:

1. speaker similarity
2. content consistency / intelligibility
3. audio quality

These are separate evaluation dimensions. A polished waveform is not automatically a better speaker reference.

## Level matching

Reference level experiments are separate from restoration. If testing multiple levels, create separate candidates (for example, with controlled gain changes) and record the level in the candidate metadata. Do not bake a particular project-specific dB value into the generic pipeline.
