import os
import sys
import json
import random
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zecpath_hiring.config.settings")
django.setup()

from zecpath_hiring.apps.core.models import JobProfile, CandidateProfile, HiringRun, AIArtifact

# Load Dentist Models
SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'samples')
DENTIST_FILE = os.path.join(SAMPLES_DIR, 'dentist_models.json')

def generate_demo_dataset():
    print("--- Generating Dentist Demo Dataset ---")
    
    with open(DENTIST_FILE, 'r') as f:
        data = json.load(f)
        
    roles = data.get("roles", [])
    
    if not roles:
        print("No roles found in dentist_models.json")
        return
        
    # 1. Create Job Profile
    target_role = next((r for r in roles if r["id"] == "dentist_001"), roles[0])
    job_title = target_role["title"]
    job_desc = f"{target_role['overview']}\n\nResponsibilities:\n" + "\n".join([f"- {r}" for r in target_role['responsibilities']])
    job_desc += "\n\nQualifications:\n" + "\n".join([f"- {q}" for q in target_role['required_qualifications']])
    
    structured_job = {
        "title": job_title,
        "required_skills": target_role["key_skills"],
        "responsibilities": target_role["responsibilities"],
        "qualifications": target_role["required_qualifications"]
    }
    
    job, _ = JobProfile.objects.get_or_create(
        title=job_title,
        defaults={
            "raw_description": job_desc,
            "structured_profile": structured_job
        }
    )
    print(f"Created Job Profile: {job.title}")

    # 2. Create Candidate Profiles & Hiring Runs
    
    # Candidate 1: Perfect Match
    c1_resume = f"Summary\nHighly experienced {job_title} with 10 years of clinical experience.\nSkills\n{', '.join(target_role['key_skills'])}\nExperience\nLead Dentist at City Clinic, 10 years.\nEducation\nBachelor of Dental Surgery (BDS)"
    c1_structured = {
        "name": "Dr. Alice Carter",
        "skills": target_role['key_skills'],
        "experience_years": 10,
        "education": "Bachelor of Dental Surgery (BDS)"
    }
    c1, _ = CandidateProfile.objects.get_or_create(
        full_name="Dr. Alice Carter",
        defaults={
            "raw_resume": c1_resume,
            "structured_profile": c1_structured
        }
    )
    
    HiringRun.objects.create(
        candidate=c1,
        job=job,
        ats_score=95.0,
        screening_score=100.0,
        interview_score=92.0,
        behavior_score=88.0,
        final_score=94.0,
        decision="HIRE",
        explanation={"reason": "Excellent match across all metrics. Strong clinical diagnosis skills."}
    )
    print(f"Created Candidate & Run: {c1.full_name} -> HIRE")

    # Candidate 2: Partial Match (Different Specialization)
    alt_role = next((r for r in roles if r["id"] == "dentist_011"), roles[1]) # Orthodontist
    c2_resume = f"Summary\nSpecialized {alt_role['title']} with 5 years experience.\nSkills\n{', '.join(alt_role['key_skills'])}\nExperience\nOrthodontist at Smiles Clinic, 5 years.\nEducation\nMDS in Orthodontics"
    c2_structured = {
        "name": "Dr. Bob Miller",
        "skills": alt_role['key_skills'],
        "experience_years": 5,
        "education": "MDS in Orthodontics"
    }
    c2, _ = CandidateProfile.objects.get_or_create(
        full_name="Dr. Bob Miller",
        defaults={
            "raw_resume": c2_resume,
            "structured_profile": c2_structured
        }
    )
    
    HiringRun.objects.create(
        candidate=c2,
        job=job,
        ats_score=60.0,
        screening_score=75.0,
        interview_score=80.0,
        behavior_score=85.0,
        final_score=70.0,
        decision="REVIEW",
        explanation={"reason": "Good candidate but over-specialized in Orthodontics for a General Dentist role."}
    )
    print(f"Created Candidate & Run: {c2.full_name} -> REVIEW")

    # Candidate 3: Poor Match
    c3_resume = "Summary\nDental Assistant looking to step up.\nSkills\nPatient communication, Scheduling\nExperience\nAssistant at Clinic, 2 years.\nEducation\nHigh School Diploma"
    c3_structured = {
        "name": "Charlie Davis",
        "skills": ["Patient communication", "Scheduling"],
        "experience_years": 2,
        "education": "High School Diploma"
    }
    c3, _ = CandidateProfile.objects.get_or_create(
        full_name="Charlie Davis",
        defaults={
            "raw_resume": c3_resume,
            "structured_profile": c3_structured
        }
    )
    
    HiringRun.objects.create(
        candidate=c3,
        job=job,
        ats_score=20.0,
        screening_score=0.0,
        interview_score=0.0,
        behavior_score=50.0,
        final_score=15.0,
        decision="REJECT",
        explanation={"reason": "Lacks required BDS degree and clinical experience."}
    )
    print(f"Created Candidate & Run: {c3.full_name} -> REJECT")

    print("\n--- Demo Dataset Generation Complete ---")
    print("You can view these records in the Zecpath Dashboard.")

if __name__ == "__main__":
    generate_demo_dataset()
