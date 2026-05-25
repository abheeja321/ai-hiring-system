# Zecpath AI: Live Demo Script

This script is designed to be read alongside your live demonstration of the Zecpath AI Hiring System. Ensure your local server is running (`python manage.py runserver`) and you have the `dental_hiring_demo` dataset ready.

## Phase 1: Introduction & The Setup
**[Action: Open the Zecpath Dashboard on the "Jobs" page]**

**Speaker:** 
> "Welcome to the live demonstration of the Zecpath AI Hiring System. Today, we are going to look at a real-world scenario in the healthcare space. 
> 
> We are a rapidly growing dental clinic, and we are looking to hire a 'General Dentist'. Let's look at the requirements the AI has automatically parsed from our HR documentation."

**[Action: Click on the 'General Dentist' Job Profile]**

**Speaker:** 
> "As you can see, the AI has structured the raw text into a clean JSON schema. It knows we need someone with a BDS degree, at least 2 years of experience, and core skills in Clinical Diagnosis and Treatment Planning."

---

## Phase 2: Processing Candidates
**[Action: Navigate to the Pipeline Runner or Bulk Upload page]**

**Speaker:** 
> "We've received a stack of resumes. Traditionally, a recruiter would spend hours reading these to find a match. We are going to upload three different candidates right now and let the AI process them in seconds."

**[Action: Run the `generate_dentist_demo.py` script in the background, or click 'Run Pipeline' for the three candidates]**

**Speaker:** 
> "The system is currently parsing the unstructured PDFs, running semantic ATS matching, verifying eligibility constraints, and actually simulating a technical interview based on the candidates' stated experience. Finally, the Decision Engine is aggregating these scores to make a recommendation."

---

## Phase 3: Reviewing the Perfect Match (HIRE)
**[Action: Open the Results Page for Candidate 1: Dr. Alice Carter]**

**Speaker:** 
> "Let's look at our first candidate, Dr. Alice Carter. The AI immediately flagged her as a **HIRE** with a final score of 94. 
> 
> Look at the generated Intelligence Report. It's not just a number. The AI provides an explainable markdown summary. Under 'Strengths', it highlights her 10 years of clinical experience. The ATS score is a 95, and her simulated Technical Interview score is a 92. This candidate is ready for an immediate offer."

---

## Phase 4: The Edge Case (HOLD / REVIEW)
**[Action: Open the Results Page for Candidate 2: Dr. Bob Miller]**

**Speaker:** 
> "Now, AI isn't just about saying Yes or No. It’s about nuance. Let's look at Dr. Bob Miller.
> 
> The AI flagged him for **REVIEW** with a score of 70. Why? Bob is highly qualified—he has an MDS in Orthodontics and 5 years of experience. However, the AI recognized that he is *over-specialized* for a General Dentist role. The Intelligence Report specifically notes under 'Risk Indicators' that an Endodontic specialist applying for a general role might be a flight risk or a skill mismatch. This saves HR from a potentially bad cultural fit, but flags it for a human to double-check."

---

## Phase 5: The Underqualified (REJECT)
**[Action: Open the Results Page for Candidate 3: Charlie Davis]**

**Speaker:** 
> "Finally, we have Charlie Davis. Charlie is a Dental Assistant. 
> 
> In a traditional ATS, if Charlie stuffed his resume with keywords like 'Dental' and 'Clinic', he might slip through. Zecpath AI, however, gave him a **REJECT** with a score of 15. The Screening AI caught that he lacks the mandatory BDS degree, immediately zeroing out his eligibility. No human recruiter had to waste time discovering this."

---

## Phase 6: Conclusion & Business Value
**[Action: Navigate back to the main Dashboard showing the aggregated stats]**

**Speaker:** 
> "In just a few minutes, the Zecpath AI system ingested unstructured data, evaluated it across four distinct dimensions of competency, and provided us with one perfect candidate, one nuanced review case, and one immediate rejection—all with fully explainable logic.
> 
> This is how we reduce time-to-hire by 80%, eliminate human bias at the top of the funnel, and ensure that only the highest quality talent makes it to the final human interview stage. Thank you."
