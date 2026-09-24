# ClausePilot — Clause-Benchmarking Negotiation Copilot

ClausePilot is an AI-powered contract analysis and negotiation copilot specifically built for freelancers, independent contractors, and gig economy workers. It extracts clauses, benchmarks them against a curated corpus of market-standard terms, identifies asymmetric risks by severity, explains clauses in plain language, drafts strategic counter-proposals, and generates an attorney consultation checklist.

---

## GenAI Architecture Table

| Pipeline Stage | Model / Service | Purpose | Input / Prompt Context | Output Contract |
|---|---|---|---|---|
| **1. Extraction Agent** | Gemini 2.5 Flash | Parses raw contract text into structured clause objects | Contract text delimited as untrusted data | Structured JSON list of clauses |
| **2. Benchmark & Risk Agent** | Gemini 2.5 Flash + Text Embeddings | RAG comparison against standard corpus; deviation & severity scoring | Extracted clause + Top-3 nearest benchmark clauses | Severity (`high`/`medium`/`low`), risk score, deviation rationale |
| **3. Plain-Language Agent** | Gemini 2.5 Flash | Translates legalese into actionable freelancer impact | Legal clause text + identified risk points | Plain-English summary, hidden trap warnings |
| **4. Negotiation-Message Agent** | Gemini 2.5 Flash | Generates tailored counter-proposal emails | Top flagged clause + selected tone (`diplomatic`, `firm`, `direct`) + benchmark target | Email subject, polite & persuasive body, proposed replacement clause |
| **5. Attorney Prep Agent** | Gemini 2.5 Flash | Formulates targeted questions for formal legal consultation | Grouped high-severity clauses & legal questions | Prioritized question list, billable time saved estimate |

## System Architecture & Data Model
Detailed technical documentation on the data models, Pydantic schemas, and in-memory RAG retrieval engine is available in [`docs/architecture.md`](file:///docs/architecture.md).

### Benchmark Corpus Design (28 Curated Standard Clauses)
The application includes a self-contained, version-controlled benchmark corpus stored in `data/benchmark_corpus.json` (173 KB, well within the 10 MB repository budget). The corpus spans 7 core freelance contractual domains:
1. **Termination & Cancellation** (Mutual 30-day notice, cure period, WIP compensation, kill fees)
2. **Payment Terms & Invoicing** (Net-30/Net-15 standards, late interest charges, service suspension, deemed acceptance windows)
3. **Intellectual Property** (Payment-conditional assignment, pre-existing IP carve-outs, portfolio display rights)
4. **Non-Compete & Exclusivity** (Non-exclusive status, elimination of post-termination non-competes, narrow non-solicitation)
5. **Limitation of Liability** (Fee-capped mutual liability, exclusion of consequential damages, personal liability immunity)
6. **Indemnification & Warranties** (Fault-based IP indemnity, mutual gross negligence, carve-out for client assets)
7. **Dispute Resolution & Governing Law** (Mandatory 30-day informal talks, neutral/small claims venue, legal fee recovery)

---

## Disclaimer
**Informational tool · Not formal legal advice.** ClausePilot provides legal education, benchmark comparisons, and drafting assistance for negotiation purposes only.
