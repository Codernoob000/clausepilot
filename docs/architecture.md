# ClausePilot System Architecture & Data Model

ClausePilot is an AI-powered contract analysis and negotiation copilot designed specifically for freelancers, independent contractors, and gig-economy talent.

---

## 1. System Architecture Overview

```
                      +---------------------------------------+
                      |   Client Web UI (Tailwind / HTML5)    |
                      |   - Screen 1: Upload & Samples        |
                      |   - Screen 2: Diagnostic Analysis     |
                      |   - Screen 3: Clause Risk Breakdown   |
                      |   - Screen 4: Counter-Draft Strategy  |
                      |   - Screen 5: Attorney Prep Sheet     |
                      +-------------------+-------------------+
                                          |
                                   REST / JSON API
                                          |
                      +-------------------v-------------------+
                      |       FastAPI Application Core        |
                      |       - Asynchronous Pipeline Mgr     |
                      |       - In-Memory Session Store       |
                      |       - Security Delimiting & Guard   |
                      +-------------------+-------------------+
                                          |
         +--------------------------------+--------------------------------+
         |                                                                 |
+--------v----------------------+                       +------------------v------------------+
|   In-Memory RAG Engine        |                       |    GenAI Multi-Agent Pipeline       |
|   - 28 Curated Standard Terms |                       |    - Call 1: Extraction Agent       |
|   - 768-dim Dense Vectors     |                       |    - Call 2: Benchmark & Risk Agent |
|   - Hybrid Signal Boosting    |                       |    - Call 3: Plain-Language Agent   |
|   - < 250 KB Memory Footprint |                       |    - Call 4: Negotiation Message    |
+-------------------------------+                       |    - Call 5: Attorney Prep Agent    |
                                                        +-------------------------------------+
```

---

## 2. Benchmark Corpus Taxonomy (28 Standard Clauses)

The benchmark corpus represents market-standard terms across 7 freelance contract pillars:

1. **Termination & Cancellation (4 Clauses)**
   - `std-term-01`: Mutual 30-Day Notice for Convenience (88% market adoption)
   - `std-term-02`: Cause Termination with 10-Day Cure Period (91% market adoption)
   - `std-term-03`: Payment for Work-in-Progress Upon Termination (95% market adoption)
   - `std-term-04`: Kill Fee for Sudden Mid-Project Cancellation (76% market adoption)

2. **Payment Terms & Invoicing (5 Clauses)**
   - `std-pay-01`: Net-30 Payment Window (82% market adoption)
   - `std-pay-02`: Net-15 Accelerated Freelancer Terms (68% market adoption)
   - `std-pay-03`: Late Payment Interest Fee (79% market adoption)
   - `std-pay-04`: Right to Suspend Services for Past-Due Accounts (86% market adoption)
   - `std-pay-05`: 10-Day Milestone Acceptance Window & Deemed Acceptance (84% market adoption)

3. **Intellectual Property & Work Product (5 Clauses)**
   - `std-ip-01`: IP Assignment Conditioned Upon Full Payment (94% market adoption)
   - `std-ip-02`: Carve-Out of Pre-Existing IP & Reusable Tools (92% market adoption)
   - `std-ip-03`: Portfolio & Case Study Showcase Rights (89% market adoption)
   - `std-ip-04`: Limited Commercial Moral Rights Waiver (74% market adoption)
   - `std-ip-05`: General Skill & Knowledge Retention (88% market adoption)

4. **Non-Compete & Exclusivity (3 Clauses)**
   - `std-comp-01`: Non-Exclusive Independent Contractor Status (96% market adoption)
   - `std-comp-02`: No Post-Termination Industry Non-Compete (93% market adoption)
   - `std-comp-03`: Narrow Client & Staff Non-Solicitation (81% market adoption)

5. **Limitation of Liability & Damages (4 Clauses)**
   - `std-liab-01`: Liability Capped at Total Fees Paid (89% market adoption)
   - `std-liab-02`: Mutual Exclusion of Consequential & Indirect Damages (92% market adoption)
   - `std-liab-03`: Exclusion of Personal Liability (90% market adoption)
   - `std-liab-04`: One-Year Statute of Limitations on Claims (78% market adoption)

6. **Indemnification & Warranties (3 Clauses)**
   - `std-ind-01`: Indemnification Limited to Willful IP Infringement (83% market adoption)
   - `std-ind-02`: Mutual Indemnification for Gross Negligence (87% market adoption)
   - `std-ind-03`: Carve-Out for Client-Supplied Assets & Unauthorized Edits (91% market adoption)

7. **Dispute Resolution & Governing Law (4 Clauses)**
   - `std-disp-01`: 30-Day Mandatory Good-Faith Negotiation (85% market adoption)
   - `std-disp-02`: Binding Neutral Arbitration or Small Claims Option (79% market adoption)
   - `std-disp-03`: Home or Mutual Jurisdiction (72% market adoption)
   - `std-disp-04`: Prevailing Party Legal Fee Recovery (84% market adoption)

---

## 3. Data Models & JSON Schemas

All schemas are strictly typed with Pydantic v2 in `app/schemas.py`:

- **`BenchmarkClause`**: `id`, `category`, `title`, `standard_text`, `rationale`, `market_adoption_pct`, `unfavorable_signals`, `embedding`
- **`RawExtractedClause`**: `id`, `section`, `title`, `category`, `original_text`
- **`BenchmarkMatch`**: `benchmark_id`, `benchmark_title`, `similarity_score`, `standard_text`, `market_adoption_pct`, `rationale`
- **`AnalyzedClause`**: `id`, `section`, `title`, `category`, `severity`, `original_text`, `plain_english`, `market_standard_text`, `market_adoption_pct`, `rationale`, `deviation_points`
- **`FullAnalysisResult`**: `session_id`, `filename`, `page_count`, `clause_count`, `flagged_count`, `risk_score`, `risk_label`, `jurisdiction`, `clauses`
- **`CounterDraftResponse`**: `clause_id`, `tone`, `subject`, `body`, `proposed_clause`, `predicted_acceptance_pct`
- **`AttorneyPrepResponse`**: `session_id`, `agreement_name`, `jurisdiction`, `estimated_call_minutes`, `billable_time_saved_estimate`, `questions`

---

## 4. RAG Retrieval Strategy

The in-memory retrieval engine uses normalized cosine similarity over 768-dimensional dense vectors with legal keyword signal boosting:
1. Dense vector dot product against precomputed benchmark embeddings.
2. Category matching bonus (+0.15) when section categories are detected.
3. Unfavorable legal signal boosting (+0.10) when known abusive terms (e.g., "perpetual", "immediate without cause", "work-for-hire prior to payment") are detected.
4. Top-k reranking ensuring optimal semantic match selection.
