from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Simulating import from behavior module
from zecpath_hiring.ai.behavior_ai.video_evaluator import BehavioralIndicator


class IntegritySignalFrame(BaseModel):
    """
    Represents raw integrity signals collected during a specific time window or event.
    """
    timestamp_ms: float
    tab_switches: int = Field(default=0, description="Number of times the browser tab lost focus")
    screen_focus_lost: bool = Field(default=False, description="Whether the entire window lost focus")
    external_voices_detected: int = Field(default=0, description="Count of distinct secondary voice events")
    is_answering_question: bool = Field(default=False, description="Whether these signals happened while the candidate was answering")


class IntegrityReport(BaseModel):
    integrity_score: float = Field(ge=0.0, le=100.0, description="100 is perfect integrity, 0 is definite malpractice")
    risk_level: str = Field(description="LOW, MEDIUM, HIGH, or CRITICAL")
    flags: List[str] = Field(default_factory=list)
    real_time_warnings_triggered: List[str] = Field(default_factory=list)


class MalpracticeEvaluator:
    """
    Evaluates raw integrity signals and behavioral indicators to detect potential malpractice.
    """

    def __init__(self):
        # Thresholds
        self.TAB_SWITCH_WARNING_THRESHOLD = 2
        self.TAB_SWITCH_CRITICAL_THRESHOLD = 5
        self.EXTERNAL_VOICE_THRESHOLD = 2

    def evaluate_session(self, signals: List[IntegritySignalFrame], behavior: Optional[BehavioralIndicator] = None, behavior_text: str = "") -> IntegrityReport:
        """
        Analyzes a session's worth of signals to generate a final integrity report.
        """
        if not signals and not behavior and not behavior_text:
            return IntegrityReport(
                integrity_score=100.0,
                risk_level="LOW",
                flags=["No integrity signals collected (assuming safe environment)."],
                real_time_warnings_triggered=[]
            )

        total_tab_switches = sum(s.tab_switches for s in signals)
        total_focus_loss = sum(1 for s in signals if s.screen_focus_lost)
        total_external_voices = sum(s.external_voices_detected for s in signals)
        
        # Calculate base score
        score = 100.0
        flags = []
        warnings = []
        
        # 1. Evaluate Tab Switches
        if total_tab_switches > self.TAB_SWITCH_CRITICAL_THRESHOLD:
            score -= 40.0
            flags.append(f"[RISK: CRITICAL] {total_tab_switches} tab switches detected.")
            warnings.append("Critical Warning: Excessive tab switching.")
        elif total_tab_switches > self.TAB_SWITCH_WARNING_THRESHOLD:
            score -= 15.0
            flags.append(f"[RISK: MEDIUM] {total_tab_switches} tab switches detected.")
            warnings.append("Warning: Please keep the interview tab focused.")
            
        # 2. Evaluate Screen Focus
        if total_focus_loss > 3:
            score -= 20.0
            flags.append(f"[RISK: HIGH] Screen focus lost {total_focus_loss} times.")
            
        # 3. Evaluate External Voices
        if total_external_voices >= self.EXTERNAL_VOICE_THRESHOLD:
            score -= 50.0
            flags.append(f"[RISK: CRITICAL] Secondary external voice detected {total_external_voices} times.")
            warnings.append("Warning: Background voices detected. Ensure you are alone.")
            
        # 4. Pattern Recognition: Integration with Behavior
        if behavior:
            # Pattern: "Search & Read" - High tab switches + High visual distraction
            if total_tab_switches >= 2 and behavior.distraction_frequency >= 3:
                score -= 30.0
                flags.append("[RISK: HIGH] Composite Pattern: Frequent tab switches correlated with looking away (Search & Read).")
                
            # Pattern: "Dual Monitor Reading" - No tab switches but extremely high visual distraction
            if total_tab_switches == 0 and behavior.distraction_frequency >= 5 and behavior.focus_level < 50.0:
                score -= 25.0
                flags.append("[RISK: MEDIUM] Composite Pattern: High visual deviation without tab switching (Possible secondary monitor).")

        # 5. Semantic NLP Analysis for Behavioral Anomalies
        if behavior_text:
            text_lower = behavior_text.lower()
            critical_flags = ["refused", "uncooperative", "cheating", "fraud", "fake"]
            medium_flags = ["evasive", "inconsistent", "nervous", "suspicious"]
            
            if any(f in text_lower for f in critical_flags):
                score -= 60.0
                flags.append("[RISK: CRITICAL] Behavioral text indicates severe non-compliance or refusal.")
            elif any(f in text_lower for f in medium_flags):
                score -= 25.0
                flags.append("[RISK: MEDIUM] Behavioral text indicates evasive or inconsistent responses.")

        # Cap score
        final_score = max(0.0, min(100.0, score))
        
        # Determine Risk Level
        if final_score < 40.0:
            risk_level = "CRITICAL"
        elif final_score < 70.0:
            risk_level = "HIGH"
        elif final_score < 90.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        if risk_level == "LOW" and not flags:
            flags.append("No malpractice signals detected. Integrity confirmed.")

        return IntegrityReport(
            integrity_score=round(final_score, 2),
            risk_level=risk_level,
            flags=flags,
            real_time_warnings_triggered=warnings
        )
