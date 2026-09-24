"""ClausePilot FastAPI Application Entrypoint."""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ClausePilot API",
    description="Clause-Benchmarking Negotiation Copilot for Freelancers",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_class=JSONResponse)
def health_check():
    return {
        "status": "healthy",
        "app": "ClausePilot",
        "version": "1.0.0",
        "disclaimer": "Informational tool · Not formal legal advice"
    }

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ClausePilot Pipeline Check</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white flex items-center justify-center min-h-screen">
        <div class="max-w-md p-8 bg-slate-800 rounded-2xl border border-slate-700 shadow-2xl text-center">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold mb-4 border border-emerald-500/20">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Pipeline Verified
            </div>
            <h1 class="text-2xl font-bold tracking-tight mb-2">ClausePilot</h1>
            <p class="text-slate-400 text-sm mb-6">Clause-benchmarking negotiation copilot for freelance contracts.</p>
            <div class="p-3 bg-slate-900/60 rounded-lg text-xs text-slate-400 border border-slate-700">
                Informational tool · Not formal legal advice
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
