# Installation

1. Clone the repository.
2. Create or identify a dedicated Python environment for Qwen3-TTS.
3. Install the Qwen3-TTS package and its runtime dependencies according to its upstream documentation.
4. Copy `config/machine.example.env` to `config/local.env`.
5. Set the local Python executable, model path, private reference path, and output directory.
6. Run:

```bash
./command/status
```

Then test the executor with synthetic text:

```bash
./command/run "This is a synthetic example."
```

Do not place private reference audio in the repository.
