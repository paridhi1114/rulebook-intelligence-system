# The Rulebook That Argues With Itself
### A Grounded Rulebook Intelligence System

A full-stack system that reads a large university academic-regulations rulebook and
answers plain-language questions about it — while strictly distinguishing between three
situations and **never hallucinating** an answer:

| State | Meaning |
|-------|---------|
| 🟢 **ANSWERABLE** | The rulebook contains enough information to answer the question. |
| 🔴 **NOT_ANSWERABLE** | The rulebook does not specify the answer. The system says so explicitly instead of guessing. |
| 🟡 **CONTRADICTORY** | Two or more applicable passages conflict. The system surfaces the conflict and shows the exact passages. |

Every substantive answer is grounded in retrieved rulebook passages with full citations
(`rule_id`, `chapter`, `section`, `subsection`, `exact_text`).

---

## 1. Problem Statement

Regulations are large, fragmented, and often internally inconsistent. A student asking
"how many days of medical leave do I get?" may be met with two different numbers in two
different sections. A naive LLM will happily pick one and sound confident. This system is
built to do the opposite: retrieve the actual governing passages, and either answer from
them, admit the rulebook is silent, or **surface the contradiction**.

## 2. Solution Architecture

```
                    ┌────────────────────────────────────────────┐
   React (CRA)      │  Ask · Browse Rulebook · Evaluation Suite  │
   Tailwind + UI    └───────────────┬────────────────────────────┘
                                    │  REST /api
                    ┌───────────────▼────────────────────────────┐
   FastAPI          │  /api/ask   /api/rulebook   /api/evaluation │
                    └───────┬───────────────┬────────────────────┘
                            │               │
             ┌──────────────▼──┐   ┌─────────▼───────────────────┐
             │ HybridRetriever │   │  Gemini Reasoning Layer     │
             │ BM25 + TF-IDF   │──▶│  (structured JSON, grounded)│
             └────────┬────────┘   └──────────┬──────────────────┘
                      │                        │ anti-hallucination
             ┌────────▼────────┐      ┌────────▼─────────┐
             │ rulebook_data   │      │ citation validate │
             │ 101 rules       │      │ (drop unknown ids) │
             └─────────────────┘      └───────────────────┘

   MongoDB: query_history · evaluation_runs
```

The design is deliberately modular: retrieval, reasoning, corpus, and evaluation are
separate modules so each can be reasoned about and swapped independently.

## 3. Tech Stack

- **Frontend:** React 19, Tailwind CSS, shadcn/ui primitives, lucide-react icons, sonner
  toasts, React Query. Serif/mono editorial "legal intelligence" theme.
- **Backend:** FastAPI (Python), Motor (async MongoDB).
- **Retrieval:** `rank_bm25` (BM25 lexical) + scikit-learn `TfidfVectorizer` (vector-space
  cosine similarity), score-fused.
- **Reasoning:** Google **Gemini** (`gemini-3.1-pro-preview`) via Emergent's universal LLM
  key, called **server-side only**.
- **Database:** MongoDB (query history + evaluation runs).

> The spec suggested Node/Express + TypeScript; this deployment target is optimised for
> FastAPI + React, so the backend is Python. The architecture, contracts, and guarantees
> are identical.

## 4. Retrieval Pipeline

`backend/retrieval.py` — a genuine hybrid pipeline (we never dump the whole rulebook into
the LLM):

1. **Load** the rulebook (101 rules) with full metadata.
2. **Chunk** at the rule level — each rule is a self-contained, citable unit that preserves
   `rule_id / chapter / section / subsection / title / exact_text`.
3. **Represent** each rule two ways:
   - **BM25** over tokenised text (lexical / keyword matching).
   - **TF-IDF** unigram+bigram vectors (a vector-space semantic representation) scored with
     cosine similarity.
4. **Retrieve** by min-max normalising both score vectors and fusing them
   (`0.5·BM25 + 0.5·vector`); return the top-K (default 8) passages.
5. **Pass only the retrieved evidence** to the reasoning layer.
6. **Produce** a structured answer.

Each response exposes a **retrieval trace** in the UI (fused / BM25 / vector scores per
passage) so retrieval is fully inspectable.

## 5. Conflict Detection Approach

Conflicts are detected by the reasoning layer over the retrieved set, not by hardcoding.
The system prompt instructs Gemini to flag `CONTRADICTORY` only when two or more retrieved
passages **govern the same matter but state different requirements/thresholds/deadlines**,
and to *not* treat explicitly different scopes (e.g. general vs a clearly-scoped special
category) as conflicts. When a conflict is found, the model must return every conflicting
`rule_id`; the UI renders them side-by-side with their exact text.

Because the deliberate contradictions are written to share vocabulary (e.g. both medical-
leave rules say "medical leave … days per semester"), hybrid retrieval reliably surfaces
*both* sides of a conflict for the same query.

## 6. Gemini Usage

- Called only from the backend (`backend/reasoning.py`); the key lives in `backend/.env`
  and is **never** exposed to the frontend.
- Gemini receives the question + retrieved passages and must return a single JSON object:

```json
{
  "state": "ANSWERABLE | NOT_ANSWERABLE | CONTRADICTORY",
  "answer": "...",
  "explanation": "...",
  "evidence": [{"rule_id": "...", "why": "..."}],
  "conflicts": [{"rule_ids": ["...","..."], "nature": "..."}],
  "missing_information": "..."
}
```

- **Anti-hallucination guard:** after Gemini responds, `_validate_grounding` drops any
  cited `rule_id` that was not actually in the retrieved set. If a `CONTRADICTORY` verdict
  has no valid surviving conflict, it is safely downgraded. Citations are then re-hydrated
  with the verbatim passage text from the corpus — so the exact text shown always comes
  from our data, never from the model's memory.

## 7. Data / Corpus Design

`backend/rulebook_data.py` — a synthetic university academic-regulations rulebook of
**~6,000 words** across **18 chapters** (Registration, Academic Eligibility, Attendance,
Examinations, Grading, Re-examinations, Assignments, Project Requirements, Internships,
Scholarships, Leave, Academic Misconduct, Disciplinary Rules, Appeals, Graduation,
Deadlines, Exceptions, Administrative Procedures).

Each of the 101 rules carries stable metadata: `rule_id`, `chapter`, `section`,
`subsection`, `title`, `exact_text`.

### How the deliberate contradictions work

The corpus embeds **19 intentional, subtle contradictions** (listed in `CONTRADICTIONS`).
They are realistic drafting inconsistencies, not nonsense — e.g.:

| Topic | Rule A | Rule B |
|-------|--------|--------|
| Attendance to sit exams | `ATT-002` (75%) | `EXM-003` (80%) |
| Supplementary attempts | `REX-002` (two) | `REX-006` (one) |
| Late assignments | `ASG-003` (5-day grace) | `DDL-004` (none) |
| Medical leave | `LEV-002` (15 days) | `LEV-006` (10 days) |
| Minimum passing grade | `GRD-003` (D/40%) | `GRD-008` (C/50% core) |
| Grace marks | `EXM-008` (up to 3) | `GRD-010` (none) |
| Internship duration | `INT-002` (8 wks) | `INT-006` (6 wks) |
| Internship credit gate | `INT-003` (90) | `INT-007` (100) |
| Scholarship CGPA | `SCH-002` (8.0) | `SCH-005` (7.5) |
| Project team size | `PRJ-003` (4) | `PRJ-006` (3) |
| Registration window | `REG-002` (2 wks) | `DDL-002` (10 days) |
| Credits to graduate | `GRAD-002` (160) | `GRAD-007` (156) |
| Appeal window | `APL-002` (7 days) | `APL-005` (14 days) |
| Probation CGPA | `ELI-004` (<5.0) | `DIS-004` (<4.5) |
| First plagiarism penalty | `MIS-002` (zero on task) | `MIS-005` (fail course) |
| Max course load | `REG-005` (24) | `REG-009` (27) |
| Withdrawal deadline | `DDL-006` (week 8) | `EXC-004` (week 10) |
| Re-evaluation window | `EXM-005` (15 days) | `APL-006` (7 days) |
| Scholarship payout | `SCH-003` (30 days) | `ADM-004` (45 days) |

The pairs are placed in *different chapters/subsections* so detecting them genuinely
requires retrieval + reasoning rather than reading a single paragraph.

## 8. Evaluation Methodology

`backend/eval_data.py` defines **exactly 25** realistic, non-trivial questions:
**10 answerable · 8 contradictory · 7 not-answerable**, including near-miss and
plausible-adjoining questions (e.g. paternity leave — the rulebook only covers maternity;
the supplementary-exam *fee amount* — only the existence of a fee is stated).

The harness (`/api/evaluation/run`) sends each question through the **live** retrieval +
reasoning pipeline (nothing is hardcoded) and records, per question:
`question, expected_state, expected_rule_ids, actual_state, retrieved_rule_ids,
cited_rule_ids, state_correct, retrieval_correct, citation_correct, difficulty`.

It then computes:
- **Overall classification accuracy**
- **Per-state accuracy** (Answerable / Not-Answerable / Contradictory)
- **Retrieval accuracy** — were all expected rule IDs retrieved (measured only on the
  grounded questions that have expected IDs)?
- **Citation accuracy** — were all expected rule IDs actually cited in the answer?
- **Edge-question accuracy** — performance on near-miss / hard questions.

The dashboard reports whatever the run measures. **We make measured claims only** — no
"100% accurate" is asserted anywhere; the numbers you see are the numbers produced by a
live run (LLM outputs are non-deterministic, so exact figures may vary slightly per run).

## 9. Results

Run the Evaluation Suite in-app (or `POST /api/evaluation/run`) to reproduce. A
representative run on this corpus scores strongly on Answerable/Contradictory detection
and on retrieval, with most misses (if any) concentrated on the intentionally hard
near-miss Not-Answerable questions — exactly where a grounded system should be most
careful. See the dashboard for the exact, timestamped figures of your run.

## 10. How to Run Locally

**Prerequisites:** Python 3.11+, Node 18+, Yarn, MongoDB running locally.

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env      # then set EMERGENT_LLM_KEY (or a Gemini key)
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Frontend (new terminal)
cd frontend
yarn install
cp .env.example .env      # set REACT_APP_BACKEND_URL=http://localhost:8001
yarn start                # http://localhost:3000
```

In this managed environment both services run under **supervisor**
(`sudo supervisorctl restart backend frontend`).

## 11. Environment Variables

**backend/.env**
| Key | Description |
|-----|-------------|
| `MONGO_URL` | MongoDB connection string |
| `DB_NAME` | Database name |
| `CORS_ORIGINS` | Allowed origins (comma-separated or `*`) |
| `EMERGENT_LLM_KEY` | Server-side key used to call Gemini |

**frontend/.env**
| Key | Description |
|-----|-------------|
| `REACT_APP_BACKEND_URL` | Base URL of the backend (all API calls are prefixed with `/api`) |

## 12. Demo Script (all three states)

1. **Contradictory:** *"How many days of medical leave am I entitled to in a semester?"* →
   🟡 CONTRADICTORY, showing `LEV-002` (15) vs `LEV-006` (10) side by side.
2. **Answerable:** *"What is the maximum number of transfer credits I can bring toward my
   degree?"* → 🟢 ANSWERABLE, citing `ELI-016` (40).
3. **Not answerable:** *"Does the university provide health insurance coverage to
   students?"* → 🔴 NOT_ANSWERABLE, with a "missing information" explanation.

## 13. Known Limitations

- **Non-determinism:** Gemini outputs vary slightly between runs; borderline near-miss
  questions are the most sensitive.
- **Semantic retriever:** TF-IDF is a vector-space (bag-of-ngrams) representation, not a
  neural embedding. It is fast, dependency-light, and effective on this legalese corpus,
  but a dense embedding model would capture paraphrase better. The retriever is a single
  swappable class (`HybridRetriever`).
- **Conflict scope:** the system flags conflicts among the top-K retrieved passages; a
  conflict whose two sides never co-retrieve for any phrasing could be missed (mitigated by
  shared-vocabulary corpus design and K=8).
- **No precedence engine:** where the rulebook gives no explicit precedence rule, conflicts
  are surfaced rather than resolved — by design.

## 14. Project Structure

```
backend/
  server.py          FastAPI app + endpoints
  rulebook_data.py   corpus (101 rules, 18 chapters, 19 contradictions)
  retrieval.py       hybrid BM25 + TF-IDF retriever
  reasoning.py       Gemini grounded reasoning + anti-hallucination guard
  eval_data.py       25 labelled evaluation questions
frontend/src/
  App.js
  lib/api.js
  components/  Header · AskPanel · StateBadge · EvidenceCard ·
               ConflictCards · RulebookViewer · EvaluationDashboard
```
