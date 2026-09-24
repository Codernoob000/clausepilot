# Frontend Wiring Spec — ClausePilot

Companion to `antigravity-master-prompt.md` Phase 4. This defines the API contract and, screen by screen, exactly which hardcoded element gets replaced with which real data field. Read this in full before touching any of the 5 HTML files.

---

## API Contract

All endpoints return JSON. `session_id` is generated on upload and threaded through every subsequent call and every screen's URL (e.g. `?session=abc123`).

### `POST /api/analyze`
Body: uploaded file (multipart) OR `{ "sample_id": "design-agency-msa" }` for the pre-loaded sample cards on screen 1.
Returns: `{ "session_id": "abc123" }`
Kicks off the Phase 2 pipeline asynchronously.

### `GET /api/status/{session_id}`
Poll every ~1s from the Analysis screen.
Returns:
```json
{
  "stage": 2,
  "stage_label": "Benchmarking Against Market Standards",
  "percent": 61,
  "eta_seconds": 8,
  "completed": false,
  "page_count": 14,
  "clauses_found_so_far": 22
}
```
`stage` is 1–4, matching the 4 diagnostic pipeline steps already laid out on screen 2 (Reading & Structuring → Benchmarking → Identifying Unfavorable Terms → Drafting Negotiation Scripts).

### `GET /api/results/{session_id}`
Returns the full analysis once `completed: true`:
```json
{
  "filename": "Apex_Creative_Studio_MSA_2025.pdf",
  "page_count": 14,
  "clause_count": 38,
  "flagged_count": 3,
  "risk_score": 64,
  "risk_label": "Fair",
  "jurisdiction": "California",
  "clauses": [
    {
      "id": "clause-9-4",
      "section": "Section 9.4",
      "title": "Broad IP Assignment & Pre-Existing Inventions",
      "category": "Intellectual Property",
      "severity": "high",
      "original_text": "...",
      "plain_english": "...",
      "market_standard_text": "...",
      "market_adoption_pct": 94,
      "rationale": "..."
    }
  ]
}
```
Every clause the UI needs a card for comes from this `clauses` array — the frontend must loop and render, not assume a fixed count of 3.

### `GET /api/counter_draft/{session_id}?clause_id=clause-9-4&tone=diplomatic`
`tone` is one of `diplomatic | firm | direct` (matches the existing tone-selector buttons on screen 4).
Returns:
```json
{
  "subject": "Re: Master Services Agreement - Minor clarifications",
  "body": "Hi ...",
  "predicted_acceptance_pct": 78
}
```
`predicted_acceptance_pct` must be a real computed value (see Screen 4 notes below), never a hardcoded constant.

### `GET /api/attorney_prep/{session_id}`
Returns:
```json
{
  "estimated_call_minutes": [18, 22],
  "billable_time_saved_estimate": "$250-$400",
  "questions": [
    {
      "clause_id": "clause-9-4",
      "section": "Section 9.4: Intellectual Property & Pre-Existing Assets",
      "priority": "high",
      "rationale": "...",
      "questions": ["...", "..."]
    }
  ]
}
```

---

## Screen-by-screen binding map

### Screen 1 — Upload
| Hardcoded element | Replace with |
|---|---|
| `uploaded-filename`, `uploaded-filesize` | Already set client-side on file select — on submit, POST the file to `/api/analyze`, then redirect to `screen2.html?session={session_id}` |
| Sample cards ("Design Agency MSA," "Tech Startup Contractor," "Content & Media Retainer") | Keep as 3 real pre-loaded sample contracts stored server-side; clicking calls `POST /api/analyze` with the matching `sample_id` instead of a file upload |
| "12,400+ verified freelance agreements," "4,200+" trust-copy | These are marketing copy, not per-analysis data — fine to leave static, **but** reword or match them to your actual benchmark corpus size (25–30 clauses) so they don't overclaim if a judge asks how big the corpus really is |

### Screen 2 — Analysis
| Hardcoded element | Replace with |
|---|---|
| `initProgressSimulator()` (fake interval starting at 78%) | Delete this function. Replace with a poller calling `GET /api/status/{session_id}` every ~1s, updating `progress-fill` width, `progress-percent-label`, `live-eta`, `countdown-num` from the real response |
| The 4 "Diagnostic Pipeline Breakdown" step states (Completed/In Progress/Queued) | Derive from `stage` in the status response — steps `< stage` are Completed, `== stage` is In Progress, `> stage` are Queued |
| "38 Clauses found," "14 Pages" header | Bind to `page_count` / `clauses_found_so_far` from the status response |
| "Live Discovery Stream" flagged-concern cards | Simplify for the demo: show a generic "Scanning clause {n} of {total}" ticker rather than trying to stream real partial clause content — full streaming here is scope creep for a hackathon timeline |
| "View Early Results" button | On `completed: true`, auto-redirect to `screen3.html?session={session_id}` |

### Screen 3 — Clause Breakdown
| Hardcoded element | Replace with |
|---|---|
| Summary cards (38 clauses mapped, 3 flagged, 64/100 market standard, "IP Retained & Net-30") | Bind to `clause_count`, `flagged_count`, `risk_score`/`risk_label` from `/api/results` |
| `clause-card-1/2/3` (fixed 3 cards) | Delete the fixed cards; render one card per entry in the `clauses` array, generating each card's DOM id dynamically (`clause-card-{id}`) so the existing `toggleClause(cardId)` function keeps working unmodified |
| Each card's 3-panel view (As Written / Plain-English Impact / Balanced Market Standard) | Bind to `clause.original_text`, `clause.plain_english`, `clause.market_standard_text` |
| "Market Adoption 6% of industry MSA drafts" / "Freelancer Benchmark Baseline 94%" | Bind to `clause.market_adoption_pct` and the corresponding rationale text |
| "Generate Counter-Draft" button | Link to `screen4.html?session={session_id}&clause={top_flagged_clause_id}` |

### Screen 4 — Counter-Draft
| Hardcoded element | Replace with |
|---|---|
| `toneData` object (3 fixed full emails for "Elena"/"Apex Studio") | Delete the static object. On tone-button click, call `GET /api/counter_draft?clause_id=...&tone=...` and populate `email-subject`/`email-body` from the response |
| "Predicted Acceptance 82%" | This is the single most obviously-fake stat if left static — bind to `predicted_acceptance_pct`, computed server-side from something real (e.g. a simple heuristic: base 70%, − 5 per high-severity flag on that clause, + adjustment for how far the clause deviates from `market_adoption_pct`). It must visibly change between different clauses/contracts |
| "Priority 1 of 3 to Counter" + next/prev arrows | Page through the real `flagged_count`, re-calling the counter-draft endpoint per clause as the user steps through |
| "Original Agreement Text" / "Proposed Smart Counter" panels | Bind to the selected clause's `original_text` and the counter-draft response's proposed replacement text |
| Benchmark Intel panel (Payment Term Distribution %, IP Carve-Out %) | Compute once from your real benchmark corpus (Phase 1) and inject as real numbers — these should be consistent across all contracts since they describe the corpus, not the uploaded document |

### Screen 5 — Attorney Prep
| Hardcoded element | Replace with |
|---|---|
| Header stats (agreement name, jurisdiction, flagged count, estimated call time) | Bind to `/api/results` + `/api/attorney_prep` fields |
| Question groups per section | Render from `/api/attorney_prep`'s `questions` array, grouped by `clause_id` |
| Checkboxes, meeting notes textarea, localStorage persistence | No backend needed — keep as-is, purely client-side |
| "Save up to 45 min of billable time ($250-$400 value)" | Keep as static illustrative copy, but note it in the README as an assumption/estimate, not a verified or computed figure — this satisfies the submission's "assumptions made" requirement rather than making it look like a real calculation |

---

## Cross-cutting fixes (apply to all 5 screens)

- Top bar document name ("Master Services Agreement – Apex ... v1.2") — bind to the real uploaded `filename` from `/api/results`, truncated if needed.
- Top bar user name/avatar ("Maya Lin, Product Designer") — this is leftover Stitch placeholder persona data; either wire to a real "Demo User" label or remove it entirely. Do not ship a fabricated real-sounding name in a legal-facing product.
- Every screen's step nav (1. Upload … 5. Attorney Prep) and the back/forward arrows must carry `?session={session_id}` in their links so navigation never loses the analysis in progress.
- The "Informational tool · Not formal legal advice" badge in the top bar must remain untouched on every screen — do not let any wiring change remove or obscure it.

## Phase 4 exit check (in addition to the master prompt's checklist)
Before moving to Phase 5, grep the final shipped HTML/JS for these literal strings and confirm none remain outside the two explicitly-allowed static-copy exceptions above: `Apex`, `Elena`, `Maya Lin`, `82%`, `94%`, `38 Clauses`. Their presence means a hardcoded value wasn't actually wired.
