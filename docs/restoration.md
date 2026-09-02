# Audio Restoration

Audio restoration is optional.

The default goal is to **preserve the speaker while removing obvious technical problems**. Processing should only be used when there is evidence that it helps the reference.

A cleaner or more polished recording is not necessarily a better voice-cloning reference.

## Current Implementation

The current pipeline provides only restrained deterministic preparation:

| Preset         | Current behavior                                          |
| -------------- | --------------------------------------------------------- |
| `direct`       | Convert source to canonical WAV; no intentional filtering |
| `minimal`      | Deterministic PCM WAV preparation                         |
| `conservative` | Minimal preparation plus 20 Hz high-pass                  |

The repository does **not** currently implement general-purpose denoising, dereverberation, declipping, de-essing, EQ, or generative enhancement.

## Restoration Techniques

The following techniques are useful when a source has a specific problem. They are described here as methodology and future extension points rather than automatic processing stages.

### Trim / Speech Detection

**Use when:** the recording contains excessive leading or trailing material.

**Risk:** removing useful breaths, pauses, or natural prosody.

Do not trim solely because an analyzer reports a high silence ratio. The current silence measurement is an amplitude estimate, not speech detection.

### DC Removal

**Use when:** measurable DC offset is present.

**Risk:** generally low, but unnecessary processing should still be avoided.

### High-Pass Filtering

**Use when:** there is genuine low-frequency rumble, handling noise, or other unwanted energy below the useful vocal range.

**Risk:** an unnecessarily high cutoff can thin the voice.

The current Conservative preset applies only a restrained 20 Hz high-pass.

A stronger high-pass should be an explicit experiment rather than an assumption.

### Broadband Denoising

**Use when:** steady background noise is clearly audible.

**Risk:** denoising can remove consonants, breath detail, and vocal texture. Excessive processing can produce watery or metallic artifacts.

Do not denoise a clean recording simply because noise-reduction software is available.

### Dereverberation

**Use when:** room reflections significantly color the recording.

**Risk:** dereverberation can introduce artifacts and alter the character of the voice.

Keep dereverberated output as a separate candidate.

### Declipping

**Use when:** actual digital clipping is present.

**Risk:** clipped samples must be reconstructed. The result can change vocal timbre or introduce artifacts.

Do not apply declipping to a recording that is not clipped.

### De-Essing

**Use when:** excessive sibilance is clearly interfering with the recording.

**Risk:** excessive reduction can dull consonants and speech intelligibility.

### Gentle EQ

**Use when:** the recording has a clear spectral imbalance that interferes with the intended reference.

**Risk:** EQ changes vocal timbre and therefore can affect speaker identity.

EQ should be treated as an experiment, not cosmetic mastering.

### Loudness Normalization

**Use when:** a controlled delivery or level experiment requires it.

**Risk:** normalization changes the signal level and potentially its dynamics.

Do not normalize every reference to a universal LUFS target without evidence that the target benefits the TTS system.

### Bandwidth Restoration

**Use when:** the original recording has unusually restricted bandwidth.

**Risk:** restoration systems may synthesize information that was not present in the source.

Any reconstructed high-frequency content should be treated as experimental.

### Generative Enhancement

**Use when:** a separate experiment is specifically intended to test whether an enhancement model improves the TTS reference.

**Risk:** generative enhancement can alter pronunciation, vocal texture, timing, or speaker identity.

Enhanced output must remain a separate candidate. It must never silently replace the original.

## Recommended Decision Process

Use:

```text id="g4yrxr"
Analyze
   ↓
Identify an actual problem
   ↓
Choose the narrowest technique that addresses it
   ↓
Create a separate candidate
   ↓
Compare against the unprocessed baseline
   ↓
Evaluate in the actual TTS task
```

Do not start with a restoration stack and assume every stage is beneficial.

## Candidate Preservation

Always preserve:

1. the original recording
2. the direct baseline
3. each processed candidate
4. the processing settings

This makes it possible to determine whether a particular technique actually helped.

## Evaluation

Restoration should be judged by the resulting voice-cloning task, not by waveform appearance alone.

Compare:

* speaker similarity
* intelligibility
* content consistency
* audio artifacts
* delivery/prosody
* generalization to different text

A technically cleaner signal can still produce a worse cloned voice.

## Extension Principle

When a new restoration technique is implemented, it should be:

* optional
* independently selectable
* reproducible
* separately output
* comparable with the Direct baseline
* documented according to its actual implementation

Avoid turning a useful experimental technique into a mandatory preprocessing chain.
