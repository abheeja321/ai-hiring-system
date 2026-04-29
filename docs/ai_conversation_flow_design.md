# AI Conversation Flow Design

## Conversation state machine

- `START`
- `ASK_QUESTION`
- `WAIT_FOR_ANSWER`
- `CLARIFY`
- `RETRY`
- `FOLLOW_UP`
- `COMPLETE`
- `FAIL_SAFE`

## Dynamic call logic

- silence triggers retry
- confusion or off-topic answers trigger clarification
- missing details trigger follow-up prompts
- repeated failure triggers safe fallback to recruiter review

## Error-handling behavior

- polite retry messages
- fallback clarification prompts
- retry limit before fail-safe
- manual recruiter handoff when audio quality is too poor

