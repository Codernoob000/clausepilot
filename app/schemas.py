"""ClausePilot Pydantic Schemas and Data Models."""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

# --- Phase 1: Benchmark Corpus Schema ---

class BenchmarkClause(BaseModel):
    id: str = Field(..., description="Unique identifier for the benchmark clause")
    category: str = Field(..., description="Legal category (e.g., Intellectual Property, Termination)")
    title: str = Field(..., description="Descriptive title of the standard provision")
    standard_text: str = Field(..., description="Market-standard balanced contract language")
    rationale: str = Field(..., description="Explanation of why this term is considered market-standard and fair")
    market_adoption_pct: int = Field(..., ge=0, le=100, description="Estimated percentage adoption across standard industry contracts")
    unfavorable_signals: List[str] = Field(default_factory=list, description="Key patterns/phrases that indicate one-sided or predatory deviations")
    embedding: Optional[List[float]] = Field(default=None, description="Precomputed dense embedding vector for semantic search")


class BenchmarkCorpus(BaseModel):
    version: str = "1.0.0"
    description: str = "Curated corpus of market-standard freelance and gig contract clauses"
    total_clauses: int
    categories: List[str]
    clauses: List[BenchmarkClause]


# --- Phase 2: Pipeline Extraction & Analysis Schemas ---

class RawExtractedClause(BaseModel):
    id: str = Field(..., description="Generated clause ID (e.g. clause-1)")
    section: str = Field(..., description="Section number or header (e.g. Section 4.2)")
    title: str = Field(..., description="Inferred clause topic or heading")
    category: str = Field(..., description="Classified category")
    original_text: str = Field(..., description="Exact extracted contract clause text")


class BenchmarkMatch(BaseModel):
    benchmark_id: str
    benchmark_title: str
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    standard_text: str
    market_adoption_pct: int
    rationale: str


class AnalyzedClause(BaseModel):
    id: str
    section: str
    title: str
    category: str
    severity: Literal["high", "medium", "low"] = Field(..., description="Risk severity rating")
    original_text: str
    plain_english: str = Field(..., description="Plain-language translation of freelancer impact")
    market_standard_text: str = Field(..., description="Balanced market-standard reference")
    market_adoption_pct: int = Field(..., ge=0, le=100)
    rationale: str = Field(..., description="Explanation of the deviation and risk")
    deviation_points: List[str] = Field(default_factory=list)


class AnalysisStatus(BaseModel):
    stage: int = Field(..., ge=1, le=4, description="1: Reading & Structuring, 2: Benchmarking, 3: Identifying Terms, 4: Drafting Scripts")
    stage_label: str
    percent: int = Field(..., ge=0, le=100)
    eta_seconds: int
    completed: bool
    page_count: int
    clauses_found_so_far: int


class FullAnalysisResult(BaseModel):
    session_id: str
    filename: str
    page_count: int
    clause_count: int
    flagged_count: int
    risk_score: int = Field(..., ge=0, le=100, description="0 (Dangerous) to 100 (Safe/Standard)")
    risk_label: Literal["Safe", "Fair", "Risky", "Critical"]
    jurisdiction: str
    clauses: List[AnalyzedClause]


# --- Counter-Draft Schema ---

class CounterDraftResponse(BaseModel):
    clause_id: str
    tone: Literal["diplomatic", "firm", "direct"]
    subject: str
    body: str
    proposed_clause: str
    predicted_acceptance_pct: int = Field(..., ge=0, le=100)


# --- Attorney Prep Schema ---

class AttorneyQuestionGroup(BaseModel):
    clause_id: str
    section: str
    priority: Literal["high", "medium", "low"]
    rationale: str
    questions: List[str]


class AttorneyPrepResponse(BaseModel):
    session_id: str
    agreement_name: str
    jurisdiction: str
    estimated_call_minutes: Any = Field(default_factory=lambda: [15, 25], description="[min_minutes, max_minutes]")
    billable_time_saved_estimate: str
    questions: List[AttorneyQuestionGroup]

    def model_post_init(self, __context: Any) -> None:
        if isinstance(self.estimated_call_minutes, (int, float)):
            val = int(self.estimated_call_minutes)
            self.estimated_call_minutes = [max(10, val - 5), val + 5]
        elif not isinstance(self.estimated_call_minutes, list):
            self.estimated_call_minutes = [15, 25]
