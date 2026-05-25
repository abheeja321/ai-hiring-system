# Demo Dataset & Simulation Environment

I have created a complete simulation environment to generate realistic hiring pipeline data using the `dentist_models.json` dataset.

## End-to-End Simulation Script
A new python script has been created in your repository:
**`zecpath_hiring/scripts/generate_dentist_demo.py`**

You can run this script at any time to populate your local database with this realistic test data:
```bash
python zecpath_hiring/scripts/generate_dentist_demo.py
```

---

## Simulated Job Profile: General Dentist

**Overview**: A General Dentist provides comprehensive dental care for patients of all ages.
**Required Qualifications**: Bachelor of Dental Surgery (BDS), Dental license.
**Key Skills**: Clinical diagnosis, Manual dexterity, Patient communication, Treatment planning, Infection control.

---

## Test Candidate Profiles & Pipeline Results

The simulation generates three distinct candidate profiles to demonstrate the system's scoring and decision capabilities.

### Candidate 1: The Perfect Match
* **Name**: Dr. Alice Carter
* **Profile**: 10 years experience as Lead Dentist, holds a BDS degree, and possesses all required skills (Clinical diagnosis, Treatment planning, etc.).
* **Simulated Pipeline Output**:
  * **ATS Score**: 95.0
  * **Screening**: 100.0 (Eligible)
  * **Interview AI**: 92.0
  * **Behavior AI**: 88.0
  * **Final Decision**: **`HIRE`** (Score: 94.0)
  * **Explanation**: Excellent match across all metrics. Strong clinical diagnosis skills demonstrated in 10 years of experience.

### Candidate 2: The Partial Match (Over-Specialized)
* **Name**: Dr. Bob Miller
* **Profile**: 5 years experience as an Orthodontist, holds an MDS in Orthodontics. Strong in specific areas but lacks general dentistry breadth.
* **Simulated Pipeline Output**:
  * **ATS Score**: 60.0
  * **Screening**: 75.0 (Partially Eligible)
  * **Interview AI**: 80.0
  * **Behavior AI**: 85.0
  * **Final Decision**: **`REVIEW`** (Score: 70.0)
  * **Explanation**: Good candidate but over-specialized in Orthodontics for a General Dentist role. HR should review if skills are transferable.

### Candidate 3: The Poor Match (Underqualified)
* **Name**: Charlie Davis
* **Profile**: 2 years experience as a Dental Assistant. Holds a High School Diploma. Only has scheduling and communication skills.
* **Simulated Pipeline Output**:
  * **ATS Score**: 20.0
  * **Screening**: 0.0 (Ineligible)
  * **Interview AI**: 0.0
  * **Behavior AI**: 50.0
  * **Final Decision**: **`REJECT`** (Score: 15.0)
  * **Explanation**: Lacks the mandatory BDS degree and clinical diagnosis experience required for the role.
