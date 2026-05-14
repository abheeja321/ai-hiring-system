import math
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class VisualSignalFrame(BaseModel):
    """
    Represents a single frame of visual coordinate data.
    These are numerical coordinates, NOT image data, ensuring privacy.
    """
    timestamp_ms: float
    gaze_x: float = Field(description="Normalized gaze X coordinate (-1.0 to 1.0, 0 is center)")
    gaze_y: float = Field(description="Normalized gaze Y coordinate (-1.0 to 1.0, 0 is center)")
    head_yaw: float = Field(description="Head rotation left/right in degrees")
    head_pitch: float = Field(description="Head rotation up/down in degrees")
    head_roll: float = Field(description="Head tilt left/right in degrees")
    is_speaking: bool = Field(default=False, description="True if audio indicates candidate is speaking")


class BehavioralIndicator(BaseModel):
    focus_level: float = Field(ge=0.0, le=100.0)
    distraction_frequency: int = Field(ge=0)
    nervous_gestures_detected: int = Field(ge=0)
    engagement_level: float = Field(ge=0.0, le=100.0)
    explanation: List[str] = Field(default_factory=list)


class VideoBehaviorEvaluator:
    """
    Analyzes visual signal time-series data to extract behavioral indicators.
    Follows a non-invasive, privacy-first approach.
    """

    def __init__(self):
        # Thresholds
        self.GAZE_TOLERANCE = 0.4  # Max allowed gaze deviation from center before it's considered "looking away"
        self.HEAD_YAW_TOLERANCE = 25.0  # Degrees
        self.JITTER_VARIANCE_THRESHOLD = 15.0  # Threshold for rapid movement variance

    def evaluate_session(self, frames: List[VisualSignalFrame]) -> BehavioralIndicator:
        """
        Processes a full session's worth of visual frames to compute final behavioral scores.
        """
        if not frames:
            return BehavioralIndicator(
                focus_level=100.0,
                distraction_frequency=0,
                nervous_gestures_detected=0,
                engagement_level=100.0,
                explanation=["No visual data provided. Defaulting to neutral positive baseline."]
            )

        # Sort frames chronologically
        frames = sorted(frames, key=lambda f: f.timestamp_ms)
        
        # Calculations
        focus_score, distractions = self._calculate_focus_and_distractions(frames)
        nervous_gestures = self._detect_nervous_gestures(frames)
        engagement_score = self._calculate_engagement(frames)
        
        explanations = []
        if distractions > 0:
            explanations.append(f"Detected {distractions} instances of prolonged distraction.")
        if nervous_gestures > 0:
            explanations.append(f"Observed {nervous_gestures} instances of rapid, repetitive head movements (potential stress indicators).")
        if engagement_score > 80:
            explanations.append("High engagement detected via stable head posture and attention.")
        
        # Apply anti-ableism buffer: Ensure no score drops below 40 due to visual alone
        focus_score = max(40.0, focus_score)
        engagement_score = max(40.0, engagement_score)
        
        return BehavioralIndicator(
            focus_level=round(focus_score, 2),
            distraction_frequency=distractions,
            nervous_gestures_detected=nervous_gestures,
            engagement_level=round(engagement_score, 2),
            explanation=explanations
        )

    def _calculate_focus_and_distractions(self, frames: List[VisualSignalFrame]) -> tuple[float, int]:
        distractions = 0
        off_screen_duration_ms = 0.0
        consecutive_off_screen = 0
        
        for i in range(1, len(frames)):
            prev_f = frames[i-1]
            curr_f = frames[i]
            dt = curr_f.timestamp_ms - prev_f.timestamp_ms
            
            # Check if looking away (Gaze or Head Yaw heavily deviated)
            is_looking_away = (
                abs(curr_f.gaze_x) > self.GAZE_TOLERANCE or 
                abs(curr_f.head_yaw) > self.HEAD_YAW_TOLERANCE
            )
            
            # Anti-ableism override: If they are speaking, looking away is often cognitive processing, not distraction
            if is_looking_away and not curr_f.is_speaking:
                consecutive_off_screen += dt
                off_screen_duration_ms += dt
            else:
                if consecutive_off_screen > 2000.0:  # 2 seconds continuous looking away while not speaking
                    distractions += 1
                consecutive_off_screen = 0
                
        # If ended while looking away
        if consecutive_off_screen > 2000.0:
            distractions += 1
            
        total_duration_ms = frames[-1].timestamp_ms - frames[0].timestamp_ms
        if total_duration_ms <= 0:
            return 100.0, 0
            
        # Focus score calculation
        off_screen_ratio = off_screen_duration_ms / total_duration_ms
        focus_score = 100.0 - (off_screen_ratio * 100.0)
        
        # Penalize for each major distraction event
        focus_score -= (distractions * 5.0)
        
        return max(0.0, focus_score), distractions

    def _detect_nervous_gestures(self, frames: List[VisualSignalFrame]) -> int:
        """
        Detects jitter/nervousness via sliding window variance analysis on head rotation.
        """
        if len(frames) < 10:
            return 0
            
        nervous_events = 0
        window_size = 30 # roughly 1 second at 30fps
        
        for i in range(0, len(frames) - window_size, window_size // 2):
            window = frames[i:i+window_size]
            yaw_variance = self._calculate_variance([f.head_yaw for f in window])
            pitch_variance = self._calculate_variance([f.head_pitch for f in window])
            
            # If variance is very high in a short window, it indicates rapid shaking/jitter
            if yaw_variance > self.JITTER_VARIANCE_THRESHOLD or pitch_variance > self.JITTER_VARIANCE_THRESHOLD:
                nervous_events += 1
                
        return nervous_events

    def _calculate_engagement(self, frames: List[VisualSignalFrame]) -> float:
        """
        Engagement is based on minimal prolonged stillness combined with focus.
        (A perfectly still candidate might be disengaged or frozen).
        """
        if not frames:
            return 100.0
            
        pitch_variance = self._calculate_variance([f.head_pitch for f in frames])
        
        # Some movement (nodding, natural shifts) indicates active listening/engagement.
        # Zero movement might mean disengagement.
        engagement = 80.0
        if pitch_variance > 2.0 and pitch_variance < 15.0:
            # Optimal natural movement range
            engagement += 20.0
        elif pitch_variance <= 2.0:
            # Too still
            engagement -= 10.0
            
        return min(100.0, max(0.0, engagement))

    @staticmethod
    def _calculate_variance(values: List[float]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
