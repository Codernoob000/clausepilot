"""ClausePilot FastAPI Application and Serving Layer."""

import os
import io
import json
import logging
import threading
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Query, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.schemas import AnalysisStatus, FullAnalysisResult, CounterDraftResponse, AttorneyPrepResponse
from app.pipeline import sessions, execute_full_pipeline
from app.extractors import extract_text_from_file
from app.security import validate_file_upload, sanitize_filename, sanitize_contract_text, rate_limiter
from app.llm import call_4_negotiation_message_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clausepilot.main")

app = FastAPI(
    title="ClausePilot API",
    description="Clause-Benchmarking Negotiation Copilot for Freelance & Gig Contracts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
SAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "samples")

SAMPLE_FILES = {
    "design-agency-msa": "design-agency-msa.txt",
    "agency": "design-agency-msa.txt",
    "tech-startup-contractor": "tech-startup-contractor.txt",
    "contractor": "tech-startup-contractor.txt",
    "content-media-retainer": "content-media-retainer.txt",
    "licensing": "content-media-retainer.txt"
}


# --- Health Check ---

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "ClausePilot",
        "version": "1.0.0",
        "disclaimer": "Informational tool · Not formal legal advice"
    }


# --- API Endpoints per frontend-wiring-spec.md ---

class AnalyzeSampleRequest(BaseModel):
    sample_id: Optional[str] = None

@app.post("/api/analyze")
async def analyze_document(
    request: Request,
    file: Optional[UploadFile] = File(None),
):
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Too many analysis requests. Please wait a minute.")

    contract_text = ""
    filename = "Uploaded_Contract.pdf"

    # Check if request has JSON body (sample contract)
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            sample_id = body.get("sample_id", "design-agency-msa")
            sample_file = SAMPLE_FILES.get(sample_id, "design-agency-msa.txt")
            sample_path = os.path.join(SAMPLES_DIR, sample_file)
            
            if not os.path.exists(sample_path):
                raise HTTPException(status_code=404, detail=f"Sample contract '{sample_id}' not found.")
            
            with open(sample_path, "r", encoding="utf-8") as f:
                contract_text = f.read()
            
            filename = sample_file.replace("-", "_").title().replace(".Txt", ".pdf")
        except Exception as e:
            logger.error(f"Error loading sample: {e}")
            raise HTTPException(status_code=400, detail=str(e))

    elif file:
        clean_filename = sanitize_filename(file.filename or "contract.txt")
        file_bytes = await file.read()
        
        # Security validation (Phase 3)
        valid, msg = validate_file_upload(clean_filename, file_bytes)
        if not valid:
            raise HTTPException(status_code=400, detail=msg)
            
        try:
            contract_text, _ = extract_text_from_file(clean_filename, file_bytes)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Extraction failed: {e}")
            
        filename = clean_filename
    else:
        raise HTTPException(status_code=400, detail="No file or sample_id provided.")

    if not contract_text or len(contract_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Document text is empty or could not be parsed.")

    # Sanitize and guard against injection (Phase 3)
    sanitized_text = sanitize_contract_text(contract_text)

    # Initialize session and kick off async pipeline (Phase 2)
    session_id = sessions.create_session(filename=filename)
    
    worker = threading.Thread(
        target=execute_full_pipeline,
        args=(session_id, sanitized_text, filename),
        daemon=True
    )
    worker.start()

    return {"session_id": session_id}


@app.get("/api/status/{session_id}")
def get_analysis_status(session_id: str):
    status_obj = sessions.get_status(session_id)
    if not status_obj:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return status_obj.model_dump()


@app.get("/api/results/{session_id}")
def get_analysis_results(session_id: str):
    res = sessions.get_result(session_id)
    if not res:
        # Check if still processing
        status_obj = sessions.get_status(session_id)
        if status_obj and not status_obj.completed:
            return JSONResponse(status_code=202, content={"status": "processing", "stage": status_obj.stage})
        raise HTTPException(status_code=404, detail=f"Results for session '{session_id}' not found.")
    return res.model_dump()


@app.get("/api/counter_draft/{session_id}")
def get_counter_draft(
    session_id: str,
    clause_id: Optional[str] = Query(None),
    tone: str = Query("diplomatic")
):
    if tone not in ("diplomatic", "firm", "direct"):
        tone = "diplomatic"

    res = sessions.get_result(session_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    target_clause = None
    if clause_id:
        target_clause = next((c for c in res.clauses if c.id == clause_id), None)
    
    if not target_clause:
        # Pick top flagged clause
        flagged = [c for c in res.clauses if c.severity in ("high", "medium")]
        target_clause = flagged[0] if flagged else res.clauses[0]

    # Check cache first
    cached = sessions.get_counter_draft(session_id, target_clause.id, tone)
    if cached:
        return cached.model_dump()

    # Generate counter draft
    draft = call_4_negotiation_message_agent(target_clause, tone=tone)
    sessions.set_counter_draft(session_id, target_clause.id, tone, draft)
    return draft.model_dump()


@app.get("/api/attorney_prep/{session_id}")
def get_attorney_prep_sheet(session_id: str):
    prep = sessions.get_attorney_prep(session_id)
    if not prep:
        raise HTTPException(status_code=404, detail=f"Attorney prep sheet for session '{session_id}' not found.")
    return prep.model_dump()


# --- HTML Screen Routes ---

def _render_template(screen_file: str) -> HTMLResponse:
    path = os.path.join(TEMPLATES_DIR, screen_file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Template {screen_file} not found.")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)


@app.get("/", response_class=HTMLResponse)
@app.get("/screen1.html", response_class=HTMLResponse)
@app.get("/upload", response_class=HTMLResponse)
def serve_screen1():
    return _render_template("screen1.html")


@app.get("/screen2.html", response_class=HTMLResponse)
@app.get("/analysis", response_class=HTMLResponse)
def serve_screen2():
    return _render_template("screen2.html")


@app.get("/screen3.html", response_class=HTMLResponse)
@app.get("/breakdown", response_class=HTMLResponse)
def serve_screen3():
    return _render_template("screen3.html")


@app.get("/screen4.html", response_class=HTMLResponse)
@app.get("/counter", response_class=HTMLResponse)
def serve_screen4():
    return _render_template("screen4.html")


@app.get("/screen5.html", response_class=HTMLResponse)
@app.get("/attorney-prep", response_class=HTMLResponse)
def serve_screen5():
    return _render_template("screen5.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
