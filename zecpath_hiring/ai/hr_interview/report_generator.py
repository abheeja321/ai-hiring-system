from datetime import UTC, datetime
from typing import Any, Dict, List


class HRInterviewReportGenerator:
    """
    Converts HR interview analysis into recruiter-ready structured insights.
    """

    def generate_structured_summary(
        self,
        candidate: Dict[str, Any],
        score_data: Dict[str, Any],
        evaluations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        strengths = self._dedupe(self._extract_items(evaluations, "strengths"))
        weaknesses = self._dedupe(self._extract_items(evaluations, "weaknesses"))
        risk_flags = self._dedupe(self._extract_items(evaluations, "risk_flags"))
        inconsistencies = self._highlight_inconsistencies(evaluations)
        culture_fit = self._culture_fit_indicators(score_data, evaluations)

        if score_data.get("averages", {}).get("communication", 0) >= 80:
            strengths.append("Communicates clearly and stays easy to follow.")
        if score_data.get("averages", {}).get("consistency", 100) < 75:
            risk_flags.append("Consistency score is below recruiter review threshold.")
        if inconsistencies:
            risk_flags.append("Interview contains inconsistencies requiring clarification.")

        final_score = score_data.get("final_score", 0)
        summary = {
            "report_id": f"hr-{candidate.get('candidate_id', 'candidate')}",
            "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "candidate": {
                "candidate_id": candidate.get("candidate_id"),
                "name": candidate.get("full_name") or candidate.get("name"),
            },
            "overall_hr_score": final_score,
            "overall_performance": self._performance_band(final_score),
            "candidate_strengths": self._dedupe(strengths),
            "weaknesses": self._dedupe(weaknesses),
            "cultural_fit_indicators": culture_fit,
            "risk_flags": self._dedupe(risk_flags),
            "inconsistencies": inconsistencies,
            "structured_summary_template": {
                "candidate_strengths": [],
                "weaknesses": [],
                "cultural_fit_indicators": [],
                "risk_flags": [],
                "overall_hr_performance": "",
                "recruiter_recommendation": "",
            },
            "recommendation": self._recommendation(final_score, risk_flags),
        }
        summary["natural_language_report"] = self.generate_natural_language_report(summary, score_data)
        return summary

    def generate_natural_language_report(self, summary: Dict[str, Any], score_data: Dict[str, Any]) -> str:
        candidate_name = summary.get("candidate", {}).get("name") or "The candidate"
        averages = score_data.get("averages", {})
        strengths = "; ".join(summary.get("candidate_strengths", [])[:3]) or "No dominant strengths were detected"
        weaknesses = "; ".join(summary.get("weaknesses", [])[:2]) or "No major weaknesses were detected"
        risks = "; ".join(summary.get("risk_flags", [])[:2]) or "No major risk flags were detected"

        return (
            f"{candidate_name} delivered a {summary.get('overall_performance', 'not rated').lower()} HR interview "
            f"with an overall score of {summary.get('overall_hr_score', 0)}/100. "
            f"Strengths: {strengths}. Weaknesses: {weaknesses}. "
            f"Communication averaged {averages.get('communication', 'N/A')}/100, consistency averaged "
            f"{averages.get('consistency', 'N/A')}/100, and recruiter risk review notes are: {risks}. "
            f"Recommendation: {summary.get('recommendation')}."
        )

    def sample_reports(self) -> List[Dict[str, Any]]:
        strong = self.generate_structured_summary(
            {"candidate_id": "sample-strong", "full_name": "Sample Strong"},
            {
                "final_score": 88.0,
                "averages": {"communication": 86.0, "confidence": 84.0, "consistency": 92.0},
            },
            [
                {
                    "strengths": ["Uses structured examples.", "Shows collaborative decision-making."],
                    "weaknesses": [],
                    "risk_flags": [],
                }
            ],
        )
        review = self.generate_structured_summary(
            {"candidate_id": "sample-review", "full_name": "Sample Review"},
            {
                "final_score": 67.0,
                "averages": {"communication": 64.0, "confidence": 61.0, "consistency": 70.0},
            },
            [
                {
                    "strengths": ["Has relevant motivation."],
                    "weaknesses": ["Answers need sharper examples."],
                    "risk_flags": ["Problem-solving structure is incomplete."],
                    "inconsistencies": ["Availability changed between opening and closing answers."],
                }
            ],
        )
        return [strong, review]

    def _extract_items(self, evaluations: List[Dict[str, Any]], key: str) -> List[str]:
        items = []
        for evaluation in evaluations:
            value = evaluation.get(key, [])
            if isinstance(value, str):
                items.append(value)
            else:
                items.extend(value)
        return [item for item in items if item]

    def _highlight_inconsistencies(self, evaluations: List[Dict[str, Any]]) -> List[str]:
        inconsistencies = self._extract_items(evaluations, "inconsistencies")
        for evaluation in evaluations:
            issues = evaluation.get("detected_issues", {})
            if issues.get("contradiction_penalty", 0) >= 30:
                inconsistencies.append("High contradiction penalty detected in one or more answers.")
        return self._dedupe(inconsistencies)

    def _culture_fit_indicators(self, score_data: Dict[str, Any], evaluations: List[Dict[str, Any]]) -> List[str]:
        indicators = []
        averages = score_data.get("averages", {})
        if averages.get("communication", 0) >= 75:
            indicators.append("Clear communication style.")
        if averages.get("confidence", 0) >= 75:
            indicators.append("Steady confidence under interview pressure.")
        for item in self._extract_items(evaluations, "culture_fit_indicators"):
            indicators.append(item)
        return self._dedupe(indicators)

    def _performance_band(self, final_score: float) -> str:
        if final_score >= 85:
            return "Strong"
        if final_score >= 70:
            return "Good"
        if final_score >= 60:
            return "Needs recruiter review"
        return "High risk"

    def _recommendation(self, final_score: float, risk_flags: List[str]) -> str:
        if final_score >= 80 and not risk_flags:
            return "Proceed to next round."
        if final_score >= 65:
            return "Proceed only after recruiter clarification."
        return "Do not advance without substantial review."

    def _dedupe(self, items: List[str]) -> List[str]:
        return list(dict.fromkeys(item for item in items if item))
