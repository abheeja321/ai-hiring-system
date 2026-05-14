from zecpath_hiring.ai.report_generator.generator import HiringIntelligenceReportGenerator
from zecpath_hiring.ai.report_generator.models import FullCandidateReport

def test_intelligence_report_generator_formats_data_correctly():
    generator = HiringIntelligenceReportGenerator()
    
    mock_pipeline_result = {
        "ats": {"final_score": 88.0},
        "screening": {"screening_score": 90.0},
        "interview": {"interview_score": 92.0},
        "behavior": {"behavior_score": 85.0},
        "integrity": {"integrity_score": 100.0, "flags": []},
        "decision": {
            "decision": "SELECTED",
            "confidence_score": 95.0,
            "explanation": "Candidate passed all thresholds.",
            "offer_automation_ready": True
        }
    }
    
    report = generator.generate_report("Alice Smith", "Backend Engineer", mock_pipeline_result)
    
    # Assert model validation
    assert isinstance(report, FullCandidateReport)
    assert report.candidate.name == "Alice Smith"
    assert report.candidate.role == "Backend Engineer"
    
    # Assert scores
    assert report.scores.ats_score == 88.0
    assert report.scores.interview_score == 92.0
    
    # Assert insights
    assert any("Strong resume match" in s for s in report.insights.strengths)
    assert any("Demonstrated high technical proficiency" in s for s in report.insights.strengths)
    assert not report.insights.weaknesses
    assert not report.insights.risk_indicators
    
    # Assert Markdown Generation
    md = generator.export_to_markdown(report)
    assert "# Hiring Intelligence Report: Alice Smith" in md
    assert "**Decision:** `SELECTED`" in md
    assert "- **ATS Match:** 88.0/100" in md

def test_intelligence_report_generator_handles_weaknesses_and_risks():
    generator = HiringIntelligenceReportGenerator()
    
    mock_pipeline_result = {
        "ats": {"final_score": 50.0},
        "screening": {"screening_score": 55.0},
        "interview": {"interview_score": 40.0},
        "behavior": {"behavior_score": 45.0},
        "integrity": {"integrity_score": 60.0, "flags": ["Tab switches detected"]},
        "decision": {
            "decision": "REJECTED",
            "confidence_score": 90.0,
            "explanation": "Candidate failed multiple stages and flagged for risk.",
            "offer_automation_ready": False
        }
    }
    
    report = generator.generate_report("Bob Jones", "Frontend Dev", mock_pipeline_result)
    
    assert any("Resume shows gaps" in w for w in report.insights.weaknesses)
    assert any("Struggled with baseline" in w for w in report.insights.weaknesses)
    assert any("Failed to meet technical" in w for w in report.insights.weaknesses)
    
    assert any("Tab switches detected" in r for r in report.insights.risk_indicators)
    assert any("Low behavioral score" in r for r in report.insights.risk_indicators)
    
    md = generator.export_to_markdown(report)
    assert "**Decision:** `REJECTED`" in md
    assert "Tab switches detected" in md
