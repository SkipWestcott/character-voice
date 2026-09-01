# Public / Private Boundary

This repository is intended to explain and distribute the reusable mechanism, not a private character project.

## Public

- command/execution architecture
- generic Qwen3-TTS integration
- hardware detection
- configuration examples
- installation instructions
- generic methodology
- synthetic example text

## Sanitize

Replace private values with generic placeholders:

| Private value | Public equivalent |
|---|---|
| character name | `Character_A` |
| private dialogue | synthetic example text |
| reference filename | `character_a_reference.wav` |
| absolute local path | `<PROJECT_ROOT>` / `<MODEL_DIR>` / `<OUTPUT_DIR>` |
| username | `<USER>` |
| hostname | `<HOST>` |
| IP address | `<HOST_IP>` |
| private URL | `<SERVICE_URL>` |

## Never commit

- source recordings
- generated private audio
- private lore
- private prompts
- credentials and tokens
- SSH material
- local environment files
- private model/checkpoint data
- caches and runtime logs

Audit both the working tree and Git history before publishing.
