# Communication Scoring Model

The communication evaluation module calculates a candidate's communication score through a combination of linguistic heuristics and AI-driven assessment. The score ranges from 0 to 100 and evaluates fluency, grammar, vocabulary, clarity, and answer structure.

## Scoring Formula & Components

The **Raw Score** is the sum of five components, each contributing a maximum of 20 points.

**1. Fluency (0-20 points) [Audio/Heuristic]**
Measures sentence continuity, speaking pace, and the prevalence of filler words.
- Formula: Starts at 20. Penalized based on the ratio of filler words to total words, as well as the Words Per Minute (WPM).
- WPM Penalty: Ideal speaking rate is ~130-150 WPM. Speeds below 100 or above 180 incur progressive point deductions.
- Tolerance: Approximately 1 filler word per 30 words is deemed acceptable without penalty. Higher ratios increase the penalty rapidly up to a maximum deduction of 20 points.

**2. Vocabulary Range (0-20 points) [Heuristic]**
Measures lexical density and the use of sophisticated phrasing.
- Formula: Evaluates unique words vs. total words (Lexical Density) and Average Word Length.
- High lexical density (e.g., > 0.65) and strong average word length (e.g., > 5.5 characters) push the score toward 20.

**3. Grammar Quality (0-20 points) [LLM]**
Assesses grammatical accuracy, subject-verb agreement, and tense usage.
- Scored objectively by the AI interviewer model.

**4. Clarity of Explanation (0-20 points) [LLM]**
Evaluates how easily the answer can be understood and the absence of convoluted sentences.
- Scored objectively by the AI interviewer model.

**5. Answer Structure (0-20 points) [LLM]**
Measures logical progression and cohesiveness (e.g., STAR method usage).
- Scored objectively by the AI interviewer model.

### Normalization 

To reduce bias and ensure fairness, the Raw Score (which can be harsh due to compounding sub-scores) is normalized. The model applies a square-root curve standard in educational grading:

`Normalized Score = 10 * sqrt(Raw Score)`

This formula mathematically lifts candidates with average or slightly flawed responses, rewarding baseline effort while retaining strict separation at the highest percentiles. The final normalized score is capped at 100.

---

## Sample Communication Score Outputs

### Sample 1: Strong Communicator
**Candidate Response:** "I successfully orchestrated the deployment of multiple microservices. This streamlined our data processing pipeline by 30%."
**AI Assessment:**
- Fluency: 20.0 (0 filler words detected)
- Vocabulary: 19.5 (High density and average length)
- Grammar: 19.0 (Excellent correctness)
- Clarity: 20.0 (Very clear)
- Structure: 18.0 (Good progression)
- **Raw Score:** 96.5
- **Normalized Final Score:** 98.2 / 100

### Sample 2: Average Communicator with Filler Words
**Candidate Response:** "Um, I think that, like, you know, we basically worked on the backend and, uh, it was good."
**AI Assessment:**
- Fluency: 6.0 (High ratio of filler words: "um", "like", "you know", "basically", "uh")
- Vocabulary: 10.0 (Low density, simple words)
- Grammar: 15.0 (Basic correctness)
- Clarity: 12.0 (Understandable but slightly convoluted)
- Structure: 10.0 (Lacks professional structure)
- **Raw Score:** 53.0
- **Normalized Final Score:** 72.8 / 100

### Sample 3: Brief/Incomplete Answer
**Candidate Response:** "I did backend code."
**AI Assessment:**
- Fluency: 20.0 (No filler words, but extremely short)
- Vocabulary: 6.0 (Low word count, simple terms)
- Grammar: 14.0 (Technically a sentence, but weak)
- Clarity: 14.0 (Clear, but lacks depth)
- Structure: 5.0 (No progression or method used)
- **Raw Score:** 59.0
- **Normalized Final Score:** 76.8 / 100
