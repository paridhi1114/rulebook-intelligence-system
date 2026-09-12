from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional
from starlette.concurrency import run_in_threadpool

from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

from rulebook_data import get_rules, get_chapters, corpus_stats, CONTRADICTIONS
from retrieval import get_retriever
from reasoning import reason_over_passages
from eval_data import EVAL_QUESTIONS

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# Synchronous handle used only to persist the Gemini embedding cache (built at startup,
# outside the async request path). Keeps corpus embeddings across restarts.
from pymongo import MongoClient as _SyncMongoClient
_sync_db = _SyncMongoClient(mongo_url)[os.environ["DB_NAME"]]
_embedding_cache = _sync_db["embedding_cache"]

app = FastAPI(title="Rulebook Intelligence System")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ Models
class AskRequest(BaseModel):
    question: str


class EvalResultDoc(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metrics: dict
    results: list


# ------------------------------------------------------------------ Rulebook endpoints
@api_router.get("/")
async def root():
    return {"message": "Rulebook Intelligence System API", "status": "ok"}


@api_router.get("/system/info")
async def system_info():
    """Transparency endpoint: which retrieval backends are actually in use."""
    retriever = get_retriever(cache_collection=_embedding_cache)
    return {"retrieval": retriever.info(), "reasoning_model": "gemini-3.1-pro-preview"}


@api_router.get("/rulebook/stats")
async def rulebook_stats():
    stats = corpus_stats()
    stats["contradictions"] = CONTRADICTIONS
    return stats


@api_router.get("/rulebook")
async def get_rulebook():
    chapters = get_chapters()
    rules = get_rules()
    grouped = []
    for ch in chapters:
        ch_rules = [r for r in rules if r["chapter"] == ch["title"]]
        grouped.append({**ch, "rules": ch_rules, "rule_count": len(ch_rules)})
    return {"chapters": grouped, "total_rules": len(rules)}


# ------------------------------------------------------------------ Ask endpoint
@api_router.post("/ask")
async def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    retriever = get_retriever(cache_collection=_embedding_cache)
    passages = await run_in_threadpool(retriever.retrieve, question, 10)

    try:
        result = await reason_over_passages(question, passages)
    except Exception as e:
        logger.exception("Reasoning failed")
        raise HTTPException(status_code=502, detail=f"Reasoning layer error: {e}")

    response = {
        "question": question,
        "state": result["state"],
        "answer": result.get("answer", ""),
        "explanation": result.get("explanation", ""),
        "evidence": result.get("evidence", []),
        "conflicts": result.get("conflicts", []),
        "missing_information": result.get("missing_information", ""),
        "retrieved": passages,
        "model": result.get("model"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    # Persist query history (fire and forget style, but awaited for correctness).
    try:
        await db.query_history.insert_one({**response, "_hid": str(uuid.uuid4())})
    except Exception:
        logger.warning("Failed to persist query history", exc_info=True)

    response.pop("_id", None)
    return response


@api_router.get("/history")
async def history(limit: int = 20):
    docs = await db.query_history.find({}, {"_id": 0, "_hid": 0, "retrieved": 0}).sort("created_at", -1).to_list(limit)
    return {"history": docs}


# ------------------------------------------------------------------ Evaluation
@api_router.get("/evaluation/questions")
async def evaluation_questions():
    return {"questions": EVAL_QUESTIONS, "count": len(EVAL_QUESTIONS)}


def _score_retrieval(expected_ids: List[str], retrieved_ids: List[str], cited_ids: List[str]):
    """Retrieval hit = all expected rule ids were retrieved. Citation hit = all cited."""
    if not expected_ids:
        return None, None
    retrieved_hit = all(rid in retrieved_ids for rid in expected_ids)
    cited_hit = all(rid in cited_ids for rid in expected_ids)
    return retrieved_hit, cited_hit


async def _evaluate_one(q: dict):
    retriever = get_retriever(cache_collection=_embedding_cache)
    passages = await run_in_threadpool(retriever.retrieve, q["question"], 10)
    retrieved_ids = [p["rule_id"] for p in passages]

    result = await reason_over_passages(q["question"], passages)
    actual_state = result["state"]

    cited_ids = [e["rule_id"] for e in result.get("evidence", [])]
    conflict_ids = []
    for c in result.get("conflicts", []):
        conflict_ids.extend(c.get("rule_ids", []))

    all_cited = list(set(cited_ids + conflict_ids))
    retrieved_hit, cited_hit = _score_retrieval(q["expected_rule_ids"], retrieved_ids, all_cited)

    return {
        "id": q["id"],
        "question": q["question"],
        "expected_state": q["expected_state"],
        "actual_state": actual_state,
        "state_correct": actual_state == q["expected_state"],
        "expected_rule_ids": q["expected_rule_ids"],
        "retrieved_rule_ids": retrieved_ids,
        "cited_rule_ids": all_cited,
        "retrieval_correct": retrieved_hit,
        "citation_correct": cited_hit,
        "difficulty": q["difficulty"],
        "answer": result.get("answer", ""),
        "explanation": result.get("explanation", ""),
        "evidence": result.get("evidence", []),
        "conflicts": result.get("conflicts", []),
        "missing_information": result.get("missing_information", ""),
    }


def _compute_metrics(results: List[dict]):
    total = len(results)
    correct = sum(1 for r in results if r["state_correct"])

    by_state = {}
    for state in ["ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"]:
        subset = [r for r in results if r["expected_state"] == state]
        s_correct = sum(1 for r in subset if r["state_correct"])
        by_state[state] = {
            "total": len(subset),
            "correct": s_correct,
            "accuracy": round(s_correct / len(subset), 4) if subset else None,
        }

    retr_items = [r for r in results if r["retrieval_correct"] is not None]
    retr_correct = sum(1 for r in retr_items if r["retrieval_correct"])
    cite_items = [r for r in results if r["citation_correct"] is not None]
    cite_correct = sum(1 for r in cite_items if r["citation_correct"])

    edge = [r for r in results if r["difficulty"] == "edge"]
    edge_correct = sum(1 for r in edge if r["state_correct"])

    return {
        "overall_accuracy": round(correct / total, 4) if total else 0,
        "total_questions": total,
        "correct": correct,
        "by_state": by_state,
        "retrieval_accuracy": round(retr_correct / len(retr_items), 4) if retr_items else None,
        "retrieval_measured_on": len(retr_items),
        "citation_accuracy": round(cite_correct / len(cite_items), 4) if cite_items else None,
        "citation_measured_on": len(cite_items),
        "edge_accuracy": round(edge_correct / len(edge), 4) if edge else None,
        "edge_total": len(edge),
    }


@api_router.post("/evaluation/run")
async def evaluation_run():
    sem = asyncio.Semaphore(4)

    async def run_q(q):
        async with sem:
            try:
                return await _evaluate_one(q)
            except Exception as e:
                logger.exception("Eval question %s failed", q["id"])
                return {
                    "id": q["id"], "question": q["question"],
                    "expected_state": q["expected_state"], "actual_state": "ERROR",
                    "state_correct": False, "expected_rule_ids": q["expected_rule_ids"],
                    "retrieved_rule_ids": [], "cited_rule_ids": [],
                    "retrieval_correct": False if q["expected_rule_ids"] else None,
                    "citation_correct": False if q["expected_rule_ids"] else None,
                    "difficulty": q["difficulty"], "answer": "", "explanation": f"Error: {e}",
                    "evidence": [], "conflicts": [], "missing_information": "",
                }

    results = await asyncio.gather(*[run_q(q) for q in EVAL_QUESTIONS])
    results = sorted(results, key=lambda r: r["id"])
    metrics = _compute_metrics(results)

    doc = EvalResultDoc(metrics=metrics, results=results)
    await db.evaluation_runs.insert_one(doc.model_dump())

    return {"metrics": metrics, "results": results, "run_id": doc.id, "created_at": doc.created_at}


@api_router.get("/evaluation/latest")
async def evaluation_latest():
    doc = await db.evaluation_runs.find_one({}, {"_id": 0}, sort=[("created_at", -1)])
    if not doc:
        return {"metrics": None, "results": [], "run_id": None}
    return doc


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def warm_up():
    # Build retrieval indices at startup so the first request is fast. Passing the sync
    # cache collection lets Gemini corpus embeddings persist across restarts.
    retriever = await run_in_threadpool(get_retriever, _embedding_cache)
    logger.info("Retriever warmed up: %s | %s", corpus_stats(), retriever.info())

    # If Gemini embeddings are configured but not yet fully cached, build them in the
    # background (chunked + rate-limit aware) without blocking startup. The retriever
    # serves via TF-IDF until the embeddings are ready, then swaps them in.
    if retriever.embedder.available and retriever.semantic_backend != "gemini":
        async def _bg():
            await run_in_threadpool(retriever.ensure_semantic)
            logger.info("Background semantic build done: %s", retriever.info())
        asyncio.create_task(_bg())


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
