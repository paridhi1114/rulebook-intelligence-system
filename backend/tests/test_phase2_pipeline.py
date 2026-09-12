"""
Phase 2 representative integration tests for the reasoning pipeline.

Covers the seven required scenarios. Where LLM classification is deterministic enough we
assert the state; everywhere we assert the robust invariants that must ALWAYS hold:
  - retrieval recall  : the relevant rule(s) appear in the retrieved candidate set
  - source integrity  : every cited rule_id (evidence + conflicts) was actually retrieved
                        (the model may not invent citations)
  - schema            : required keys are present and state is one of the three allowed.

Run:  cd /app/backend && python -m pytest tests/test_phase2_pipeline.py -v
Requires the backend running on :8001 (default) or BACKEND_URL env.
"""

import os
import requests

BASE = os.environ.get("BACKEND_URL", "http://localhost:8001") + "/api"
ALLOWED = {"ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"}


def _ask(question):
    r = requests.post(f"{BASE}/ask", json={"question": question}, timeout=90)
    assert r.status_code == 200, r.text
    return r.json()


def _cited_ids(data):
    ids = [e["rule_id"] for e in data.get("evidence", [])]
    for c in data.get("conflicts", []):
        ids.extend(c.get("rule_ids", []))
    return set(ids)


def _assert_schema_and_grounding(data):
    for key in ("state", "answer", "explanation", "evidence", "conflicts", "missing_information", "retrieved"):
        assert key in data, f"missing key {key}"
    assert data["state"] in ALLOWED
    retrieved = {p["rule_id"] for p in data["retrieved"]}
    # SOURCE INTEGRITY: no cited id may be outside the retrieved candidate set.
    assert _cited_ids(data).issubset(retrieved), f"hallucinated citations: {_cited_ids(data) - retrieved}"


# 1. Clearly answerable
def test_answerable_transfer_credits():
    d = _ask("What is the maximum number of transfer credits I can bring toward my degree?")
    _assert_schema_and_grounding(d)
    assert "ELI-016" in {p["rule_id"] for p in d["retrieved"]}
    assert d["state"] == "ANSWERABLE"
    assert "ELI-016" in _cited_ids(d)


# 2. Clearly unanswerable
def test_not_answerable_dress_code():
    d = _ask("Is there a dress code that students must follow on campus?")
    _assert_schema_and_grounding(d)
    assert d["state"] == "NOT_ANSWERABLE"
    assert d["missing_information"].strip() != ""


# 3. Clearly contradictory
def test_contradictory_medical_leave():
    d = _ask("How many days of medical leave am I entitled to in a semester?")
    _assert_schema_and_grounding(d)
    assert d["state"] == "CONTRADICTORY"
    conflict_ids = _cited_ids(d)
    assert {"LEV-002", "LEV-006"}.issubset(conflict_ids)
    # both conflicting passages must be shown with exact text
    for c in d["conflicts"]:
        for p in c.get("passages", []):
            assert p["exact_text"]


# 4. Semantically phrased, little/no word overlap -> semantic retrieval must still find it
def test_semantic_paraphrase_recall():
    d = _ask("If I was absent from my final test because I was in hospital, can I take it later?")
    _assert_schema_and_grounding(d)
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    # None of these ids share the query's surface words; only semantics connects them.
    assert retrieved & {"REX-001", "EXM-017", "EXC-007"}, f"semantic recall failed: {retrieved}"


# 5. Exact keyword query -> lexical retrieval should nail it
def test_exact_keyword_supplementary():
    d = _ask("How many supplementary examination attempts are allowed per course?")
    _assert_schema_and_grounding(d)
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    assert {"REX-002", "REX-006"}.issubset(retrieved)
    assert d["state"] == "CONTRADICTORY"


# 6. Question involving an explicit exception
def test_exception_credit_overload():
    d = _ask("Can a final-year student exceed the normal credit limit to graduate on time?")
    _assert_schema_and_grounding(d)
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    assert "EXC-003" in retrieved  # the explicit exception must be retrieved


# 7. Two related rules that are NOT actually contradictory (must not be over-flagged)
def test_related_but_not_contradictory():
    d = _ask("If I represent the university at an official sports event, is that time counted as attendance?")
    _assert_schema_and_grounding(d)
    # LEV-009 explicitly grants duty-leave attendance; this is a compatible, answerable fact.
    assert d["state"] == "ANSWERABLE"
    assert "LEV-009" in _cited_ids(d)


# 8. Empty query must be rejected, not answered
def test_empty_query_rejected():
    r = requests.post(f"{BASE}/ask", json={"question": "   "}, timeout=30)
    assert r.status_code == 400
