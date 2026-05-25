# Zecpath AI: Strategic Roadmap (V2 & Beyond)

This document outlines the strategic vision and future technical milestones for the Zecpath AI Hiring System, prioritizing scale, multimodality, and deeper enterprise integration.

---

## 🚀 Phase 1: Near-Term Enhancements (Months 1-3)
### 1. Asynchronous Task Offloading
- **Current State**: The AI pipeline runs synchronously, meaning the UI blocks while LLM calls execute.
- **Roadmap**: Integrate **Celery & Redis** to run the `run_hiring_pipeline` asynchronously. This will allow recruiters to bulk-upload 500+ resumes and receive push notifications when parsing is complete.

### 2. Multi-Lingual Resume Parsing
- **Current State**: Parsing is heavily optimized for English.
- **Roadmap**: Upgrade the NLP Parser to support multi-lingual extraction (Spanish, French, German) using deep learning translation models prior to semantic scoring, enabling global recruitment capabilities.

### 3. Database Migration
- **Current State**: Development uses SQLite.
- **Roadmap**: Migrate to **PostgreSQL** to handle concurrent pipeline writes and utilize `JSONB` fields for advanced querying of unstructured LLM outputs.

---

## ⚡ Phase 2: Core AI Upgrades (Months 4-6)
### 1. Vector Database Integration (Semantic Search 2.0)
- **Roadmap**: Replace deterministic skill matching with a Vector Database (e.g., Pinecone or pgvector). Resumes and Job Descriptions will be converted into embeddings, allowing the ATS to instantly find "Hidden Gem" candidates based on conceptual similarity rather than specific keywords.

### 2. Dynamic Conversational AI Chatbot
- **Roadmap**: Instead of simulating the interview via static prompts, build a dynamic web interface where candidates chat live with the Zecpath AI. The AI will adapt its follow-up technical questions based on the candidate's real-time answers.

### 3. Automated Interview Scheduling
- **Roadmap**: For candidates that receive a `SELECTED` status, integrate with Google Calendar and Microsoft Outlook APIs to automatically generate meeting links and schedule final human interviews without HR intervention.

---

## 🌍 Phase 3: Enterprise & Multimodality (Months 7-12)
### 1. Video & Voice Interview Analysis
- **Roadmap**: Move beyond text-based screening. Allow candidates to record 2-minute video answers. Zecpath AI will use Whisper (for speech-to-text) and computer vision models to evaluate communication clarity, confidence, and language proficiency natively.

### 2. Predictive Attrition Modeling (Churn)
- **Roadmap**: Link Zecpath's pre-hire data with post-hire employee performance data. Build a machine learning model to predict candidate longevity, flagging candidates who might be a high "Flight Risk" based on historical attrition patterns.

### 3. Custom Enterprise LLM Fine-Tuning
- **Roadmap**: Allow enterprise clients to fine-tune a private instance of the LLM based on their own highly specific, proprietary interview rubrics and internal company culture documents.
