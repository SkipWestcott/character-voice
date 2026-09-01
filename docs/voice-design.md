# Voice Design Methodology

A reusable voice-generation system should separate:

1. **Reference selection** — choose a clean representative recording.
2. **Reference preparation** — normalize or level-adjust the reference when testing how input level affects cloning.
3. **Prompt construction** — use the Qwen3-TTS voice-clone prompt mechanism.
4. **Generation** — synthesize the same controlled text across parameter/reference variants.
5. **Evaluation** — compare clarity, identity consistency, delivery, artifacts, and generalization.
6. **Selection** — retain the best-performing reference and settings in private project configuration.

Keep actual character material outside the public repository.
