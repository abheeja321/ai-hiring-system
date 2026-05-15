import sys
import os
import time

# Ensure we can import zecpath_hiring
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zecpath_hiring.ai.ats_engine.pipeline import run_hiring_pipeline
from zecpath_hiring.ai.parsers.jd_parser import parse_job_description
from zecpath_hiring.ai.parsers.resume_parser import parse_resume_text

# Candidate Data Profiles
candidates = [
    {
        "name": "Alice Strong",
        "resume": "Summary\nSenior Backend engineer with 8 years of experience.\nSkills\nPython, Django, SQL, AWS, React, Communication, Leadership\nExperience\nLead Backend Engineer at TechCorp, 4 years. Senior Developer at DataInc, 4 years.\nEducation\nMaster of Computer Science",
        "human_decision": "SELECTED"
    },
    {
        "name": "Bob Borderline",
        "resume": "Summary\nBackend developer.\nSkills\nPython, SQL\nExperience\nDeveloper at Startup, 2 years.\nEducation\nBachelor of Science",
        "human_decision": "HOLD_REVIEW"
    },
    {
        "name": "Charlie Reject",
        "resume": "Summary\nFrontend designer.\nSkills\nHTML, CSS, Photoshop\nExperience\nGraphic Designer, 5 years.\nEducation\nBA in Arts",
        "human_decision": "REJECTED"
    },
    {
        "name": "David Risk",
        "resume": "Summary\nBackend engineer.\nSkills\nPython, Django, SQL, AWS\nExperience\nBackend Engineer, 4 years.\nEducation\nMaster of Computer Science\nBehavior\nRefused to answer questions, inconsistent details.",
        "human_decision": "REJECTED" # AI is smarter here and catches the integrity risk
    }
]

job_title = "Senior Python Backend Engineer"
job_desc = "Looking for an experienced backend engineer with 5+ years of experience. Must know Python, Django, SQL, AWS, and have leadership skills."

def run_simulation():
    print("--- Starting Full System Simulation ---")
    start_total = time.time()
    
    # Track phase times
    phase_times = {"parsing": 0.0, "pipeline": 0.0}
    
    # Parse Job
    t0 = time.time()
    job = parse_job_description(job_title, job_desc)
    phase_times["parsing"] += (time.time() - t0)
    
    results = []
    
    for c in candidates:
        print(f"\nEvaluating Candidate: {c['name']}")
        
        t1 = time.time()
        parsed_resume = parse_resume_text(c["name"], c["resume"])
        phase_times["parsing"] += (time.time() - t1)
        
        t2 = time.time()
        try:
            result = run_hiring_pipeline(parsed_resume, job)
            ai_decision = result["decision"]["decision"]
            final_score = result["decision"]["final_score"]
            integrity = result.get("integrity", {}).get("risk_level", "LOW")
        except Exception as e:
            print(f"Error evaluating {c['name']}: {e}")
            ai_decision = "ERROR"
            final_score = 0.0
            integrity = "UNKNOWN"
            
        exec_time = time.time() - t2
        phase_times["pipeline"] += exec_time
        
        print(f"AI Decision: {ai_decision} (Score: {final_score}, Risk: {integrity}) | Human: {c['human_decision']}")
        print(f"Scores: ATS={result['ats']['final_score']}, Screen={result['screening']['screening_score']}, Tech={result['interview']['interview_score']}, Behav={result['behavior']['behavior_score']}")
        print(f"Execution Time: {exec_time:.3f}s")
        
        # Consider a mismatch if Human says SELECTED and AI says REJECTED.
        # It's an interesting case if Human says HOLD and AI says REJECT.
        match = ai_decision == c['human_decision']
        
        results.append({
            "name": c["name"],
            "ai_decision": ai_decision,
            "human_decision": c["human_decision"],
            "match": match,
            "exec_time": exec_time,
            "score": final_score
        })
        
    total_time = time.time() - start_total
    print("\n--- Simulation Complete ---")
    print(f"Total Time: {total_time:.3f}s")
    print(f"Parsing Time: {phase_times['parsing']:.3f}s")
    print(f"Pipeline Time: {phase_times['pipeline']:.3f}s")
    print(f"Average Pipeline Time / Candidate: {phase_times['pipeline']/len(candidates):.3f}s")
    
    matches = sum(1 for r in results if r["match"])
    print(f"\nAccuracy: {matches}/{len(results)} ({(matches/len(results))*100:.2f}%)")
    for r in results:
        print(f"{r['name']}: AI={r['ai_decision']}, Human={r['human_decision']} -> {'MATCH' if r['match'] else 'MISMATCH'}")

if __name__ == '__main__':
    run_simulation()
