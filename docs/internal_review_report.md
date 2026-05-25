# Internal Review & System Walkthrough Report

## 1. Executive Summary
This document serves as the Day 64 internal review of the Zecpath AI Hiring System. A full system walkthrough from candidate ingestion to final AI decision was conducted to evaluate the pipeline's stability, accuracy, and user experience. While the system demonstrates robust, multi-faceted intelligence (ATS, Technical, Behavioral, Integrity), several critical bottlenecks in performance and UX must be addressed before enterprise-scale deployment.

---

## 2. Full System Walkthrough Observations

### Phase 1: Ingestion & ATS Engine
- **Workflow**: Resumes and JDs are parsed into structured JSON and compared deterministically.
- **Observation**: Fast and reliable. However, the parser occasionally struggles with unconventional resume formats (e.g., highly stylized multi-column PDFs).
- **Accuracy Gap**: Pure keyword matching in ATS can penalize highly skilled candidates who use different synonyms not explicitly mapped by the LLM.

### Phase 2: Screening & Eligibility
- **Workflow**: Hard constraints (e.g., "Must have BDS degree") are evaluated.
- **Observation**: Works well for structured data.
- **Accuracy Gap**: Semantic understanding of "equivalent experience" needs refinement. Sometimes a Master's degree is flagged as failing a "Bachelor's required" check due to strict LLM instruction bounds.

### Phase 3: Technical & HR Interview Simulation
- **Workflow**: Generates potential Q&A pairs and scores candidate competency.
- **Observation**: Highly insightful and provides excellent explainability.
- **Performance Issue**: **CRITICAL**. These modules make synchronous external API calls to Large Language Models. Running this sequentially takes 15-45 seconds per candidate. 

### Phase 4: Behavior & Integrity Checking
- **Workflow**: Sentiment analysis and detection of malpractice (e.g., fake certifications, anomalies).
- **Observation**: The Integrity engine catches obvious discrepancies (e.g., overlapping full-time employment gaps).
- **Accuracy Gap**: False positives. An overqualified candidate may trigger "flight risk" behavioral flags too aggressively.

### Phase 5: Final Decision Maker
- **Workflow**: Aggregates scores and outputs `HIRE`, `REVIEW`, or `REJECT`.
- **Observation**: The weighted average logic works, but a single poor score (e.g., an ATS miss due to formatting) can drag a perfectly good candidate down to `REJECT`.

---

## 3. Identified Improvement Areas

### A. Accuracy Gaps
1. **Resume Parser Resilience**: Needs an OCR fallback for image-based PDFs and better handling of multi-column layouts.
2. **Semantic ATS Matching**: Move from exact string keyword matching to Vector/Embedding similarity matching (e.g., using `sentence-transformers`) to handle synonyms gracefully.
3. **LLM Hallucinations in Interviews**: The technical simulator occasionally expects overly academic answers; needs prompt tuning for practical, real-world responses.

### B. User Experience (UX) Issues
1. **Synchronous Waiting**: The current Django API and web dashboard block the UI while waiting for the pipeline to finish. A recruiter uploading 50 resumes will cause a timeout.
2. **Lack of Real-Time Feedback**: Users have no visibility into which stage (ATS vs. Screening vs. Interview) the candidate is currently in.
3. **Rigid Dashboards**: The dashboard UI is functional but lacks filtering capabilities to sort candidates dynamically by sub-scores (e.g., "Show me high Behavioral, low Technical").

### C. Performance & Scalability Issues
1. **Sequential AI Calls**: Calling ATS -> Screening -> Tech -> Behavior in series is computationally expensive.
2. **SQLite Database**: The local `db.sqlite3` will face database lock errors under concurrent load.
3. **Payload Sizes**: Saving entire raw unstructured transcripts in the `HiringRun` payload causes database bloat.

---

## 4. Prioritized Action Plan

> [!IMPORTANT]  
> The following list is prioritized by impact vs. effort to transition the system to a production-ready state.

### Priority 1: High Impact / Immediate (Days 65-67)
- [ ] **Asynchronous Processing**: Implement `Celery` with `Redis` or `RabbitMQ` to offload the `run_hiring_pipeline` execution.
- [ ] **Database Migration**: Migrate from SQLite to **PostgreSQL** to handle concurrent reads/writes and support JSONB field querying.
- [ ] **WebSockets / Polling**: Add a progress bar to the dashboard using WebSockets (Django Channels) or AJAX polling to show real-time pipeline status (e.g., "Running ATS...").

### Priority 2: Medium Impact / Core Logic (Days 68-72)
- [ ] **Parallel AI Execution**: Refactor the pipeline so ATS, Screening, and Interview models run concurrently using `asyncio` or multiple Celery tasks, reducing total wait time by 60%.
- [ ] **Vector Search Integration**: Implement a lightweight vector database (e.g., Pinecone, pgvector) to replace deterministic ATS matching with semantic similarity.

### Priority 3: Optimization / UI (Days 73+)
- [ ] **Dashboard Revamp**: Build interactive React/Vue components or enhanced Django templates for rich filtering and sorting.
- [ ] **Data Pruning**: Implement a cron job to compress or archive `AIArtifact` logs older than 30 days to save DB storage.
- [ ] **Resume Parser Fallback**: Integrate AWS Textract or Tesseract OCR for failing PDF documents.
