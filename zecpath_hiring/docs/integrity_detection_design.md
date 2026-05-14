# Integrity & Malpractice Detection Design

## 1. Overview
The Integrity & Malpractice Detection module is designed to ensure the authenticity of the candidate's interview performance. It monitors for external assistance, unauthorized material usage, and screen-sharing malpractice.

## 2. Malpractice Signals

### 2.1 Browser/Device Signals
- **Tab Switching Frequency:** Monitored via the browser's `visibilitychange` or `blur`/`focus` events. Indicates the candidate is navigating away from the interview interface (potentially to search for answers).
- **Loss of Screen Focus:** The interview window losing focus entirely (e.g., clicking on a dual-monitor setup or opening another local application).

### 2.2 Audio/Visual Signals
- **External Voice Detection:** Monitored via voice activity detection (VAD) and speaker diarization. Detects if a secondary voice is present in the room prompting the candidate.
- **Repeated Looking Away:** Monitored via the visual behavior engine. Unlike occasional distraction, *repeated* and *rhythmic* looking away off-screen (especially right after a question is asked) strongly indicates reading from notes or a secondary screen.

## 3. Detection Logic & Pattern Recognition

The system uses a combination of hard thresholds and pattern recognition.

### Threshold-Based Flags
- **Tab Switches:** > 2 times triggers a warning. > 5 times triggers a critical flag.
- **Off-Screen Duration:** > 15 seconds continuously triggers a warning.
- **External Voice:** > 3 instances of a distinct secondary voice speaking while the interviewer is quiet.

### Pattern Recognition (Composite Risks)
The most accurate malpractice detection comes from combining signals:
1. **The "Search & Read" Pattern:** The system detects a *Tab Switch / Focus Loss* immediately followed by a prolonged *Looking Away* visual signal, ending with a highly fluent technical answer.
2. **The "Prompter" Pattern:** The system detects an *External Voice* whisper, followed by the candidate repeating the phrase or suddenly changing their answer trajectory.
3. **The "Dual Monitor" Pattern:** The candidate maintains perfect screen focus (no tab switches), but visual signals show their gaze locked steadily at a 45-degree angle (reading a secondary monitor) rather than at the camera/primary screen.

## 4. Warning & Flagging System

### Real-Time Alerts (Candidate Facing)
- **Soft Warnings:** The UI will display a gentle toast notification if a minor threshold is breached (e.g., "Please keep the interview tab focused." or "We detect high background noise, please ensure you are in a quiet room."). This deters casual malpractice.
- **Auto-Pause:** If critical thresholds are breached rapidly (e.g., 5 tab switches in 1 minute), the AI interviewer may pause the interview and state: "It seems you might be navigating away from the interview. Please ensure you stay on this screen to continue."

### Interview Risk Tagging (Recruiter Facing)
The system does *not* automatically disqualify a candidate. Instead, it generates an `Integrity Confidence Score` and attaches specific Risk Tags to the final report:
- `[RISK: HIGH] Multiple tab switches detected during technical questions.`
- `[RISK: CRITICAL] Secondary voice detected prompting answers.`
- `[RISK: MEDIUM] Frequent gaze deviation consistent with reading external notes.`

## 5. Integration with Behavioral Signals
The Integrity module imports data from the `BehavioralIndicator` (from `ai/behavior_ai/video_evaluator.py`). 
- If the Behavioral AI flags high "distraction," the Integrity AI checks if that distraction correlates with tab switches or external voices. 
- If distraction is high but no tab switches or voices are present, it is classified as *benign distraction* (e.g., thinking, nervousness, or a pet in the room) rather than malpractice.
