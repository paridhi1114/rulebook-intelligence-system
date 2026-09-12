"""Backend API tests for Rulebook Intelligence System."""
import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://rulebook-ai-1.preview.emergentagent.com").rstrip("/")


@pytest.fixture(scope="module")
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# --- Rulebook stats ---
def test_stats(client):
    r = client.get(f"{BASE_URL}/api/rulebook/stats", timeout=30)
    assert r.status_code == 200
    d = r.json()
    assert d["total_words"] >= 6000, f"total_words={d.get('total_words')}"
    assert d["total_chapters"] == 18
    assert d.get("total_rules", 0) > 0
    assert d.get("intentional_contradictions", 0) >= 1
    assert isinstance(d.get("contradictions"), list) and len(d["contradictions"]) >= 1


# --- Rulebook full ---
def test_rulebook(client):
    r = client.get(f"{BASE_URL}/api/rulebook", timeout=30)
    assert r.status_code == 200
    d = r.json()
    chapters = d.get("chapters") or d
    assert len(chapters) >= 1
    # Find a rule in first chapter that has rules
    for ch in chapters:
        rules = ch.get("rules", [])
        if rules:
            rule = rules[0]
            for key in ("rule_id", "chapter", "title", "exact_text"):
                assert key in rule, f"missing {key} in rule"
            break


# --- Ask: ANSWERABLE ---
def test_ask_answerable(client):
    payload = {"question": "What is the maximum number of transfer credits I can bring toward my degree?"}
    r = client.post(f"{BASE_URL}/api/ask", json=payload, timeout=90)
    assert r.status_code == 200
    d = r.json()
    assert d["state"] == "ANSWERABLE", f"got state={d['state']}"
    evidence = d.get("evidence", [])
    assert len(evidence) >= 1
    cited_ids = {e["rule_id"] for e in evidence}
    assert "ELI-016" in cited_ids, f"cited={cited_ids}"
    retrieved_ids = {r_["rule_id"] for r_ in d.get("retrieved", [])}
    assert cited_ids.issubset(retrieved_ids), f"hallucinated citations: {cited_ids - retrieved_ids}"


# --- Ask: CONTRADICTORY ---
def test_ask_contradictory(client):
    payload = {"question": "How many days of medical leave am I entitled to in a semester?"}
    r = client.post(f"{BASE_URL}/api/ask", json=payload, timeout=90)
    assert r.status_code == 200
    d = r.json()
    assert d["state"] == "CONTRADICTORY", f"got state={d['state']}"
    conflicts = d.get("conflicts", [])
    # Collect rule_ids from conflicts (may be a flat list or grouped)
    ids = set()
    for c in conflicts:
        if isinstance(c, dict):
            if "rule_id" in c:
                ids.add(c["rule_id"])
            for p in c.get("passages", []) or []:
                ids.add(p.get("rule_id"))
                assert p.get("exact_text"), "conflict passage missing exact_text"
    assert "LEV-002" in ids and "LEV-006" in ids, f"expected LEV-002 & LEV-006 in {ids}"


# --- Ask: NOT_ANSWERABLE ---
def test_ask_not_answerable(client):
    payload = {"question": "Does the university provide health insurance coverage to students?"}
    r = client.post(f"{BASE_URL}/api/ask", json=payload, timeout=90)
    assert r.status_code == 200
    d = r.json()
    assert d["state"] == "NOT_ANSWERABLE", f"got state={d['state']}"
    assert d.get("missing_information")
    assert not d.get("evidence")


# --- Ask: empty ---
def test_ask_empty_400(client):
    r = client.post(f"{BASE_URL}/api/ask", json={"question": ""}, timeout=15)
    assert r.status_code == 400, f"got {r.status_code}"


# --- Evaluation ---
def test_eval_questions(client):
    r = client.get(f"{BASE_URL}/api/evaluation/questions", timeout=30)
    assert r.status_code == 200
    d = r.json()
    qs = d.get("questions") or d
    assert len(qs) == 25, f"got {len(qs)}"


def test_eval_run(client):
    r = client.post(f"{BASE_URL}/api/evaluation/run", json={}, timeout=240)
    assert r.status_code == 200
    d = r.json()
    metrics = d.get("metrics", d)
    assert "overall_accuracy" in metrics
    assert metrics["overall_accuracy"] >= 0.75, f"low acc {metrics['overall_accuracy']}"
    for k in ("retrieval_accuracy", "citation_accuracy", "edge_accuracy"):
        assert k in metrics, f"missing {k}"
    by_state = metrics.get("by_state", {})
    for s in ("ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"):
        assert s in by_state, f"missing by_state.{s}"
    results = d.get("results") or d.get("per_question") or []
    assert len(results) == 25
    for res in results:
        assert res.get("actual_state") != "ERROR"
