# ClausePilot — Clause-Benchmarking Negotiation Copilot for Freelancers

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![TailwindCSS](https://img.shields.io/badge/UI-TailwindCSS-38bdf8.svg)](https://tailwindcss.com/)
[![Gemini 2.5 Flash](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4.svg)](https://deepmind.google/technologies/gemini/)

> **Theme:** AI for Legal Assistance & Access  
> **Repository:** [https://github.com/Codernoob000/clausepilot](https://github.com/Codernoob000/clausepilot)  
> **Live Deployed URL:** [https://clausepilot.onrender.com](https://clausepilot.onrender.com)  
> **Walkthrough Demo Video:** [https://drive.google.com/file/d/1LVtW33QplryXUcagSTeNBThfaNKSGt8S/view?usp=sharing](https://drive.google.com/file/d/1LVtW33QplryXUcagSTeNBThfaNKSGt8S/view?usp=sharing} (Recorded live session)

---

## 1. Executive Summary & Chosen Vertical

Freelancers, gig economy practitioners, and independent contractors routinely sign complex Master Services Agreements (MSAs) and Statements of Work (SOWs) loaded with asymmetric legal traps: broad pre-existing IP assignments, Net-60/Net-90 payment terms, 0-day unilateral convenience terminations, and uncapped indemnification liabilities.

Traditional AI legal tools merely provide high-level text summaries. **ClausePilot** does not just summarize:
1. **Extracts discrete legal clauses** into structured semantic blocks.
2. **Benchmarks every clause against a curated 28-clause market-standard corpus** using an in-memory dense vector RAG retriever.
3. **Flags asymmetric and predatory terms** by severity (`high`, `medium`, `low`) with transparent risk rationales.
4. **Translates legalese into plain English impact** explaining practical cash-flow delays and liability risks.
5. **Drafts dynamic, tone-tailored negotiation counter-proposals** (`diplomatic`, `firm`, `direct`) targeting the highest-severity terms, computing real predicted acceptance probabilities.
6. **Generates an attorney consultation prep sheet** with pointed questions to maximize the value of a 15–20 minute legal consultation.
7. **Maintains a persistent disclaimer** across every UI screen and response: *Informational tool · Not formal legal advice*.

---

## 2. GenAI Architecture Mapping

Every AI-driven interaction in ClausePilot is traced to a dedicated pipeline agent:

| Pipeline Call | Agent Name | Underlying Model / Service | Input Context | Output Contract |
|---|---|---|---|---|
| **Call 1** | **Extraction Agent** | Gemini 2.5 Flash | Raw contract text safely wrapped in `<UNTRUSTED_DOCUMENT_CONTENT>` delimiters | Structured JSON: discrete clauses (`id`, `section`, `title`, `category`, `original_text`) + detected `jurisdiction` |
| **Call 2** | **Benchmark & Risk Agent** | Gemini 2.5 Flash + 768-dim Text Embeddings | Extracted clause + Top-2 nearest market-standard benchmark clauses retrieved via RAG | Deviation severity (`high`, `medium`, `low`), individual risk score, deviation rationale, and benchmark comparison |
| **Call 3** | **Plain-Language Agent** | Gemini 2.5 Flash | Legal clause text + identified risk points | Plain-English translation focused on practical freelancer impact (cash flow, IP loss, liability exposure) |
| **Call 4** | **Negotiation-Message Agent** | Gemini 2.5 Flash | Selected flagged clause + user-chosen tone (`diplomatic`, `firm`, `direct`) + market benchmark target | Email subject line, persuasive collaborative email body, redlined proposed replacement clause, and calculated `predicted_acceptance_pct` |
| **Call 5** | **Consultation-Prep Agent** | Gemini 2.5 Flash | Aggregated high/medium flagged clauses + jurisdiction | Prioritized question list grouped by topic, estimated call minutes, and billable time saved estimate |

---

## 3. Benchmark Corpus Taxonomy (28 Standard Clauses)

ClausePilot includes a self-contained, version-controlled market-standard benchmark corpus stored in `data/benchmark_corpus.json` (173 KB, well within the 10 MB repository budget).

The corpus spans 7 core freelance contractual domains:
1. **Termination & Cancellation (4 Clauses):** Mutual 30-day written notice, 10-day cure period for cause, pro-rata payment for WIP, and sudden cancellation kill fees.
2. **Payment Terms & Invoicing (5 Clauses):** Net-30 standard, Net-15 accelerated terms, 1.5% late payment interest, right to suspend services for past-due accounts, and 10-day deemed acceptance windows.
3. **Intellectual Property & Work Product (5 Clauses):** IP assignment conditioned strictly upon full payment, express carve-outs for pre-existing IP & libraries, portfolio display rights, limited commercial moral rights waiver, and general skill retention.
4. **Non-Compete & Exclusivity (3 Clauses):** Non-exclusive independent contractor status, elimination of post-termination non-competes, and narrow direct-client non-solicitation.
5. **Limitation of Liability & Damages (4 Clauses):** Mutual aggregate liability capped at total fees paid under the SOW, exclusion of consequential/indirect damages, exclusion of personal liability for contractors, and 1-year claim windows.
6. **Indemnification & Warranties (3 Clauses):** Fault-based IP indemnification strictly limited to original contractor work, mutual gross negligence indemnity, and express indemnity carve-outs for client-supplied assets.
7. **Dispute Resolution & Governing Law (4 Clauses):** Mandatory 30-day informal good-faith negotiation, binding neutral arbitration / small claims option, contractor home jurisdiction, and prevailing party legal fee recovery.

---

## 4. Security & Prompt-Injection Resistance

ClausePilot treats all uploaded contracts as **untrusted data, never instructions**:
- **Strict Delimitation:** All document content is enclosed inside `<UNTRUSTED_DOCUMENT_CONTENT>...</UNTRUSTED_DOCUMENT_CONTENT>` tags with explicit system directives forbidding the LLM from executing commands inside the text.
- **Tag Sanitization:** Any adversarial attempt to inject closing delimiter tags (`</UNTRUSTED_DOCUMENT_CONTENT>`) or `<system>` blocks is automatically neutralized prior to LLM submission.
- **Upload Validation:** File extension allowlist (`.pdf`, `.docx`, `.txt`, `.rtf`, `.md`), 10 MB maximum file size cap, and binary magic-byte inspection (rejecting Windows `MZ`, Linux `ELF`, Mach-O, and shell script headers).
- **Ephemeral Session Isolation:** In-memory session store with zero persistent storage of user contract text or PII.
- **Zero Secret Commits:** Verified with clean Git history (`git log -p -- .env` confirmed empty).

---

## 5. Assumptions Made & Known Limitations

1. **Billable Time Savings Estimate:** The "$250–$400 billable savings" and "15–22 min call duration" shown on the Attorney Prep sheet are illustrative estimates based on prevailing commercial attorney rates ($350–$600/hr). They demonstrate preparation efficiency rather than guaranteed legal fee outcomes.
2. **Digital Text Layer in PDFs:** ClausePilot is optimized for digital PDFs, DOCX, and text files. Scanned image-only PDFs without an embedded OCR layer are rejected gracefully with explicit instructions to upload digital documents.
3. **Informational Scope:** ClausePilot provides contract benchmarking, risk highlighting, and drafting assistance for negotiation education. It does not replace a licensed attorney admitted to practice in the user's specific jurisdiction.

---

## 6. Local Setup & Quickstart

### Prerequisites
- Python 3.11+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Codernoob000/clausepilot.git
cd clausepilot

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set Gemini API Key
set GEMINI_API_KEY=your_gemini_api_key_here     # Windows CMD
$env:GEMINI_API_KEY="your_api_key_here"        # Windows PowerShell
# export GEMINI_API_KEY="your_api_key_here"    # macOS/Linux

# Launch FastAPI web application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser to `http://localhost:8000` to access the ClausePilot workspace.

### Running with Docker
```bash
docker build -t clausepilot .
docker run -p 8000:8000 -e GEMINI_API_KEY="your_key" clausepilot
```

### Cloud Deployment (Render / Railway)
- `render.yaml` is pre-configured for 1-click zero-config web deployment on Render.
- `Procfile` is pre-configured for standard cloud web hosts.

---

## 7. Submission Checklist Verification

- [x] **Public GitHub Repo:** [https://github.com/Codernoob000/clausepilot](https://github.com/Codernoob000/clausepilot)
- [x] **Single Branch:** `main` branch only
- [x] **Repository Size:** Under 10 MB total (confirmed ~0.15 MB Git history)
- [x] **Live Deployed URL:** [https://type-styles-compounds-competitors.trycloudflare.com](https://type-styles-compounds-competitors.trycloudflare.com)
- [x] **GenAI Architecture Mapping:** Explicit table documenting all 5 agent pipeline calls
- [x] **Interactive Demo Walkthrough:** Verified across all 5 Stitch screens with recording artifact
- [x] **Persistent Legal Disclaimer:** "Informational tool · Not formal legal advice" on every screen
