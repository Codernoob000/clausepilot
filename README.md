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

---

## Disclaimer
**Informational tool · Not formal legal advice.** ClausePilot provides legal education, benchmark comparisons, and drafting assistance for negotiation purposes only.
