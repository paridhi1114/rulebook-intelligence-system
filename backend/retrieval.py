"""
Hybrid retrieval engine over the rulebook.

Two complementary signals, fused:
  - Lexical  : BM25 (rank_bm25) over tokenised rule text — strong on exact terminology.
  - Semantic : Gemini text embeddings (gemini-embedding-001) with cosine similarity —
               strong on paraphrase / different wording. If no GEMINI_API_KEY is present
               (or the API errors), this transparently falls back to a TF-IDF vector-space
               cosine so the system keeps working.

Scores from both signals are min-max normalised per query and combined with a weighted sum.
Retrieval preserves full rule metadata so the reasoning layer and UI can cite
rule_id / chapter / section / subsection / exact_text precisely.
"""

import os
import re
import logging
from typing import List, Dict, Optional

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rulebook_data import get_rules
from embeddings import get_embeddings

logger = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall(text.lower())


def _minmax(arr: np.ndarray) -> np.ndarray:
    if arr.size == 0:
        return arr
    lo, hi = float(arr.min()), float(arr.max())
    if hi - lo < 1e-9:
        return np.zeros_like(arr)
    return (arr - lo) / (hi - lo)


class HybridRetriever:
    def __init__(self, cache_collection=None):
        self.rules: List[Dict] = get_rules()
        self.documents = [
            f"{r['chapter']} {r['section']} {r['subsection']} {r['title']}. {r['exact_text']}"
            for r in self.rules
        ]

        # --- Lexical index (always on) ---
        self._tokenized = [_tokenize(d) for d in self.documents]
        self.bm25 = BM25Okapi(self._tokenized)

        # --- TF-IDF (semantic fallback, always built so it's ready instantly) ---
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2), sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

        # --- Gemini embeddings (preferred semantic signal) ---
        self.embedder = get_embeddings(cache_collection=cache_collection)
        self.doc_embeddings: Optional[np.ndarray] = None
        self.semantic_backend = "tfidf"
        self.bm25_weight, self.semantic_weight = 0.5, 0.5
        if self.embedder.available:
            # Fast path: activate immediately only if the whole corpus is already cached
            # (no network). Otherwise leave TF-IDF active and let the caller build in the
            # background via ensure_semantic().
            mat = self.embedder.embed_documents(self.documents, cache_only=True)
            if mat is not None:
                self._activate_gemini(mat)
        logger.info("Semantic backend at init: %s", self.semantic_backend)

    def _activate_gemini(self, mat: np.ndarray):
        self.doc_embeddings = mat
        self.semantic_backend = "gemini"
        self.bm25_weight, self.semantic_weight = 0.45, 0.55
        logger.info("Semantic backend: Gemini embeddings (%s)", self.embedder.model)

    def ensure_semantic(self):
        """Blocking build of Gemini corpus embeddings (run in a background thread).
        No-op if already active or unavailable. Swaps the backend in on success."""
        if self.semantic_backend == "gemini" or not self.embedder.available:
            return
        mat = self.embedder.embed_documents(self.documents, cache_only=False)
        if mat is not None:
            self._activate_gemini(mat)
        else:
            logger.warning("Gemini embedding build incomplete; staying on TF-IDF for now.")

    def _semantic_scores(self, query: str) -> np.ndarray:
        if self.semantic_backend == "gemini" and self.doc_embeddings is not None:
            q = self.embedder.embed_query(query)
            if q is not None:
                # cosine — vectors are L2-normalised already, so this is a dot product.
                return self.doc_embeddings @ q
            # Gemini failed mid-flight: fall back to TF-IDF for this query.
            logger.warning("Gemini query embedding unavailable; using TF-IDF for this query.")
        q_vec = self.vectorizer.transform([query])
        return cosine_similarity(q_vec, self.tfidf_matrix).ravel()

    def retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        if not query.strip():
            return []

        bm25_scores = np.array(self.bm25.get_scores(_tokenize(query)), dtype=float)
        sem_scores = np.asarray(self._semantic_scores(query), dtype=float)

        fused = self.bm25_weight * _minmax(bm25_scores) + self.semantic_weight * _minmax(sem_scores)

        order = np.argsort(fused)[::-1][:top_k]
        results = []
        for rank, idx in enumerate(order):
            if fused[idx] <= 0:
                continue
            r = self.rules[idx]
            results.append(
                {
                    "rank": rank + 1,
                    "rule_id": r["rule_id"],
                    "chapter": r["chapter"],
                    "section": r["section"],
                    "subsection": r["subsection"],
                    "title": r["title"],
                    "exact_text": r["exact_text"],
                    "scores": {
                        "fused": round(float(fused[idx]), 4),
                        "bm25": round(float(bm25_scores[idx]), 4),
                        "semantic": round(float(sem_scores[idx]), 4),
                    },
                }
            )
        return results

    def info(self) -> Dict:
        return {
            "lexical": "bm25",
            "semantic_backend": self.semantic_backend,
            "embedding_model": self.embedder.model if self.semantic_backend == "gemini" else None,
            "weights": {"bm25": self.bm25_weight, "semantic": self.semantic_weight},
            "documents_indexed": len(self.documents),
        }


_retriever: Optional[HybridRetriever] = None


def get_retriever(cache_collection=None) -> HybridRetriever:
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever(cache_collection=cache_collection)
    return _retriever
