# Conservative Restoration

The default goal is **preserve the speaker while removing obvious technical defects**.

## Stage guidance

| Stage | Default | Use when | Risk |
|---|---|---|---|
| Trim / VAD | Optional | Excessive leading/trailing silence | Can remove useful breath/prosody |
| DC removal | Optional | Measurable DC offset | Very low |
| High-pass | Optional | Rumble / handling noise | Can thin the voice |
| Broadband denoise | Optional | Clearly audible steady noise | Can remove consonants or vocal texture |
| Dereverb | Optional | Strong room coloration | Can create artifacts |
| Declipping | Optional | Actual clipping is present | Reconstruction can alter timbre |
| Bandwidth restoration | Optional | Severe recording bandwidth limits | Can synthesize non-original detail |
| De-ess | Optional | Excessive sibilance | Can dull consonants |
| Gentle EQ | Optional | Clear spectral imbalance | Changes vocal identity |
| Loudness normalization | Not default | Delivery/mastering requirement | Changes dynamics and level |

The generic implementation intentionally keeps heavyweight ML enhancement out of the default path. If an external enhancement model is added, it should be an optional backend and its output should remain a separate candidate.

## What not to do by default

- Do not aggressively denoise a clean recording.
- Do not apply generative enhancement merely because the result sounds more polished.
- Do not normalize every reference to a fixed LUFS target without model-specific testing.
- Do not overwrite the source recording.
- Do not assume more seconds of audio means better speaker identity.

## Analysis

For each candidate, record at least sample rate, duration, channels, peak dBFS, RMS dBFS, crest factor, estimated silence ratio, and clipping ratio. These are diagnostic signals, not a replacement for listening and TTS evaluation.
