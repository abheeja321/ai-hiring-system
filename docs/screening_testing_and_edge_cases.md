# Screening System Testing, Optimization, and Edge Cases

## Testing focus

- simulated AI screening calls
- comparison-ready structured outputs for human review
- threshold tuning for fewer false rejections
- intent and follow-up logic verification

## Optimization notes

- confidence score now contributes to final screening score
- missing-information follow-ups reduce premature rejection risk
- conversation flow includes retry and clarification before failure

## Edge cases handled

- poor audio
- language mixing
- missing answers
- background noise
- silence
- off-topic responses
- contradictions

## Fallback framework

- retry question
- request quieter environment
- ask for one-language response
- escalate to manual recruiter follow-up

