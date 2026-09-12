"""
Gemini text-embedding provider (semantic half of hybrid retrieval).

Uses the official google-genai SDK with a server-side GEMINI_API_KEY (BYOK). Vectors are
L2-normalised. Corpus embeddings are cached in MongoDB keyed by (model, text_hash) so we
never re-embed unchanged passages across restarts. If no key is configured — or the API
errors — callers fall back to the lexical/TF-IDF path, so the app never crashes.

The key lives only in backend/.env and is never sent to the frontend.
"""

import os
import time
import hashlib
import logging
from typing import List, Optional

import numpy as np

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIMENSIONS = int(os.environ.get("EMBEDDING_DIMENSIONS", "768"))


def text_hash(text: str) -> str:
    return hashlib.sha256(f"{EMBEDDING_MODEL}:{text}".encode("utf-8")).hexdigest()


def _l2_normalize(vec: List[float]) -> List[float]:
    arr = np.asarray(vec, dtype=np.float32)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr.tolist()
    return (arr / norm).tolist()


class GeminiEmbeddings:
    """Thin, resilient wrapper around google-genai embeddings."""

    def __init__(self, cache_collection=None):
        self.model = EMBEDDING_MODEL
        self.dimensions = EMBEDDING_DIMENSIONS
        self.cache = cache_collection  # a pymongo collection or None
        self._client = None
        self._task_types_supported = True
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        self.available = bool(api_key)
        if self.available:
            try:
                from google import genai

                self._client = genai.Client(api_key=api_key)
            except Exception as e:  # pragma: no cover
                logger.error("Failed to init google-genai client: %s", e)
                self.available = False

    # ----------------------------------------------------------------- internals
    def _embed_call(self, texts: List[str], task_type: str) -> List[List[float]]:
        from google.genai import types

        last_err = None
        for attempt in range(5):
            try:
                cfg_kwargs = {"output_dimensionality": self.dimensions}
                if self._task_types_supported:
                    cfg_kwargs["task_type"] = task_type
                res = self._client.models.embed_content(
                    model=self.model,
                    contents=texts,
                    config=types.EmbedContentConfig(**cfg_kwargs),
                )
                return [_l2_normalize(list(e.values)) for e in res.embeddings]
            except Exception as e:
                msg = str(e)
                last_err = e
                # If task_type is rejected by the model, retry once without it.
                if "task_type" in msg and self._task_types_supported:
                    self._task_types_supported = False
                    continue
                # Backoff on rate limits / transient errors (free tier = 100 req/min).
                if any(k in msg for k in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "deadline")):
                    time.sleep(30)
                    continue
                break
        raise RuntimeError(f"Gemini embedding call failed: {last_err}")

    # ----------------------------------------------------------------- public API
    def embed_documents(self, texts: List[str], cache_only: bool = False) -> Optional[np.ndarray]:
        """Embed corpus passages, using the Mongo cache where possible. Returns matrix or None.

        cache_only=True performs NO network calls: it returns the matrix only if every
        passage is already cached, else None (used for a fast, non-blocking startup path).
        """
        if not self.available:
            return None
        try:
            vectors: List[Optional[List[float]]] = [None] * len(texts)
            to_embed_idx = []
            to_embed_txt = []

            for i, t in enumerate(texts):
                h = text_hash(t)
                cached = self.cache.find_one({"_id": h}) if self.cache is not None else None
                if cached and len(cached.get("vector", [])) == self.dimensions:
                    vectors[i] = cached["vector"]
                else:
                    to_embed_idx.append(i)
                    to_embed_txt.append(t)

            if to_embed_txt and cache_only:
                return None  # not fully cached; caller will trigger a background build

            # Batch the uncached texts in small chunks to respect free-tier rate limits,
            # caching each item immediately so partial progress survives restarts.
            CHUNK = 20
            for start in range(0, len(to_embed_txt), CHUNK):
                chunk_txt = to_embed_txt[start : start + CHUNK]
                chunk_idx = to_embed_idx[start : start + CHUNK]
                embedded = self._embed_call(chunk_txt, task_type="RETRIEVAL_DOCUMENT")
                for j, vec in enumerate(embedded):
                    vectors[chunk_idx[j]] = vec
                    if self.cache is not None:
                        self.cache.update_one(
                            {"_id": text_hash(chunk_txt[j])},
                            {"$set": {"vector": vec, "model": self.model, "dim": self.dimensions}},
                            upsert=True,
                        )
                if start + CHUNK < len(to_embed_txt):
                    time.sleep(20)  # space chunks under the 100 req/min free-tier limit

            if any(v is None for v in vectors):
                return None
            return np.asarray(vectors, dtype=np.float32)
        except Exception as e:
            logger.error("embed_documents failed, will fall back to lexical: %s", e)
            return None

    def embed_query(self, query: str) -> Optional[np.ndarray]:
        if not self.available:
            return None
        try:
            vec = self._embed_call([query], task_type="RETRIEVAL_QUERY")[0]
            return np.asarray(vec, dtype=np.float32)
        except Exception as e:
            logger.error("embed_query failed: %s", e)
            return None


_provider: Optional[GeminiEmbeddings] = None


def get_embeddings(cache_collection=None) -> GeminiEmbeddings:
    global _provider
    if _provider is None:
        _provider = GeminiEmbeddings(cache_collection=cache_collection)
    return _provider
