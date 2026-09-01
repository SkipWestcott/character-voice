# Character Voice

A generic, local-first command and execution layer for character voice generation with Qwen3-TTS.

The package separates reusable execution logic from machine-specific configuration and private character data.

## Architecture

```text
Command
  ↓
Execute
  ↓
Qwen3-TTS Python environment
  ↓
Qwen3TTSModel
  ↓
reference audio + text + generation parameters
  ↓
WAV output
```

ComfyUI is optional. It may provide model, input, or output storage, but it is not required by the core TTS executor.

## Design principle

> The repository describes capabilities; configuration describes machines; private project data describes characters.

## Privacy

Do not commit:
- private reference recordings
- generated character audio
- real character names or dialogue
- local usernames, hostnames, IP addresses, or private URLs
- API keys, tokens, credentials, or secrets
- local model caches/checkpoints unless redistribution is explicitly permitted

See `docs/privacy.md` for the public/private boundary.

## Requirements

- Linux/macOS shell environment
- Python 3.10+ recommended
- NVIDIA CUDA is the primary acceleration target, but hardware detection is intended to be generic
- Qwen3-TTS installed in a dedicated Python environment

The package intentionally does not vendor the Qwen3-TTS model or Python environment.

## Quick start

Copy the example machine configuration:

```bash
cp config/machine.example.env config/local.env
```

Edit `config/local.env`, then:

```bash
./command/status
./command/run
```

The executor currently provides a conservative scaffold. Add model-specific generation settings to local configuration rather than hard-coding private project values into the repository.
