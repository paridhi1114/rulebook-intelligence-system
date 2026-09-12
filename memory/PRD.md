# PRD — The Rulebook That Argues With Itself

## Original Problem Statement
Build a grounded Rulebook Intelligence System that reads a large university academic-
regulations rulebook (6000+ words) and answers plain-language questions, classifying each
into exactly one of three states — ANSWERABLE, NOT_ANSWERABLE, CONTRADICTORY — with zero
hallucination, full citations, side-by-side conflict passages, genuine hybrid retrieval,
Gemini structured-JSON reasoning, and a 25-question evaluation harness reporting measured
accuracy. (IT Geeks AI Developer Vibe Coding Round.)

## Architecture
- **Frontend:** React 19 + Tailwind (authoritative legal/regulatory dark theme), React Query, sonner. Tabs: Ask, Browse Rulebook, Accuracy Evaluation.
- **Backend:** FastAPI (Python), Motor/MongoDB.
- **Retrieval:** `retrieval.py` HybridRetriever = BM25 (rank_bm25) + TF-IDF cosine (scikit-learn), min-max normalised + fused, top_k=10.
- **Reasoning:** `reasoning.py` Gemini `gemini-3.1-pro-preview` via emergentintegrations (server-side EMERGENT_LLM_KEY). Returns structured JSON; `_validate_grounding` drops hallucinated citations; passages re-hydrated from corpus.
- **Corpus:** `rulebook_data.py` — 101 rules, 18 chapters, 6,021 words, 19 deliberate contradiction pairs.
- **Eval:** `eval_data.py` — 25 labelled questions; `/api/evaluation/run` scores overall/per-state/retrieval/citation/edge accuracy. Stored in MongoDB.

## User Personas
- **Student** asking plain-language questions about regulations.
- **Registrar / administrator** auditing rules and spotting internal conflicts.
- **Evaluator** verifying grounded accuracy via the dashboard.

## Core Requirements (static)
- Never hallucinate; ground every answer in retrieved passages with rule_id/chapter/section/subsection/exact_text.
- Distinguish ANSWERABLE / NOT_ANSWERABLE / CONTRADICTORY; surface all conflicting passages.
- Genuine hybrid retrieval; do not send whole rulebook to LLM.
- Measured evaluation claims only.

## Implemented (2026-06-12)
- 6,021-word, 101-rule, 18-chapter synthetic rulebook with 19 subtle contradictions.
- **Phase 1:** Hybrid BM25 + TF-IDF retriever; Gemini grounded reasoning with anti-hallucination citation validation; full 3-state Ask UI (state badge, answer/explanation, evidence cards, side-by-side conflict cards, missing-information block, retrieval trace); Browse viewer with conflict flags; Evaluation dashboard (25 Qs, live metrics); README/.env.example/.gitignore.
- **Phase 2 (core reasoning engine hardening):**
  - Semantic retriever upgraded to **real Google Gemini embeddings** (`gemini-embedding-001`, 768-dim, `google-genai`, server-side `GEMINI_API_KEY`), L2-normalised, **cached in MongoDB** (`embedding_cache`), built in a rate-limit-aware background task with automatic **TF-IDF fallback**. Hybrid fusion 0.45 BM25 / 0.55 semantic.
  - `GET /api/system/info` reports the live retrieval backend.
  - Reasoning layer: stricter scope/contradiction logic (overlapping scopes with different requirements = contradiction unless explicit precedence), retry on malformed/invalid model output, graceful error handling (Gemini errors, empty query 400, no-retrieval, rate limits) without exposing secrets.
  - Source integrity: cited rule_ids validated against retrieved candidate set (no invented citations).
  - 8 representative Phase-2 tests (`backend/tests/test_phase2_pipeline.py`) covering answerable/unanswerable/contradictory/semantic-paraphrase/exact-keyword/exception/related-not-contradictory/empty-query — all pass.
  - Measured eval: representative run 25/25 (100%) with Gemini embeddings; non-deterministic so may vary.

## Backlog / Remaining
- **P1:** Async job + polling for evaluation run (currently a single blocking POST ~60–90s).
- **P2:** Swap TF-IDF for a dense neural embedding retriever for better paraphrase recall.
- **P2:** Precedence-rule engine to resolve conflicts where the rulebook states precedence.
- **P2:** Persisted per-question history browser in the UI.

## Next Tasks
- Consider streaming the Ask answer token-by-token for perceived speed.
- Add export of an evaluation run to CSV/JSON from the dashboard.
