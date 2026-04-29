# Speech-to-Text Integration & Cleaning

## Objective

Convert raw screening voice input into clean, structured text for AI analysis.

## Integration approach

- A production system would connect a speech-to-text provider through an adapter layer.
- This repository includes a deterministic STT simulation and transcript normalization module for offline development.

## Cleaning behavior

- removes filler words
- restores punctuation
- normalizes case
- flags interrupted speech
- flags partial answers
- flags silence or empty responses

## Test coverage areas

- different accents through `accent_hint` metadata
- background noise through `noise_level`
- interruptions through `--` and `...`
- partial and silent answers

## STT accuracy report

Current repository status:

- functional simulation layer implemented
- transcript normalization module implemented
- formal benchmark dataset not yet added
- future report should compare provider confidence vs manual transcripts across accent/noise buckets

