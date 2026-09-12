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
- Hybrid BM25+TF-IDF retriever with inspectable retrieval trace in UI.
- Gemini grounded reasoning with anti-hallucination citation validation.
- Full 3-state Ask UI: state badge, answer/explanation, evidence cards, side-by-side conflict cards, missing-information block, retrieval trace.
- Browse Rulebook viewer with chapter nav, search, conflict flags.
- Evaluation dashboard: 25 questions, live run, overall/per-state/retrieval/citation/edge metrics + results table.
- README, .env.example, .gitignore, backend/frontend .env.example.
- Verified: backend pytest 8/8 pass; frontend E2E pass; eval run 92%–100% overall (non-deterministic). Mobile responsive, no overflow.

## Backlog / Remaining
- **P1:** Async job + polling for evaluation run (currently a single blocking POST ~60–90s).
- **P2:** Swap TF-IDF for a dense neural embedding retriever for better paraphrase recall.
- **P2:** Precedence-rule engine to resolve conflicts where the rulebook states precedence.
- **P2:** Persisted per-question history browser in the UI.

## Next Tasks
- Consider streaming the Ask answer token-by-token for perceived speed.
- Add export of an evaluation run to CSV/JSON from the dashboard.
