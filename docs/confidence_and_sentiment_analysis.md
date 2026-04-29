# Confidence & Sentiment Signal Analysis

## Objective

Assess communication quality and behavioral indicators from screening transcripts.

## Signals captured

- hesitation patterns
- response length
- response pace
- positive or negative sentiment
- uncertainty cues
- possible contradictions
- communication strength

## Output structure

```json
{
  "hesitation_patterns": 1,
  "response_length_words": 14,
  "response_pace_wpm": 126.0,
  "sentiment_score": 74,
  "sentiment_label": "positive",
  "uncertainty_score": 82,
  "contradictions": [],
  "confidence_score": 84,
  "communication_strength": "strong",
  "behavioral_indicators": {
    "confidence_band": "high",
    "sentiment_band": "positive",
    "hesitation_risk": "low",
    "contradiction_risk": "low",
    "missing_data_risk": "low"
  }
}
```

