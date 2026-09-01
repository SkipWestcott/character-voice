# Character Voice

**Create and clean up local AI character voices from short audio samples, then generate speech with reusable voice variants.**

Everything runs locally using Qwen3-TTS. Keep your recordings, voice variants, generated audio, and character data on your own machine.

## Capabilities

### 1. Create a Voice Variant

Start with a short voice sample and turn it into a reusable voice variant.

```text
Sample Audio → Voice Variant
```

A voice variant captures the characteristics you want to reuse for a character. Create multiple variants from different samples or processing approaches and compare the results.

### 2. Clean Up a Sample Clip

Have a good performance recorded with poor audio quality? Clean the clip before using it as a voice reference.

```text
Sample Clip → Cleanup → Reference Clip
```

The cleanup pipeline can be used for things such as:

* noise reduction
* silence / speech trimming
* high-pass filtering
* dereverberation
* declipping
* de-essing
* gentle EQ
* level adjustment

Processing is intentionally configurable. A clean original recording may be a better reference than an aggressively processed one.

### 3. Text to Speech with a Voice Variant

Once you have a voice variant, use it to generate new speech from text.

```text
Voice Variant + Text → Generated Speech
```

Generate multiple takes and adjust the generation parameters to find the delivery that works best for the character.

### 4. Design and Iterate

Voice creation is an iterative process.

Create alternate references, clean them differently, adjust generation settings, and compare the resulting takes.

```text
Reference
    ↓
Voice Variant
    ↓
Generate
    ↓
Compare
    ↓
Adjust
    ↓
Generate Again
```

The toolkit is designed to keep this process repeatable rather than treating voice cloning as a one-shot operation.

## Quick Start

### Requirements

* Linux recommended
* Python 3.12
* NVIDIA GPU with CUDA support recommended
* Qwen3-TTS model
* FFmpeg and/or SoX for audio processing

### Install

```bash
git clone https://github.com/SkipWestcott/character-voice.git
cd character-voice

cp config/machine.example.env config/local.env
./command/setup
```

Check the installation:

```bash
./command/status
```

### Create a Voice Variant

```bash
./command/reference build \
  --input <SAMPLE_AUDIO> \
  --output <REFERENCE_DIR> \
  --preset conservative
```

**Reference cleanup presets:**

* `direct` — Use the original audio without processing
* `minimal` — Apply basic cleanup only
* `conservative` — Apply gentle cleanup while preserving the original voice characteristics
* `aggressive` — Apply stronger restoration for heavily degraded recordings

Start with `direct` or `conservative`. Compare variants before choosing a reference.

```bash
# Original audio
./command/reference build \
  --input <SAMPLE_AUDIO> \
  --output <REFERENCE_DIR> \
  --preset direct

# Basic cleanup
./command/reference build \
  --input <SAMPLE_AUDIO> \
  --output <REFERENCE_DIR> \
  --preset minimal

# Gentle cleanup
./command/reference build \
  --input <SAMPLE_AUDIO> \
  --output <REFERENCE_DIR> \
  --preset conservative

# Strong restoration
./command/reference build \
  --input <SAMPLE_AUDIO> \
  --output <REFERENCE_DIR> \
  --preset aggressive
```

### Generate Speech

```bash
./command/run \
  --reference <REFERENCE_AUDIO> \
  "Synthetic example dialogue."
```

## How It Works

The project separates the reusable voice-generation tools from local machine configuration and private character data.

```text
Character Voice
├── Sample audio
│      ↓
├── Cleanup / restoration
│      ↓
├── Voice variant
│      ↓
└── Text-to-speech
       ↓
   Generated takes
```

Model files, source recordings, generated audio, and private character data are not part of the repository.

## Documentation

* [Installation](docs/installation.md)
* [Reference Pipeline](docs/reference-pipeline.md)
* [Audio Restoration](docs/restoration.md)
* [Voice Design](docs/voice-design.md)
* [Evaluation](docs/evaluation.md)
* [Architecture](docs/architecture.md)
* [Machine Configuration](docs/machines.md)
* [Privacy](docs/privacy.md)

## License

MIT
