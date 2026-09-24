"""End-to-End Pipeline Validation Script for Phase 2."""

import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.pipeline import sessions, execute_full_pipeline
from app.schemas import FullAnalysisResult, CounterDraftResponse, AttorneyPrepResponse
from app.llm import call_4_negotiation_message_agent

def main():
    sample_path = os.path.join("data", "samples", "design-agency-msa.txt")
    print(f"Loading sample contract: {sample_path}")
    with open(sample_path, "r", encoding="utf-8") as f:
        contract_text = f.read()

    session_id = sessions.create_session(filename="Apex_Creative_Studio_MSA_2025.txt")
    print(f"Created session: {session_id}")

    start_t = time.time()
    print("Executing full GenAI pipeline...")
    execute_full_pipeline(session_id, contract_text, "Apex_Creative_Studio_MSA_2025.txt")
    elapsed = time.time() - start_t
    print(f"Pipeline finished in {elapsed:.2f} seconds.")

    status = sessions.get_status(session_id)
    print(f"Final Status: completed={status.completed}, stage={status.stage}, percent={status.percent}%")

    result = sessions.get_result(session_id)
    assert result is not None, "Error: Analysis result is None!"
    
    print("\n--- Pipeline Summary ---")
    print(f"Filename: {result.filename}")
    print(f"Clauses extracted: {result.clause_count}")
    print(f"Flagged risky clauses: {result.flagged_count}")
    print(f"Risk Score: {result.risk_score} / 100 ({result.risk_label})")
    print(f"Jurisdiction: {result.jurisdiction}")

    # Spot-check at least 3 flagged clauses
    flagged = [c for c in result.clauses if c.severity in ("high", "medium")]
    print(f"\n--- Spot-Checking {min(3, len(flagged))} Flagged Clauses ---")
    for i, c in enumerate(flagged[:3], 1):
        print(f"\n[Check #{i}] {c.section}: {c.title} ({c.severity.upper()} RISK)")
        print(f"  Original Text Excerpt: {c.original_text[:120]}...")
        print(f"  Plain English: {c.plain_english}")
        print(f"  Market Benchmark: {c.market_adoption_pct}% adoption ({c.market_standard_text[:90]}...)")
        print(f"  Rationale: {c.rationale}")

    # Test Counter-Draft generation across tones
    top_clause = flagged[0] if flagged else result.clauses[0]
    print(f"\n--- Testing Counter-Draft Generation on {top_clause.title} ---")
    for tone in ["diplomatic", "firm", "direct"]:
        counter = call_4_negotiation_message_agent(top_clause, tone=tone)
        print(f"\n[Tone: {tone.upper()}] Predicted Acceptance: {counter.predicted_acceptance_pct}%")
        print(f"  Subject: {counter.subject}")
        print(f"  Body Preview: {counter.body[:150]}...")
        print(f"  Proposed Replacement: {counter.proposed_clause[:100]}...")

    # Test Attorney Prep output
    attorney_prep = sessions.get_attorney_prep(session_id)
    assert attorney_prep is not None, "Error: Attorney Prep is None!"
    print("\n--- Attorney Prep Validation ---")
    print(f"Estimated Call Minutes: {attorney_prep.estimated_call_minutes}")
    print(f"Billable Time Saved: {attorney_prep.billable_time_saved_estimate}")
    print(f"Question Groups Count: {len(attorney_prep.questions)}")
    for qg in attorney_prep.questions[:2]:
        print(f"  Section: {qg.section} (Priority: {qg.priority})")
        for q in qg.questions:
            print(f"    - {q}")

    print("\nPhase 2 Pipeline Execution: SUCCESS!")

if __name__ == "__main__":
    main()
