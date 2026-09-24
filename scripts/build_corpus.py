"""Build and embed the 28 benchmark clauses, saving to data/benchmark_corpus.json."""

import os
import sys
import json
import time
import urllib.request
import numpy as np

# Ensure root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.corpus_data import CORPUS_CLAUSES

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

def get_gemini_embedding(text: str) -> list:
    """Fetch dense embedding from Gemini API."""
    if not API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={API_KEY}"
    payload = {
        "model": "models/gemini-embedding-001",
        "content": {"parts": [{"text": text}]}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode())
        vec = res.get("embedding", {}).get("values", [])
        return vec

def build_offline_embedding(text: str, dim: int = 768) -> list:
    """Deterministic normalized pseudo-semantic hash embedding for robust fallback."""
    words = text.lower().split()
    vec = np.zeros(dim, dtype=np.float32)
    for i, word in enumerate(words):
        h = hash(word) % dim
        vec[h] += 1.0 / (1.0 + np.log(i + 1))
        # Add character bi-grams
        for j in range(len(word) - 1):
            bg_h = hash(word[j:j+2]) % dim
            vec[bg_h] += 0.5
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()

def main():
    os.makedirs("data", exist_ok=True)
    embedded_clauses = []
    print(f"Embedding {len(CORPUS_CLAUSES)} benchmark clauses...")

    use_gemini = bool(API_KEY)
    print(f"API key detected: {use_gemini}")

    for idx, clause in enumerate(CORPUS_CLAUSES):
        embed_input = f"{clause['category']} - {clause['title']}: {clause['standard_text']}. Rationale: {clause['rationale']}"
        vec = None
        if use_gemini:
            try:
                vec = get_gemini_embedding(embed_input)
                time.sleep(0.4) # respectful pacing
            except Exception as e:
                print(f"Warning: Failed to fetch API embedding for {clause['id']} ({e}), using fallback")

        if not vec:
            vec = build_offline_embedding(embed_input, dim=768)

        # Normalize and truncate to 768 dimensions for <250 KB storage budget
        v_np = np.array(vec[:768], dtype=np.float32)
        norm = np.linalg.norm(v_np)
        if norm > 0:
            v_np = v_np / norm
        
        clause_entry = dict(clause)
        clause_entry["embedding"] = [round(float(x), 4) for x in v_np.tolist()]
        embedded_clauses.append(clause_entry)
        print(f"[{idx+1}/{len(CORPUS_CLAUSES)}] Embedded {clause['id']}: {clause['title']} (dim={len(clause_entry['embedding'])})")

    corpus_payload = {
        "version": "1.0.0",
        "description": "Curated corpus of market-standard freelance and gig contract clauses for ClausePilot",
        "total_clauses": len(embedded_clauses),
        "categories": sorted(list(set(c["category"] for c in embedded_clauses))),
        "clauses": embedded_clauses
    }

    out_path = os.path.join("data", "benchmark_corpus.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(corpus_payload, f, separators=(',', ':'))

    size_kb = os.path.getsize(out_path) / 1024
    print(f"\nSaved benchmark corpus to {out_path} ({size_kb:.1f} KB, budget < 1000 KB).")

if __name__ == "__main__":
    main()
