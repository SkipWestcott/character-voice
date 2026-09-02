# Voice Design

Voice Design creates a new voice from a natural-language description rather than from a reference recording.

The workflow is:

    Voice Description
           |
           v
    VoiceDesign Model
           |
           v
    Generated Take
           |
           v
    Evaluation
           |
           v
    Revise Description
           |
           v
    Generate Again

## Design vs Clone

Design and Clone are separate workflows.

| Workflow | Input | Purpose |
|---|---|---|
| Design | Voice description + text | Create a voice concept |
| Clone | Reference audio + transcript + text | Reproduce a recorded voice |

Design does not require reference audio or a transcript.

Clone does not use the VoiceDesign model.

Do not route Design through the Clone executor.

## Voice Descriptions

A Voice Design description should describe the characteristics you want the generated voice to have.

Useful dimensions include:

- apparent age
- gender presentation
- vocal register
- vocal weight
- vocal texture
- resonance
- articulation
- speaking energy
- emotional character
- authority or softness
- pacing
- conversational or formal delivery

A description can combine several dimensions.

For example:

    A calm, articulate middle-aged male voice with a warm low register and restrained authority.

The description should focus on the desired sound rather than on implementation details.

## Delivery vs Identity

Evaluate two different properties independently.

### Identity

Identity concerns whether the generated voice feels like a distinct and coherent character.

Consider:

- Is the voice recognizable across takes?
- Does it have a distinctive character?
- Does the vocal texture remain coherent?
- Does it fit the intended character concept?

### Delivery

Delivery concerns how the voice performs the supplied text.

Consider:

- pacing
- emphasis
- pauses
- emotional intensity
- articulation
- conversational naturalness

A voice can have strong identity but poor delivery, or strong delivery without a sufficiently distinctive identity.

Do not change the voice description when the actual problem is only delivery.

## Iteration

Voice Design is an exploratory process.

A useful loop is:

    Description
         |
         v
    Generate
         |
         v
    Listen
         |
         v
    Identify the problem
         |
         +------> Identity problem
         |              |
         |              v
         |       Revise voice description
         |
         +------> Delivery problem
                        |
                        v
                 Revise generation approach
                        |
                        v
                     Generate

Change one meaningful variable at a time when evaluating a voice.

This makes it easier to determine which change produced an improvement.

## Multiple Takes

Voice Design generation can vary between takes.

When evaluating a new voice concept, generate multiple takes rather than deciding from a single sample.

A single take may have:

- unusually good or bad pacing
- unusual emphasis
- an atypical emotional delivery
- small variations in vocal character

The goal is to identify a stable and useful voice concept rather than selecting the best isolated performance.

## Command

The Design command is:

    ./command/design \
      --instruct "A calm, articulate middle-aged male voice with a warm low register and restrained authority." \
      --text "Hello. This is a test."

The output can be specified explicitly:

    ./command/design \
      --instruct "A calm, articulate middle-aged male voice with a warm low register and restrained authority." \
      --text "Hello. This is a test." \
      --output output/example.wav

An optional language can also be supplied:

    ./command/design \
      --instruct "A calm, articulate middle-aged male voice with a warm low register and restrained authority." \
      --text "Hello. This is a test." \
      --language English

## Configuration

Design uses its own model configuration:

    QWEN_TTS_DESIGN_MODEL

The model should point to the Qwen3-TTS VoiceDesign checkpoint.

Design does not depend on:

    REFERENCE_AUDIO
    REFERENCE_TEXT

This allows the Design workflow to operate independently of the reference pipeline.

## Evaluation

When evaluating a Design take, record observations separately for identity and delivery.

A simple evaluation can include:

    Identity:
    - distinctive
    - coherent
    - appropriate character

    Delivery:
    - natural
    - appropriate pacing
    - appropriate emphasis
    - appropriate emotional intensity

Avoid changing several variables simultaneously when possible.

## Design Output

Design produces generated speech.

It is not automatically a reference recording.

A generated Design take may later become useful as reference material, but converting Design output into a formal Clone reference is a separate workflow and is not currently automated by this project.

## Privacy

Voice descriptions, dialogue, generated audio, and other character-specific material may be private.

Do not place private character descriptions, dialogue, generated takes, or reference recordings in the public repository.

Machine-specific paths belong in:

    config/local.env

which is ignored by Git.
