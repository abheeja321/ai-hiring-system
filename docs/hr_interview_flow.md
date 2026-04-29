# HR Interview State & Flow Design

## Interview State Structure

The interview session state is a living JSON document (or database record) that tracks the candidate's progress.

```json
{
  "session_id": "uuid-1234",
  "candidate_id": 50,
  "job_id": 20,
  "current_phase": "CORE_HR",
  "history": [
    {
      "turn": 1,
      "speaker": "AI",
      "question_id": "intro_01",
      "category": "Self-introduction",
      "content": "Hi Jane, it's great to meet you. To start off, could you walk me through your background?"
    },
    {
      "turn": 2,
      "speaker": "Candidate",
      "content": "Sure, I have been working as a backend engineer for 5 years..."
    }
  ],
  "follow_up_eligibility": {
    "can_follow_up": true,
    "max_follow_ups_per_question": 1,
    "current_follow_up_count": 0
  },
  "metrics": {
    "total_duration_seconds": 120,
    "questions_asked": 1
  }
}
```

## Conversation Phases

The Flow Controller dictates transitions between four primary phases:

### Phase 1: Introduction
- **Goal**: Welcome the candidate, set expectations, and warm up.
- **Actions**:
  - Greet the candidate by name.
  - Ask a high-level `Self-introduction` question.
- **Transition**: Moves to Phase 2 after the candidate provides their introduction.

### Phase 2: Core HR Questions
- **Goal**: Evaluate standard behavioral and cultural vectors.
- **Actions**:
  - Ask 1 question from `Career journey`.
  - Ask 1 question from `Strengths & weaknesses`.
  - Ask 1 question from `Teamwork & culture fit`.
- **Logic**: For each question, the `Response Evaluator` determines if a follow-up is needed (if `follow_up_eligibility` permits).
- **Transition**: Moves to Phase 3 once core questions are exhausted.

### Phase 3: Role-based Evaluation
- **Goal**: Contextualize behavior within the specific job function.
- **Actions**:
  - Ask 1-2 questions tailored to the intersection of their experience level (Fresher/Exp) and role type (Tech/Non-Tech).
- **Transition**: Moves to Phase 4.

### Phase 4: Closing
- **Goal**: Wrap up the interview gracefully.
- **Actions**:
  - Ask about `Career goals` or `Availability & commitment`.
  - Allow the candidate to ask any questions they have.
  - Close the session and trigger the final scoring pipeline.
