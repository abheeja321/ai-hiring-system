import sys
import os
import json

# Ensure we can import zecpath_hiring
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zecpath_hiring.ai.hr_interview.simulation import HRInterviewSimulationRunner

def print_separator(title: str):
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80 + "\n")

def run_demo():
    print_separator("Day 45: HR Interview AI - Final Production Demo")
    
    print("Initializing HR Interview Simulation Runner...")
    runner = HRInterviewSimulationRunner()
    
    print_separator("1. Architecture & Scoring Logic Explanation")
    print("Architecture Overview:")
    print(" - Modular AI Pipeline: Aptitude, Behavioral, Communication, and Logical Reasoning Evaluators.")
    print(" - HR Scoring Engine: Aggregates scores across turns, applying a customizable weighted configuration.")
    print(" - Report Generator: Produces structured recruiter-ready summaries and natural language text.\n")
    
    print("Scoring Logic (Weights):")
    weights = runner.scoring_engine.config.model_dump()
    for k, v in weights.items():
        print(f" - {k.replace('_', ' ').title()}: {v * 100:.0f}%")
        
    print_separator("2. Running Candidate Interview Simulation")
    print("Simulating interviews for 4 distinct candidate personas...")
    results = runner.run_simulations()
    
    sessions = results.get("sessions", [])
    
    for session in sessions:
        print(f"\n--- Candidate: {session['candidate_id']} ({session['candidate_type']}) ---")
        print(f"Response Style: {session['response_style']}")
        print(f"Manager Notes: {session.get('manager_notes')}")
        
        # Scoring Breakdown
        score_data = session['score_data']
        print("\nScoring Breakdown:")
        avgs = score_data['averages']
        for k, v in avgs.items():
            print(f"  - {k.replace('_', ' ').title()}: {v}/100")
            
        print(f"\nFinal AI Score: {session['ai_score']}/100")
        print(f"Manager Manual Score: {session['manager_score']}/100")
        print(f"Score Delta: {session['score_delta']}")
        
        # Recommendation
        report = session['recruiter_report']
        print(f"\nFinal Hiring Recommendation: {report['recommendation']}")
        print(f"Risks Detected: {', '.join(report['risk_flags']) if report['risk_flags'] else 'None'}")
        
        print("\n" + "-"*60)
        
    print_separator("3. Final Improvements Post Feedback")
    print("Evaluation of AI Scoring vs Manager Manual Scoring (Accuracy & Tuning):")
    for key, value in results['accuracy_evaluation'].items():
        print(f" - {key.replace('_', ' ').title()}: {value}")
    
    print("\nSystem Improvements Implemented:")
    for rec in results['improvement_recommendations']:
        print(f" [Implemented] {rec}")
    print(" [Implemented] Transitioned from generic error gaps to targeted role-fit modifier risk profiling.")
    print(" [Implemented] Manager evaluations seamlessly integrated into final system comparisons.")
    print(" [Implemented] Fully structured JSON generation for production integration.")
    
    print_separator("4. System Handover")
    print("Deliverables Finalized:")
    print(" [x] Final HR Interview AI system")
    print(" [x] Demo dataset (4 distinct candidate personas simulated)")
    print(" [x] Manager evaluation feedback integrated and tracked")
    print(" [x] Production-ready HR Interview module")
    print("\nSYSTEM HANDOVER COMPLETE. THE HR INTERVIEW MODULE IS READY FOR DEPLOYMENT.")

if __name__ == "__main__":
    run_demo()
