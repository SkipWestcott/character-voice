# Machine Configuration

The code should not contain machine-specific assumptions.

Configure locally:

- Python executable
- model directory
- reference audio location
- output directory
- device selection
- dtype or performance settings

Hardware detection should report what is available rather than assume a specific GPU model.

The repository is designed around NVIDIA/CUDA as a primary acceleration path while remaining explicit about runtime capabilities.
