from datetime import UTC, datetime, timedelta
from typing import Any, Dict, List


PROTECTED_SIGNAL_KEYS = {
    "age",
    "date_of_birth",
    "dob",
    "gender",
    "sex",
    "race",
    "ethnicity",
    "religion",
    "caste",
    "marital_status",
    "pregnancy",
    "disability",
    "nationality",
    "citizenship",
    "photo",
    "profile_photo",
}


class EthicsComplianceReviewer:
    """
    Builds ethics and compliance guardrails for HR AI outputs.
    """

    DEFAULT_RETENTION_DAYS = {
        "raw_resume": 180,
        "transcript": 90,
        "scorecard": 365,
        "audit_log": 730,
        "training_snapshot": 365,
    }

    REQUIRED_CONSENT_FLAGS = {
        "ai_screening_consent",
        "transcript_processing_consent",
        "automated_scoring_notice",
        "data_retention_notice",
    }

    def validate_consent(self, consent_payload: Dict[str, Any]) -> Dict[str, Any]:
        missing = sorted(flag for flag in self.REQUIRED_CONSENT_FLAGS if not consent_payload.get(flag))
        return {
            "consent_valid": not missing,
            "missing_consent": missing,
            "required_consent": sorted(self.REQUIRED_CONSENT_FLAGS),
            "notes": "Candidate consent must be captured before AI screening, transcript processing, or automated scoring.",
        }

    def remove_demographic_bias_signals(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sanitized, removed = self._sanitize_value(payload)
        return {
            "sanitized_payload": sanitized,
            "removed_protected_signals": sorted(set(removed)),
        }

    def review_scoring_fairness(self, score_object: Dict[str, Any]) -> Dict[str, Any]:
        input_scores = score_object.get("input_scores", {})
        risk_flags = []
        score_values = [float(value) for value in input_scores.values() if isinstance(value, (int, float))]
        if score_values and max(score_values) - min(score_values) >= 30:
            risk_flags.append("Large cross-round score spread requires human review.")
        if score_object.get("risk_flags"):
            risk_flags.extend(score_object["risk_flags"])

        fairness_notes = [
            "Do not use protected demographic attributes in scoring.",
            "Use job-related criteria only: skills, experience relevance, answer quality, communication clarity, and role alignment.",
            "Route low-confidence or inconsistent scores to manual recruiter review.",
            "Keep candidate-facing explanations concise and tied to assessed job criteria.",
        ]
        return {
            "fairness_review_status": "review_required" if risk_flags else "pass",
            "risk_flags": list(dict.fromkeys(risk_flags)),
            "fairness_notes": fairness_notes,
        }

    def build_explainability_notes(self, score_object: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "explainability_available": True,
            "candidate_summary": (
                "The hiring-fit score combines resume/job match, screening answer quality, and HR interview performance."
            ),
            "recruiter_summary": {
                "input_scores": score_object.get("input_scores", {}),
                "applied_weights": score_object.get("applied_weights", {}),
                "weighted_contributions": score_object.get("weighted_contributions", {}),
                "decision_band": score_object.get("decision_band"),
                "recommendation": score_object.get("recommendation"),
            },
            "limitations": [
                "AI score is a decision-support signal, not a final employment decision.",
                "Manual review is required when risk flags or inconsistent cross-round scores appear.",
            ],
        }

    def build_retention_policy(self, created_at: datetime | None = None) -> Dict[str, Any]:
        created = created_at or datetime.now(UTC)
        return {
            artifact_type: {
                "retention_days": days,
                "delete_after": (created + timedelta(days=days)).date().isoformat(),
            }
            for artifact_type, days in self.DEFAULT_RETENTION_DAYS.items()
        }

    def build_compliance_readiness_report(
        self,
        candidate: Dict[str, Any],
        score_object: Dict[str, Any],
        consent_payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        consent = self.validate_consent(consent_payload)
        sanitized = self.remove_demographic_bias_signals(candidate)
        fairness = self.review_scoring_fairness(score_object)
        explainability = self.build_explainability_notes(score_object)
        retention = self.build_retention_policy()
        blocking_items = []
        if not consent["consent_valid"]:
            blocking_items.append("Missing required consent.")
        if sanitized["removed_protected_signals"]:
            blocking_items.append("Protected demographic signals were removed before scoring.")
        if fairness["fairness_review_status"] != "pass":
            blocking_items.append("Fairness review requires recruiter validation.")

        return {
            "report_id": f"ethics-{candidate.get('candidate_id', candidate.get('id', 'candidate'))}",
            "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "consent": consent,
            "protected_signal_review": sanitized,
            "fairness_review": fairness,
            "explainability": explainability,
            "retention_policy": retention,
            "compliance_status": "ready" if not blocking_items else "action_required",
            "blocking_items": blocking_items,
        }

    def _sanitize_value(self, value: Any) -> tuple[Any, List[str]]:
        removed = []
        if isinstance(value, dict):
            sanitized = {}
            for key, child in value.items():
                normalized_key = key.lower()
                if normalized_key in PROTECTED_SIGNAL_KEYS:
                    removed.append(key)
                    continue
                child_sanitized, child_removed = self._sanitize_value(child)
                sanitized[key] = child_sanitized
                removed.extend(child_removed)
            return sanitized, removed
        if isinstance(value, list):
            sanitized_list = []
            for item in value:
                child_sanitized, child_removed = self._sanitize_value(item)
                sanitized_list.append(child_sanitized)
                removed.extend(child_removed)
            return sanitized_list, removed
        return value, removed
