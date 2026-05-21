import os
import csv
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dental_hiring_demo')

DIRS = [
    "resumes",
    "job_descriptions",
    "candidate_profiles",
    "ats_results",
    "interview_answers",
    "screening_outputs",
    "final_selection"
]

def create_directories():
    os.makedirs(DATASET_DIR, exist_ok=True)
    for d in DIRS:
        os.makedirs(os.path.join(DATASET_DIR, d), exist_ok=True)

def generate_csv(filename, headers, data, sub_dir=""):
    path = os.path.join(DATASET_DIR, sub_dir, filename)
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Created {path}")

def create_dataset():
    create_directories()

    # 1. Job Descriptions (jobs.csv)
    jobs_headers = ["Job_ID", "Role", "Qualification", "Experience", "Skills", "Location", "Salary"]
    jobs_data = [
        ["DEN001", "General Dentist", "BDS", "2+ years", "Clinical diagnosis, communication", "Kochi", "₹40,000/month"],
        ["DEN002", "Orthodontist", "MDS Orthodontics", "3+ years", "Braces, Aligners, Facial growth analysis", "Bangalore", "₹80,000/month"],
        ["DEN003", "Pediatric Dentist", "MDS Pediatric", "1+ years", "Child behavior management, Preventive dentistry", "Mumbai", "₹60,000/month"],
        ["DEN004", "Implantologist", "MDS / Cert in Implants", "5+ years", "Surgical precision, Implant systems", "Delhi", "₹100,000/month"],
        ["DEN005", "Dental AI Researcher", "BDS + Data Science", "0-2 years", "Python, Clinical NLP, Research", "Remote", "₹70,000/month"]
    ]
    generate_csv("jobs.csv", jobs_headers, jobs_data, "job_descriptions")

    # 2. Resumes / Candidate Profiles (resumes.csv)
    resumes_headers = ["Candidate_ID", "Name", "Role_Applied", "Qualification", "Experience", "Skills", "Communication_Level", "Anomaly_Flag", "Resume_Quality"]
    resumes_data = [
        # General Dentist Candidates
        ["CAND001", "Rahul Menon", "General Dentist", "BDS", "3 years", "Root canal, diagnosis, general care", "Excellent", "None", "Good"],
        ["CAND002", "Arya S", "General Dentist", "BDS", "Fresher", "Cleaning, fillings", "Average", "Experience Gap", "Medium"],
        ["CAND003", "John K", "General Dentist", "BDS", "None", "Limited, observation only", "Poor", "Missing Skills", "Poor"],
        
        # Orthodontist Candidates
        ["CAND004", "Dr. Sarah", "Orthodontist", "MDS Orthodontics", "4 years", "Invisalign, Braces, 3D Scanning", "Excellent", "None", "Good"],
        ["CAND005", "Dr. FakeCert", "Orthodontist", "BDS", "1 year", "Basic braces", "Average", "Fake Certification claimed", "Poor"],
        
        # Pediatric Dentist Candidates
        ["CAND006", "Dr. Emily", "Pediatric Dentist", "MDS Pediatric", "2 years", "Behavior management, sealants", "Excellent", "None", "Good"],
        ["CAND007", "Dr. Overqual", "Pediatric Dentist", "MDS Pediatric + PhD", "15 years", "Advanced surgery, research", "Excellent", "Overqualified", "Good"],

        # Implantologist Candidates
        ["CAND008", "Dr. Smith", "Implantologist", "MDS Prosthodontics", "6 years", "All-on-4, Sinus lift, Grafting", "Excellent", "None", "Good"],
        ["CAND009", "Dr. Mismatch", "Implantologist", "MDS Endodontics", "5 years", "Root canals, apicoectomy", "Good", "Skill Mismatch", "Medium"]
    ]
    generate_csv("resumes.csv", resumes_headers, resumes_data, "resumes")

    # 3. ATS Scores (ats_scores.csv)
    ats_headers = ["Candidate_ID", "Name", "Job_ID", "ATS_Score_Pct", "Keyword_Match", "Experience_Match"]
    ats_data = [
        ["CAND001", "Rahul Menon", "DEN001", 92, "High", "Matched"],
        ["CAND002", "Arya S", "DEN001", 71, "Medium", "Under"],
        ["CAND003", "John K", "DEN001", 40, "Low", "Under"],
        ["CAND004", "Dr. Sarah", "DEN002", 95, "High", "Matched"],
        ["CAND005", "Dr. FakeCert", "DEN002", 45, "Low", "Under"],
        ["CAND006", "Dr. Emily", "DEN003", 90, "High", "Matched"],
        ["CAND007", "Dr. Overqual", "DEN003", 99, "High", "Over"],
        ["CAND008", "Dr. Smith", "DEN004", 96, "High", "Matched"],
        ["CAND009", "Dr. Mismatch", "DEN004", 55, "Low", "Matched"]
    ]
    generate_csv("ats_scores.csv", ats_headers, ats_data, "ats_results")

    # 4. Interview Responses (interview.csv)
    interview_headers = ["Candidate_ID", "Question_Type", "Question", "Answer_Transcript", "Evaluation_Score", "Feedback"]
    interview_data = [
        ["CAND001", "Technical", "Explain root canal treatment.", "Root canal treatment removes infected pulp tissue and seals the tooth to prevent reinfection.", 90, "Accurate and concise."],
        ["CAND002", "Technical", "Explain root canal treatment.", "It involves cleaning the tooth when it hurts.", 65, "Too simplistic, lacking medical terminology."],
        ["CAND003", "Technical", "Explain root canal treatment.", "It is treatment for teeth pain.", 40, "Inaccurate and lacks depth."],
        ["CAND004", "Behavioral", "How do you handle an anxious patient?", "I take time to explain the procedure and use calming techniques before starting.", 95, "Great empathy and process."],
        ["CAND005", "Behavioral", "How do you handle an anxious patient?", "I just tell them to relax, it won't hurt.", 50, "Lacks empathy and proper management."],
    ]
    generate_csv("interview.csv", interview_headers, interview_data, "interview_answers")

    # 5. Shortlist / Final Selection (shortlist.csv)
    shortlist_headers = ["Candidate_ID", "Name", "Job_ID", "Final_Score", "Decision", "Reasoning"]
    shortlist_data = [
        ["CAND001", "Rahul Menon", "DEN001", 91.5, "Selected", "Strong ATS and interview performance."],
        ["CAND002", "Arya S", "DEN001", 68.0, "Hold", "Needs training; decent potential but inexperienced."],
        ["CAND003", "John K", "DEN001", 35.0, "Rejected", "Failed technical interview and ATS."],
        ["CAND004", "Dr. Sarah", "DEN002", 94.0, "Selected", "Perfect match for Orthodontics."],
        ["CAND005", "Dr. FakeCert", "DEN002", 20.0, "Rejected", "Integrity flags raised during screening."],
        ["CAND006", "Dr. Emily", "DEN003", 92.0, "Selected", "Excellent pediatric skills."],
        ["CAND007", "Dr. Overqual", "DEN003", 85.0, "Hold", "Overqualified, flight risk. Verify salary expectations."],
        ["CAND008", "Dr. Smith", "DEN004", 95.0, "Selected", "Extensive implant experience."],
        ["CAND009", "Dr. Mismatch", "DEN004", 45.0, "Rejected", "Endodontic specialist applying for surgical implant role."]
    ]
    generate_csv("shortlist.csv", shortlist_headers, shortlist_data, "final_selection")

    # Write text files for Resumes and JDs to simulate raw data
    for row in jobs_data:
        jd_path = os.path.join(DATASET_DIR, "job_descriptions", f"{row[0]}.txt")
        with open(jd_path, "w", encoding="utf-8") as f:
            f.write(f"Job ID: {row[0]}\nRole: {row[1]}\nQualification: {row[2]}\nExperience: {row[3]}\nSkills: {row[4]}\nLocation: {row[5]}\nSalary: {row[6]}\n")

    for row in resumes_data:
        res_path = os.path.join(DATASET_DIR, "resumes", f"{row[0]}.txt")
        with open(res_path, "w", encoding="utf-8") as f:
            f.write(f"Name: {row[1]}\nApplying For: {row[2]}\nQualification: {row[3]}\nExperience: {row[4]}\nSkills: {row[5]}\n")

    print(f"\nSuccessfully generated Demo Dataset in {DATASET_DIR}")

if __name__ == "__main__":
    create_dataset()
