# Public / Private Boundary

Character Voice is intended to distribute the reusable voice-creation workflow, not a private character project.

The repository should contain the mechanism and methodology.

Private recordings, character material, generated audio, and machine-specific data should remain outside the repository.

## Public

The following can be committed:

* command scripts
* execution scripts
* generic Qwen3-TTS integration
* audio-analysis utilities
* reference-preparation logic
* configuration templates
* installation instructions
* generic methodology
* synthetic example text
* documentation
* license

## Private

Keep the following outside the public repository:

* source voice recordings
* reference candidates containing private recordings
* generated private audio
* private dialogue
* character names and identifying information
* private prompts
* private transcripts when they contain sensitive material
* model weights
* local caches
* machine-specific configuration
* credentials and API tokens
* SSH keys or other authentication material
* private URLs

## Sanitize Before Committing

Replace private values with generic equivalents.

| Private value       | Public equivalent                                 |
| ------------------- | ------------------------------------------------- |
| Character name      | `Character_A`                                     |
| Private dialogue    | synthetic example text                            |
| Reference filename  | `character_a_reference.wav`                       |
| Absolute local path | `<PROJECT_ROOT>` / `<MODEL_DIR>` / `<OUTPUT_DIR>` |
| Username            | `<USER>`                                          |
| Hostname            | `<HOST>`                                          |
| IP address          | `<HOST_IP>`                                       |
| Private URL         | `<SERVICE_URL>`                                   |

Do not replace a private value only in documentation while leaving the same value in a script, configuration file, comment, example, test fixture, or generated artifact.

## Local Configuration

Machine-specific configuration belongs in:

```text id="x4v0pz"
config/local.env
```

This file is ignored by Git.

The repository should provide templates rather than real machine configuration.

For example:

```text id="p9j5ke"
config/defaults.env
config/machine.example.env
config/local.env       # private, ignored
```

## Audio Files

Audio files should not be committed by default.

The repository's ignore rules cover common generated and source formats such as:

```text id="w7q8zr"
*.wav
*.mp3
*.flac
*.ogg
*.webm
```

Local reference candidates and generated output should remain outside the repository.

## History Matters

Deleting a private file from the current working tree is not sufficient if it was previously committed.

Before publishing, inspect:

```bash id="v2h5rc"
git status
git diff
git ls-files
git log --all --stat
```

Search the repository for obvious private values as appropriate.

If sensitive material was committed previously, treat the Git history as compromised and remove it using an appropriate history-rewriting procedure before publication.

## Generated Data

Generated audio is experimental output, not source code.

Do not use generated audio to replace a private source recording in the repository simply because the generated result appears less identifiable.

Generated audio can still contain:

* recognizable speaker characteristics
* private dialogue
* character-specific material
* artifacts derived from private source material

Keep it private unless it has been deliberately created as a public demonstration artifact.

## Documentation Examples

Documentation should use synthetic examples:

```text id="q3s6yn"
This is a synthetic example sentence.
```

Do not use actual character dialogue merely because it makes an example sound more realistic.

Likewise, documentation should use generic paths:

```text id="r8c2wm"
/path/to/reference.wav
/path/to/qwen-tts-venv/bin/python
/path/to/Qwen3-TTS-12Hz-1.7B-Base
```

## Publication Checklist

Before making the repository public:

```text id="k6x1wv"
[ ] No source recordings are tracked
[ ] No generated private audio is tracked
[ ] No private dialogue is present
[ ] No private character names are present
[ ] No private transcripts are present
[ ] No machine-specific absolute paths remain
[ ] No usernames, hostnames, or IP addresses remain
[ ] No credentials or tokens remain
[ ] No private URLs remain
[ ] Model weights are not tracked
[ ] Local configuration is ignored
[ ] Git history has been reviewed
[ ] Documentation examples are synthetic
```

## Principle

The public repository should be sufficient to understand and reproduce the **method**, while revealing nothing unnecessary about the private voice project used to develop it.
