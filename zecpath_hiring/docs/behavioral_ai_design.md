# Behavioral AI Research & Design Document

## 1. Overview
The goal of this module is to interpret candidate behavior during video interviews using non-invasive observable signals. Instead of employing highly controversial "emotion recognition" AI—which suffers from severe racial, cultural, and neurodivergent bias—this system measures transient kinematic data (eye gaze coordinates, head pose) to derive objective behavioral indicators.

## 2. Measurable Indicators & Signal Mapping

### 2.1 Focus Level
**Definition:** The degree to which the candidate maintains attention on the interview environment (the screen/camera).
* **Raw Signals:** Eye gaze stability (X/Y coordinate deviation), Head Yaw/Pitch.
* **Mapping Logic:** 
  * If gaze coordinates remain within a 20-degree cone of the screen bounding box, focus is maintained.
  * Rapid gaze saccades outside the bounding box temporarily reduce the focus score.
  * Sustained off-screen looking triggers a distraction flag.

### 2.2 Distraction Frequency
**Definition:** The number of times the candidate's attention is broken by external stimuli.
* **Raw Signals:** Sudden, large-magnitude changes in head Yaw or Pitch, coupled with sustained gaze deviation.
* **Mapping Logic:**
  * Count the frequency of gaze deviation events exceeding 2.0 seconds.
  * Score is inversely proportional to frequency (more distractions = lower score).

### 2.3 Nervous Gestures
**Definition:** Involuntary, repetitive movements often associated with anxiety or stress.
* **Raw Signals:** High-frequency micro-movements in Head Yaw/Pitch/Roll, rapid blinking rate.
* **Mapping Logic:**
  * Use a sliding window to calculate variance in head posture.
  * If variance exhibits high-frequency jitter (rapid oscillating movements), flag as a nervous gesture.
  * Note: This metric is purely observational and does not penalize overall interview score; it serves as context for the recruiter (e.g., "Candidate exhibited signs of stress during the technical architecture question").

### 2.4 Engagement Level
**Definition:** The candidate's active participation and physical responsiveness during the interview.
* **Raw Signals:** Head nodding (Pitch oscillation matching conversational cadence), facial landmark bounding box stability (leaning in vs leaning back).
* **Mapping Logic:**
  * Positive correlation with steady, slow head nods during interviewer speech.
  * Forward lean (detected via bounding box expansion) indicates increased engagement.

## 3. Non-Invasive Scoring Approach (Ethics & Fairness)
> [!IMPORTANT]
> **Privacy First:** Raw video feeds are NEVER stored. The client-side application extracts transient numerical landmark coordinates (e.g., using MediaPipe) and streams only these numbers to the scoring engine.

> [!CAUTION]
> **Anti-Ableism Protocol:** Candidates with motor tics, strabismus, or neurodivergent traits (like avoiding eye contact while thinking) may trigger false positives for distraction or nervousness. To mitigate this:
> 1. The behavioral score is **never** a hard filter. It only contributes a maximum of 5% to the final aggregate hiring fit score.
> 2. Prolonged "looking away" while the candidate is actively speaking (detected via audio analysis) is classified as "cognitive processing" rather than distraction.

## 4. Signal-to-Score Architecture
The system utilizes a Time-Series Aggregation approach:
1. **Frame-level Ingestion:** 30fps coordinate data is ingested.
2. **Windowing:** Data is aggregated into 5-second overlapping windows to calculate moving averages and variances.
3. **Indicator Calculation:** The mapping logic (defined in section 2) is applied to the windowed data.
4. **Session Rollup:** At the end of the interview, the time-series indicators are averaged, and frequency events are counted to produce a final 0-100 score for Focus, Engagement, and Composure.
