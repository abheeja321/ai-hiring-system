from typing import Dict, Any
from zecpath_hiring.ai.report_generator.models import (
    CandidateProfile, ModuleSummary, KeyInsights, Recommendation, FullCandidateReport
)

class HiringIntelligenceReportGenerator:
    def generate_report(self, candidate_name: str, job_title: str, pipeline_result: Dict[str, Any]) -> FullCandidateReport:
        # 1. Parse Profile
        profile = CandidateProfile(name=candidate_name, role=job_title)
        
        # 2. Extract Scores
        ats_score = float(pipeline_result.get("ats", {}).get("final_score", 0))
        screening_score = float(pipeline_result.get("screening", {}).get("screening_score", 0))
        interview_score = float(pipeline_result.get("interview", {}).get("interview_score", 0))
        behavior_score = float(pipeline_result.get("behavior", {}).get("behavior_score", 0))
        integrity_score = float(pipeline_result.get("integrity", {}).get("integrity_score", 100.0))
        
        scores = ModuleSummary(
            ats_score=ats_score,
            screening_score=screening_score,
            interview_score=interview_score,
            behavior_score=behavior_score,
            integrity_score=integrity_score
        )
        
        # 3. Derive Insights
        strengths = []
        weaknesses = []
        risk_indicators = []
        
        # ATS logic
        if ats_score >= 80:
            strengths.append(f"Strong resume match for the {job_title} role (ATS: {ats_score}).")
        elif ats_score < 60:
            weaknesses.append("Resume shows gaps in required skills or experience.")
            
        # Screening logic
        if screening_score >= 85:
            strengths.append("Exceptional performance in initial screening and aptitude.")
        elif screening_score < 60:
            weaknesses.append("Struggled with baseline screening questions.")
            
        # Technical/Interview logic
        if interview_score >= 85:
            strengths.append(f"Demonstrated high technical proficiency in interview (Score: {interview_score}).")
        elif interview_score < 50:
            weaknesses.append("Failed to meet technical interview benchmarks.")
            
        # Behavior & Integrity logic
        if behavior_score >= 80:
            strengths.append("High behavioral confidence and positive communication style.")
        elif behavior_score < 50:
            risk_indicators.append("Low behavioral score; possible communication or confidence issues.")
            
        integrity_flags = pipeline_result.get("integrity", {}).get("flags", [])
        if integrity_score < 70 or integrity_flags:
            risk_indicators.extend(integrity_flags)
            risk_indicators.append("Elevated integrity risk detected during session.")
            
        insights = KeyInsights(strengths=strengths, weaknesses=weaknesses, risk_indicators=risk_indicators)
        
        # 4. Final Recommendation
        decision_data = pipeline_result.get("decision", {})
        recommendation = Recommendation(
            decision=decision_data.get("decision", "REJECTED"),
            confidence_score=decision_data.get("confidence_score", 0.0),
            explanation=decision_data.get("explanation", "No explanation provided."),
            automation_ready=decision_data.get("offer_automation_ready", False)
        )
        
        return FullCandidateReport(
            candidate=profile,
            scores=scores,
            insights=insights,
            recommendation=recommendation,
            raw_data=pipeline_result
        )
        
    def export_to_markdown(self, report: FullCandidateReport) -> str:
        md = f"# Hiring Intelligence Report: {report.candidate.name}\n"
        md += f"**Role Evaluated:** {report.candidate.role}\n\n"
        
        md += "## Final Recommendation\n"
        md += f"- **Decision:** `{report.recommendation.decision}`\n"
        md += f"- **AI Confidence Score:** {report.recommendation.confidence_score}%\n"
        md += f"- **Explanation:** {report.recommendation.explanation}\n\n"
        
        md += "## Module Breakdown\n"
        md += f"- **ATS Match:** {report.scores.ats_score}/100\n"
        md += f"- **Screening:** {report.scores.screening_score}/100\n"
        md += f"- **HR/Tech Interview:** {report.scores.interview_score}/100\n"
        md += f"- **Behavioral:** {report.scores.behavior_score}/100\n"
        md += f"- **Integrity:** {report.scores.integrity_score}/100\n\n"
        
        md += "## Key Insights\n"
        md += "### Strengths\n"
        if report.insights.strengths:
            for s in report.insights.strengths:
                md += f"- {s}\n"
        else:
            md += "- No major strengths identified.\n"
            
        md += "\n### Weaknesses\n"
        if report.insights.weaknesses:
            for w in report.insights.weaknesses:
                md += f"- {w}\n"
        else:
            md += "- No major weaknesses identified.\n"
            
        md += "\n### Risk Indicators\n"
        if report.insights.risk_indicators:
            for r in report.insights.risk_indicators:
                md += f"- {r}\n"
        else:
            md += "- No risks detected. Safe profile.\n"
            
        return md

    def export_to_dict(self, report: FullCandidateReport) -> dict:
        return report.model_dump() if hasattr(report, "model_dump") else report.dict()
