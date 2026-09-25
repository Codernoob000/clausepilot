"""ClausePilot End-to-End Analysis Pipeline & Session Manager."""

import os
import time
import math
import uuid
import logging
import threading
from typing import Dict, Any, Optional, List
from app.schemas import (
    AnalysisStatus,
    FullAnalysisResult,
    AnalyzedClause,
    RawExtractedClause,
    CounterDraftResponse,
    AttorneyPrepResponse
)
from app.rag import retriever
from app.llm import (
    call_1_extraction_agent,
    call_2_benchmark_risk_agent,
    call_3_plain_language_agent,
    call_4_negotiation_message_agent,
    call_5_attorney_prep_agent
)

logger = logging.getLogger("clausepilot.pipeline")

class SessionManager:
    """Thread-safe in-memory session and cache store."""

    def __init__(self):
        self._lock = threading.Lock()
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, filename: str = "Uploaded_Contract.pdf") -> str:
        session_id = uuid.uuid4().hex[:10]
        with self._lock:
            self.sessions[session_id] = {
                "session_id": session_id,
                "filename": filename,
                "page_count": 1,
                "status": AnalysisStatus(
                    stage=1,
                    stage_label="Reading & Structuring Document",
                    percent=10,
                    eta_seconds=12,
                    completed=False,
                    page_count=1,
                    clauses_found_so_far=0
                ),
                "result": None,
                "attorney_prep": None,
                "counter_drafts": {},
                "created_at": time.time()
            }
        return session_id

    def update_status(self, session_id: str, **kwargs):
        with self._lock:
            if session_id in self.sessions:
                curr = self.sessions[session_id]["status"].model_dump()
                curr.update(kwargs)
                self.sessions[session_id]["status"] = AnalysisStatus(**curr)

    def get_status(self, session_id: str) -> Optional[AnalysisStatus]:
        with self._lock:
            sess = self.sessions.get(session_id)
            return sess["status"] if sess else None

    def set_result(self, session_id: str, result: FullAnalysisResult, attorney_prep: AttorneyPrepResponse):
        with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id]["result"] = result
                self.sessions[session_id]["attorney_prep"] = attorney_prep
                self.sessions[session_id]["status"] = AnalysisStatus(
                    stage=4,
                    stage_label="Drafting Negotiation Scripts Complete",
                    percent=100,
                    eta_seconds=0,
                    completed=True,
                    page_count=result.page_count,
                    clauses_found_so_far=result.clause_count
                )

    def get_result(self, session_id: str) -> Optional[FullAnalysisResult]:
        with self._lock:
            sess = self.sessions.get(session_id)
            return sess["result"] if sess else None

    def get_attorney_prep(self, session_id: str) -> Optional[AttorneyPrepResponse]:
        with self._lock:
            sess = self.sessions.get(session_id)
            return sess["attorney_prep"] if sess else None

    def get_counter_draft(self, session_id: str, clause_id: str, tone: str) -> Optional[CounterDraftResponse]:
        key = f"{clause_id}_{tone}"
        with self._lock:
            sess = self.sessions.get(session_id)
            if not sess:
                return None
            return sess["counter_drafts"].get(key)

    def set_counter_draft(self, session_id: str, clause_id: str, tone: str, draft: CounterDraftResponse):
        key = f"{clause_id}_{tone}"
        with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id]["counter_drafts"][key] = draft


sessions = SessionManager()


def execute_full_pipeline(session_id: str, contract_text: str, filename: str):
    """Executes the 5-stage GenAI pipeline asynchronously."""
    try:
        page_estimate = max(1, math.ceil(len(contract_text) / 2500))
        sessions.update_status(
            session_id,
            stage=1,
            stage_label="Reading & Structuring Document",
            percent=15,
            eta_seconds=10,
            page_count=page_estimate,
            clauses_found_so_far=0
        )

        # --- STAGE 1: Clause Extraction (Call 1) ---
        extraction_res = call_1_extraction_agent(contract_text)
        raw_clauses_data = extraction_res.get("clauses", [])
        jurisdiction = extraction_res.get("jurisdiction", "California")

        raw_clauses = [RawExtractedClause(**c) for c in raw_clauses_data]
        sessions.update_status(
            session_id,
            stage=2,
            stage_label="Benchmarking Against Market Standards",
            percent=40,
            eta_seconds=7,
            clauses_found_so_far=len(raw_clauses)
        )

        # --- STAGE 2: RAG Comparison & Deviation Scoring (Call 2 & Call 3) ---
        from concurrent.futures import ThreadPoolExecutor

        def process_single_clause(raw_clause: RawExtractedClause) -> AnalyzedClause:
            matches = retriever.search(raw_clause.original_text, top_k=2, category=raw_clause.category)
            bench_res = call_2_benchmark_risk_agent(raw_clause, matches)
            plain_eng = call_3_plain_language_agent(
                raw_clause.title,
                raw_clause.original_text,
                bench_res.get("severity", "low"),
                bench_res.get("rationale", "")
            )
            return AnalyzedClause(
                id=raw_clause.id,
                section=raw_clause.section,
                title=raw_clause.title,
                category=raw_clause.category,
                severity=bench_res.get("severity", "low"),
                original_text=raw_clause.original_text,
                plain_english=plain_eng,
                market_standard_text=bench_res.get("market_standard_text", matches[0].standard_text if matches else "Standard balanced term."),
                market_adoption_pct=bench_res.get("market_adoption_pct", matches[0].market_adoption_pct if matches else 85),
                rationale=bench_res.get("rationale", "Standard clause."),
                deviation_points=bench_res.get("deviation_points", [])
            )

        analyzed_clauses: List[AnalyzedClause] = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            analyzed_clauses = list(executor.map(process_single_clause, raw_clauses))

        sessions.update_status(
            session_id,
            stage=3,
            stage_label="Identifying Unfavorable Terms",
            percent=75,
            eta_seconds=3
        )

        # Compute overall contract risk score (0 to 100)
        flagged = [c for c in analyzed_clauses if c.severity in ("high", "medium")]
        high_count = sum(1 for c in analyzed_clauses if c.severity == "high")
        med_count = sum(1 for c in analyzed_clauses if c.severity == "medium")
        total_clauses = max(1, len(analyzed_clauses))
        high_ratio = high_count / total_clauses
        med_ratio = med_count / total_clauses

        # Base penalty from absolute flags + ratio penalty
        penalty = (high_count * 20) + (med_count * 8) + int(high_ratio * 30) + int(med_ratio * 12)
        computed_risk = max(18, 95 - penalty)

        # Enforce realistic ceiling if severe risks exist
        if high_count >= 2:
            computed_risk = min(computed_risk, 42)
        elif high_count == 1:
            computed_risk = min(computed_risk, 54)
        elif med_count >= 1:
            computed_risk = min(computed_risk, 72)

        if computed_risk >= 75:
            risk_label = "Safe"
        elif computed_risk >= 55:
            risk_label = "Fair"
        elif computed_risk >= 35:
            risk_label = "Risky"
        else:
            risk_label = "Critical"

        sessions.update_status(
            session_id,
            stage=4,
            stage_label="Drafting Negotiation Scripts",
            percent=90,
            eta_seconds=2
        )

        # --- STAGE 4: Negotiation Message & Attorney Prep Generation (Call 4 & 5) ---
        top_flagged = flagged[0] if flagged else analyzed_clauses[0]
        # Pre-generate default diplomatic counter draft for the top clause
        default_counter = call_4_negotiation_message_agent(top_flagged, tone="diplomatic")
        sessions.set_counter_draft(session_id, top_flagged.id, "diplomatic", default_counter)

        # Call 5: Attorney Prep
        attorney_prep = call_5_attorney_prep_agent(session_id, filename, jurisdiction, flagged or analyzed_clauses[:3])

        full_result = FullAnalysisResult(
            session_id=session_id,
            filename=filename,
            page_count=page_estimate,
            clause_count=len(analyzed_clauses),
            flagged_count=len(flagged),
            risk_score=computed_risk,
            risk_label=risk_label, # type: ignore
            jurisdiction=jurisdiction,
            clauses=analyzed_clauses
        )

        sessions.set_result(session_id, full_result, attorney_prep)
        logger.info(f"Pipeline complete for session {session_id}. Score: {computed_risk}, Flagged: {len(flagged)}")

    except Exception as e:
        logger.error(f"Pipeline error for session {session_id}: {e}", exc_info=True)
        # Mark as completed with fallback so user is not stuck
        sessions.update_status(
            session_id,
            stage=4,
            stage_label="Analysis Complete",
            percent=100,
            eta_seconds=0,
            completed=True
        )
