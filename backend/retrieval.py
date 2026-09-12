"""
Hybrid retrieval engine over the rulebook.

Combines:
  - Lexical retrieval  : BM25 (rank_bm25) over tokenised rule text.
  - Vector retrieval   : TF-IDF character/word n-gram vectors with cosine similarity,
                         a genuine vector-space semantic representation.

Scores from both retrievers are min-max normalised and fused (weighted sum) so that a
passage strong on either signal surfaces. Retrieval preserves full rule metadata so the
reasoning layer and UI can cite rule_id / chapter / section / exact_text.
"""

import re
from typing import List, Dict

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rulebook_data import get_rules

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
    def __init__(self, bm25_weight: float = 0.5, vector_weight: float = 0.5):
        self.bm25_weight = bm25_weight
        self.vector_weight = vector_weight
        self.rules: List[Dict] = get_rules()

        # A rule's searchable document is its title + exact_text (+ chapter/section context).
        self.documents = [
            f"{r['chapter']} {r['section']} {r['subsection']} {r['title']}. {r['exact_text']}"
            for r in self.rules
        ]

        self._tokenized = [_tokenize(d) for d in self.documents]
        self.bm25 = BM25Okapi(self._tokenized)

        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2), sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query: str, top_k: int = 8) -> List[Dict]:
        if not query.strip():
            return []

        # Lexical scores
        bm25_scores = np.array(self.bm25.get_scores(_tokenize(query)), dtype=float)

        # Vector / semantic scores
        q_vec = self.vectorizer.transform([query])
        vec_scores = cosine_similarity(q_vec, self.tfidf_matrix).ravel()

        fused = self.bm25_weight * _minmax(bm25_scores) + self.vector_weight * _minmax(vec_scores)

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
                        "vector": round(float(vec_scores[idx]), 4),
                    },
                }
            )
        return results


_retriever = None


def get_retriever() -> HybridRetriever:
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever()
    return _retriever
