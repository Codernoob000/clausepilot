"""ClausePilot Retrieval-Augmented Generation (RAG) & Benchmark Retrieval Engine."""

import os
import json
import logging
import urllib.request
import numpy as np
from typing import List, Optional, Dict, Any
from app.schemas import BenchmarkMatch, BenchmarkClause

logger = logging.getLogger("clausepilot.rag")

CORPUS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "benchmark_corpus.json")
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

class BenchmarkRetriever:
    """In-memory vector retrieval engine for freelance standard clauses."""

    def __init__(self, corpus_path: str = CORPUS_PATH):
        self.corpus_path = corpus_path
        self.clauses: List[Dict[str, Any]] = []
        self.matrix: Optional[np.ndarray] = None
        self._load_corpus()

    def _load_corpus(self):
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found at {self.corpus_path}. Run scripts/build_corpus.py first.")
        
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.clauses = data.get("clauses", [])
        vectors = []
        for c in self.clauses:
            vec = c.get("embedding", [])
            vectors.append(vec)
        
        self.matrix = np.array(vectors, dtype=np.float32)
        # Verify normalization
        norms = np.linalg.norm(self.matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.matrix = self.matrix / norms

    def embed_text(self, text: str) -> np.ndarray:
        """Embed text using Gemini API or deterministic fallback."""
        key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or API_KEY
        vec = None
        if key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={key}"
                payload = {
                    "model": "models/gemini-embedding-001",
                    "content": {"parts": [{"text": text[:2000]}]}
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    res = json.loads(resp.read().decode())
                    raw_vec = res.get("embedding", {}).get("values", [])
                    if raw_vec:
                        vec = np.array(raw_vec[:768], dtype=np.float32)
            except Exception as e:
                logger.warning(f"Gemini embedding API call failed: {e}. Falling back to offline embedding.")

        if vec is None:
            # Deterministic word + char-ngram pseudo-embedding
            words = text.lower().split()
            dim = 768
            v = np.zeros(dim, dtype=np.float32)
            for i, word in enumerate(words):
                h = hash(word) % dim
                v[h] += 1.0 / (1.0 + np.log(i + 1))
                for j in range(len(word) - 1):
                    bg_h = hash(word[j:j+2]) % dim
                    v[bg_h] += 0.5
            vec = v

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def search(self, query_text: str, top_k: int = 3, category: Optional[str] = None) -> List[BenchmarkMatch]:
        """Retrieve the top-k most semantically similar benchmark clauses."""
        q_vec = self.embed_text(query_text)
        
        # Cosine similarity is the dot product of normalized vectors
        scores = np.dot(self.matrix, q_vec)
        
        # Keyword-based signal boosting for legal terms
        q_lower = query_text.lower()
        for idx, clause in enumerate(self.clauses):
            # Category match bonus
            if category and clause.get("category", "").lower() == category.lower():
                scores[idx] += 0.15
            # Unfavorable signals match bonus
            signals = clause.get("unfavorable_signals", [])
            for sig in signals:
                if sig.lower() in q_lower:
                    scores[idx] += 0.10
                    break

        ranked_indices = np.argsort(scores)[::-1]
        
        results: List[BenchmarkMatch] = []
        for i in ranked_indices:
            clause = self.clauses[i]
            if category and clause.get("category", "").lower() != category.lower() and len(results) < top_k - 1:
                # Prioritize category match when requested
                pass
            
            raw_score = float(scores[i])
            # Bound score between 0.0 and 1.0
            norm_score = max(0.0, min(1.0, (raw_score + 1.0) / 2.0 if raw_score <= 1.0 else 0.99))
            
            match = BenchmarkMatch(
                benchmark_id=clause["id"],
                benchmark_title=clause["title"],
                similarity_score=round(norm_score, 3),
                standard_text=clause["standard_text"],
                market_adoption_pct=clause["market_adoption_pct"],
                rationale=clause["rationale"]
            )
            results.append(match)
            if len(results) >= top_k:
                break
                
        return results

# Singleton retriever instance
retriever = BenchmarkRetriever()
