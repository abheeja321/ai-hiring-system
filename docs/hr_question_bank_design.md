# HR Question Bank Architecture

The Question Bank is not a static list of strings; it is an intelligent generator that selects themes and constraints to guide the AI in asking personalized questions.

## Categories
Questions are grouped into six core HR categories:
1. **Self-introduction**: Ice-breakers and background summaries.
2. **Career journey**: Past experiences, transitions, and learnings.
3. **Strengths & weaknesses**: Self-awareness and growth mindset.
4. **Teamwork & culture fit**: Collaboration, conflict resolution, and adaptability.
5. **Career goals**: Short-term/long-term aspirations and alignment with the company.
6. **Availability & commitment**: Logistics, notice periods, and work arrangements.

## Role-Based Generation Logic

The bank uses the candidate's parsed resume and the job description to apply two primary filters:

### 1. Experience Level Factor
- **Fresher (0-2 years)**:
  - Focus: Potential, academic projects, internships, adaptability, and willingness to learn.
  - *Example Theme*: "Describe a challenging university project and how you handled a disagreement with a team member."
- **Experienced (3+ years)**:
  - Focus: Track record, leadership, complex problem-solving, and career trajectory.
  - *Example Theme*: "Tell me about a time you had to pivot a major project due to shifting business requirements."

### 2. Role Type Factor
- **Technical Roles** (e.g., Software Engineer, Data Scientist):
  - Focus: Code reviews, technical disagreements, agile workflows, and managing technical debt.
  - *Example Theme*: "How do you handle situations where a stakeholder demands a feature that compromises system architecture?"
- **Non-Technical Roles** (e.g., Sales, HR, Marketing):
  - Focus: Client management, cross-functional collaboration, communication, and target achievement.
  - *Example Theme*: "Describe a time you had to persuade a difficult client or internal stakeholder to adopt your strategy."

## AI Prompt Structure
When a category is selected by the Flow Controller, the Question Bank outputs a prompt payload for the LLM:
```json
{
  "category": "Teamwork",
  "candidate_experience_level": "Experienced",
  "role_type": "Technical",
  "instructions": "Ask a behavioral question about resolving a technical dispute within an engineering team. Do not sound robotic; frame it conversationally."
}
```
