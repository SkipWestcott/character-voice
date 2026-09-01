# Reference Evaluation

Reference selection should be evaluated through the actual TTS task, not waveform appearance alone.

For each candidate, generate the same small set of synthetic test phrases and score independently:

- **Speaker similarity:** Does the generated voice sound like the intended speaker/character?
- **Content consistency:** Is the requested text rendered clearly and faithfully?
- **Audio quality:** Are there clicks, pumping, metallic artifacts, excessive noise, or bandwidth problems?

Use repeated takes when the TTS system is stochastic. Record the candidate name and generation settings with each result.

A candidate that wins on one dimension may lose on another. The purpose of the pipeline is to make those tradeoffs visible rather than hiding them behind a single “enhanced” file.
