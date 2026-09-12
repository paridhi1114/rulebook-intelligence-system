"""Phase 2 iteration 2 tests - use external REACT_APP_BACKEND_URL."""
import os
import requests

BASE = os.environ.get("REACT_APP_BACKEND_URL", "https://rulebook-ai-1.preview.emergentagent.com").rstrip("/") + "/api"
ALLOWED = {"ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"}


def _ask(q, timeout=120):
    r = requests.post(f"{BASE}/ask", json={"question": q}, timeout=timeout)
    assert r.status_code == 200, r.text
    return r.json()


def _cited(d):
    ids = [e["rule_id"] for e in d.get("evidence", [])]
    for c in d.get("conflicts", []):
        ids.extend(c.get("rule_ids", []))
    return set(ids)


def _assert_grounding(d):
    for k in ("state", "answer", "explanation", "evidence", "conflicts", "missing_information", "retrieved"):
        assert k in d, f"missing {k}"
    assert d["state"] in ALLOWED
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    assert _cited(d).issubset(retrieved), f"hallucinated: {_cited(d)-retrieved}"
    # scores contain bm25 and semantic
    for p in d["retrieved"]:
        assert "scores" in p
        assert "bm25" in p["scores"]
        assert "semantic" in p["scores"]


def test_system_info():
    r = requests.get(f"{BASE}/system/info", timeout=30)
    assert r.status_code == 200
    j = r.json()
    assert j["retrieval"]["semantic_backend"] == "gemini"
    assert j["retrieval"]["embedding_model"] == "gemini-embedding-001"
    assert j["reasoning_model"] == "gemini-3.1-pro-preview"


def test_answerable_transfer_credits():
    d = _ask("What is the maximum number of transfer credits I can bring toward my degree?")
    _assert_grounding(d)
    assert d["state"] == "ANSWERABLE"
    assert "ELI-016" in _cited(d)


def test_contradictory_medical_leave():
    d = _ask("How many days of medical leave am I entitled to in a semester?")
    _assert_grounding(d)
    assert d["state"] == "CONTRADICTORY"
    assert {"LEV-002", "LEV-006"}.issubset(_cited(d))
    for c in d["conflicts"]:
        for p in c.get("passages", []):
            assert p["exact_text"].strip()


def test_not_answerable_dress_code():
    d = _ask("Is there a dress code that students must follow on campus?")
    _assert_grounding(d)
    assert d["state"] == "NOT_ANSWERABLE"
    assert d["missing_information"].strip() != ""


def test_semantic_paraphrase():
    d = _ask("If I was absent from my final test because I was in hospital, can I take it later?")
    _assert_grounding(d)
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    assert retrieved & {"REX-001", "EXM-017", "EXC-007"}, f"semantic recall failed: {retrieved}"


def test_exact_keyword_supplementary():
    d = _ask("How many supplementary examination attempts are allowed per course?")
    _assert_grounding(d)
    retrieved = {p["rule_id"] for p in d["retrieved"]}
    assert {"REX-002", "REX-006"}.issubset(retrieved)
    assert d["state"] == "CONTRADICTORY"


def test_related_not_contradictory():
    d = _ask("If I represent the university at an official sports event, is that time counted as attendance?")
    _assert_grounding(d)
    assert d["state"] == "ANSWERABLE"
    assert "LEV-009" in _cited(d)


def test_empty_query_400():
    r = requests.post(f"{BASE}/ask", json={"question": "   "}, timeout=30)
    assert r.status_code == 400


def test_evaluation_run():
    r = requests.post(f"{BASE}/evaluation/run", json={}, timeout=240)
    assert r.status_code == 200, r.text
    j = r.json()
    m = j["metrics"]
    assert "overall_accuracy" in m
    for s in ("ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"):
        assert s in m["by_state"]
    assert "retrieval_accuracy" in m
    assert "citation_accuracy" in m
    assert "edge_accuracy" in m
    assert len(j["results"]) == 25
    for res in j["results"]:
        assert res.get("actual_state") != "ERROR"
    assert m["overall_accuracy"] >= 0.8, f"low accuracy: {m['overall_accuracy']}"
