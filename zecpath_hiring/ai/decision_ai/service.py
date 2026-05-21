from typing import Dict, Any, List

class DecisionEngine:
    def __init__(self):
        self.weights = {
            "ats": 0.30,
            "screening": 0.20,
            "interview": 0.35,
            "behavior": 0.15
        }
    
    def evaluate(self, ats: Dict[str, Any], screening: Dict[str, Any], interview: Dict[str, Any], behavior: Dict[str, Any], integrity: Dict[str, Any] = None) -> Dict[str, Any]:
        explanation: List[str] = []
        confidence_penalties = 0.0
        has_error = False
        
        def safe_float(val, module_name):
            nonlocal has_error
            if val == "ERROR" or val == "UNKNOWN":
                has_error = True
                explanation.append(f"[SYSTEM] {module_name} module failed. Defaulting to HOLD_REVIEW.")
                return 0.0
            try:
                return float(val)
            except (ValueError, TypeError):
                has_error = True
                explanation.append(f"[SYSTEM] {module_name} score unparseable. Defaulting to HOLD_REVIEW.")
                return 0.0

        # Base scores
        ats_score = safe_float(ats.get("final_score", 0), "ATS")
        screening_score = safe_float(screening.get("screening_score", 0), "Screening")
        interview_score = safe_float(interview.get("interview_score", 0), "Interview")
        behavior_score = safe_float(behavior.get("behavior_score", 0), "Behavior")
        
        # Risk levels
        integrity_risk = "LOW"
        if integrity:
            integrity_risk = integrity.get("risk_level", "LOW")
            
        if integrity_risk == "ERROR":
            integrity_risk = "LOW"
            has_error = True
            explanation.append("[SYSTEM] Integrity check failed. Defaulting to HOLD_REVIEW.")
        elif integrity_risk == "UNKNOWN":
            integrity_risk = "LOW"
            confidence_penalties += 10.0
            explanation.append("[CONFIDENCE] Integrity risk was UNKNOWN, defaulting to LOW but applying a penalty.")
        
        # --- RULE-BASED EVALUATION (Hard Limits) ---
        hard_reject = False
        
        if integrity_risk in ["HIGH", "CRITICAL"]:
            hard_reject = True
            explanation.append(f"[RULE] Candidate rejected due to {integrity_risk} integrity risk.")
        
        if behavior_score < 35 and behavior.get("behavior_score") != "ERROR":
            hard_reject = True
            explanation.append("[RULE] Candidate rejected due to extremely low behavior score (<35).")
            
        if interview_score < 55 and interview.get("interview_score") != "ERROR":
            hard_reject = True
            explanation.append("[RULE] Candidate rejected due to failing technical interview threshold (<55).")

        # --- SCORE-BASED EVALUATION ---
        final_score = round(
            (ats_score * self.weights["ats"])
            + (screening_score * self.weights["screening"])
            + (interview_score * self.weights["interview"])
            + (behavior_score * self.weights["behavior"]),
            2
        )
        
        # Determine Decision
        if has_error:
            decision = "HOLD_REVIEW"
            confidence_penalties += 50.0
        elif hard_reject:
            decision = "REJECTED"
        else:
            if final_score >= 80 and integrity_risk == "LOW":
                decision = "SELECTED"
                explanation.append(f"Candidate passed all thresholds and achieved a high composite score ({final_score}).")
            elif final_score >= 60:
                decision = "HOLD_REVIEW"
                explanation.append(f"Candidate achieved a moderate score ({final_score}). Requires manual review.")
                if integrity_risk == "MEDIUM":
                    explanation.append("Medium integrity risk detected, suggesting a hold/review status.")
            else:
                decision = "REJECTED"
                explanation.append(f"Candidate did not meet the minimum composite score threshold of 65 (Score: {final_score}).")

        # --- CONFIDENCE SCORE CALCULATION ---
        # Confidence is higher if scores are consistent (low variance) and far from thresholds.
        scores = [ats_score, screening_score, interview_score, behavior_score]
        mean_score = sum(scores) / 4
        variance = sum((s - mean_score) ** 2 for s in scores) / 4
        std_dev = variance ** 0.5
        
        # Penalty for high variance
        if std_dev > 15 and not has_error:
            confidence_penalties += 10
            explanation.append("[CONFIDENCE] Moderate penalty due to inconsistent scores across stages.")
            
        # Penalty for borderline decisions
        if 78 <= final_score < 82 and decision != "REJECTED":
            confidence_penalties += 10
            explanation.append("[CONFIDENCE] Borderline score around the SELECTED threshold reduces confidence slightly.")
        elif 63 <= final_score < 67 and not hard_reject:
            confidence_penalties += 10
            explanation.append("[CONFIDENCE] Borderline score around the HOLD/REJECT threshold reduces confidence.")
            
        # Missing data penalty
        if not integrity and not has_error:
            confidence_penalties += 20
            explanation.append("[CONFIDENCE] Missing integrity data reduces overall decision confidence.")
            
        confidence_score = max(0.0, round(100.0 - confidence_penalties, 2))

        return {
            "final_score": final_score,
            "decision": decision,
            "confidence_score": confidence_score,
            "risk_level": integrity_risk,
            "explanation": " ".join(explanation),
            "offer_automation_ready": decision == "SELECTED" and confidence_score >= 90
        }

def make_final_decision(ats: dict, screening: dict, interview: dict, behavior: dict, integrity: dict = None) -> dict:
    engine = DecisionEngine()
    return engine.evaluate(ats, screening, interview, behavior, integrity)
