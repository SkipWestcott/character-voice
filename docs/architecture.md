# Architecture

## Layers

### Command

Human-facing entry points.

Examples:

```text
./command/run
./command/status
./command/setup
```

### Execute

Machine-facing execution logic.

Responsibilities:
- select the configured Python environment
- inspect hardware/runtime availability
- invoke Qwen3-TTS
- manage arguments and output paths

### Qwen3-TTS

The external Python package provides the model implementation.

The public package does not redistribute model weights.

### Configuration

Machine-specific paths and runtime choices belong in ignored local configuration.

### Private character data

Reference recordings, character names, dialogue, and generated audio stay outside the public repository.

## Separation rule

A different machine should require configuration changes, not source-code edits.
