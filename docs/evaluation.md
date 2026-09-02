# Reference Evaluation

Reference quality should be evaluated through the actual TTS task, not by waveform appearance alone.

A reference that looks cleaner, louder, or more technically polished is not necessarily a better voice reference.

## Evaluation Dimensions

Evaluate each candidate independently on four dimensions.

### Speaker Similarity

Does the generated voice sound like the intended speaker or character?

Consider:

* vocal identity
* timbre
* characteristic vocal qualities
* consistency across different phrases

### Content Consistency

Does the generated system render the requested text correctly?

Consider:

* pronunciation
* missing or changed words
* repeated words
* unexpected sounds
* intelligibility

### Audio Quality

Does the generated result contain unwanted artifacts?

Listen for:

* clicks
* distortion
* metallic or synthetic textures
* pumping
* excessive noise
* bandwidth problems
* unstable voice quality

### Delivery

Does the generated speech deliver the text appropriately?

Consider:

* rhythm
* pacing
* emphasis
* pauses
* prosody
* emotional character

Speaker similarity and delivery quality should not be treated as the same measurement.

A voice can sound highly similar while delivering a line poorly.

## Controlled Comparison

When comparing reference candidates, keep the other variables fixed.

For example:

```text id="q1y7dn"
Candidate A → same test text → Take 1
Candidate B → same test text → Take 1
Candidate C → same test text → Take 1
```

Then repeat if necessary.

This makes differences between candidates easier to attribute.

## Multiple Takes

If generation is stochastic, produce multiple takes from the same candidate.

For example:

```text id="7m2c4p"
reference_minimal
    ├── take 01
    ├── take 02
    └── take 03
```

Do not reject a reference solely because of one poor generation.

Likewise, do not select a reference solely because it produced one unusually good take.

Look for repeatable behavior.

## Test Text

Use short synthetic test phrases when evaluating reference candidates.

The test text should make it possible to hear:

* normal speech
* different word combinations
* consonants and vowels
* pacing
* emphasis
* longer phrases

Keep the test text unchanged when comparing candidates.

Private character dialogue should not be committed to the repository.

## Evaluation Record

For each comparison, record the relevant experimental conditions.

A simple record can look like:

```text id="h3p0xa"
Reference:
Test text:
Generation settings:
Take:

Speaker similarity:
Content consistency:
Audio quality:
Delivery:

Notes:
```

The exact scoring system is less important than using the same criteria consistently.

A simple numerical scale can be useful:

```text id="4t8nq2"
1 = poor
2 = weak
3 = acceptable
4 = good
5 = excellent
```

Use the scale comparatively rather than treating the numbers as an objective measurement of voice quality.

## What Not to Infer

Do not infer TTS quality from a single waveform metric.

For example:

* higher peak level does not mean better cloning
* lower noise does not mean better speaker identity
* longer duration does not mean better reference quality
* more processing does not mean better output
* lower silence ratio does not necessarily mean better reference quality

Technical analysis and listening evaluation answer different questions.

## Selecting a Reference

A practical selection process is:

1. Analyze the source.
2. Build the available reference candidates.
3. Generate the same test text from each candidate.
4. Produce additional takes when needed.
5. Compare speaker similarity, content consistency, audio quality, and delivery separately.
6. Select the candidate that performs best for the intended use.

Do not optimize for a single metric when the actual objective is a usable character voice.

## Evaluation Principle

The purpose of evaluation is to expose tradeoffs.

The pipeline should make it easy to answer:

> Which reference produces the most useful generated voice under the same conditions?

It should not attempt to hide that decision behind an automatic “best reference” score.
