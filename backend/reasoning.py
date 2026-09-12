"""
Gemini-powered reasoning layer.

Given a user question and ONLY the retrieved rulebook passages, Gemini classifies the
situation into ANSWERABLE / NOT_ANSWERABLE / CONTRADICTORY and returns structured JSON.
The system prompt forbids any use of outside knowledge, so every answer is grounded in the
supplied evidence. After the model responds we hard-validate that every cited rule_id was
actually in the retrieved set, dropping any hallucinated citation.
"""

import os
import json
import uuid
import logging
from typing import List, Dict

from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger(__name__)

MODEL_PROVIDER = "gemini"
MODEL_NAME = "gemini-3.1-pro-preview"

SYSTEM_PROMPT = """You are a meticulous Academic Regulations Intelligence engine for a university rulebook.

You will be given a QUESTION and a numbered list of RETRIEVED PASSAGES from the rulebook. Each passage has a rule_id, chapter, section, subsection, title and exact_text.

Your job is to classify the question into EXACTLY ONE of three states and answer STRICTLY using the retrieved passages. You must NEVER use outside knowledge and NEVER invent rules, numbers, or citations. Only cite rule_ids that appear in the retrieved passages.

The three states:

1. ANSWERABLE — The retrieved passages contain enough information to answer the question, and any applicable passages agree with one another (no conflict). Give a concise, direct answer grounded in the passages.

2. NOT_ANSWERABLE — The retrieved passages do NOT contain the specific information needed to answer the question. Do not guess. Explicitly state that the rulebook does not specify the answer and describe what information is missing. A passage merely being about a nearby topic does NOT make the question answerable; the specific fact asked for must be present.

3. CONTRADICTORY — Two or more retrieved passages are each applicable to the question but state conflicting requirements, thresholds, numbers, deadlines, or rules for the same matter. Surface the conflict, explain it, and list ALL conflicting passages. Do NOT silently pick one unless a passage explicitly provides a precedence/override rule (in which case explain the precedence and classify ANSWERABLE).

Rules for deciding between states:
- If applicable passages conflict, prefer CONTRADICTORY over ANSWERABLE.
- If no passage contains the specific fact asked, choose NOT_ANSWERABLE even if the topic seems related.
- Two passages that address different sub-cases (e.g. general vs a clearly-scoped special category) are NOT a contradiction ONLY IF their scopes are mutually exclusive, so that no single real situation is governed by both. If one passage says "any/all courses" and another imposes a different requirement for "core courses", their scopes OVERLAP (a core course is governed by both), and prescribing different requirements for that overlapping case IS a contradiction — do NOT silently apply "specific overrides general" unless the rulebook contains an EXPLICIT precedence/override rule. When in genuine doubt about whether two applicable passages give different answers for the same situation, prefer CONTRADICTORY.

Return ONLY a single valid JSON object, no markdown fences, with this exact schema:
{
  "state": "ANSWERABLE | NOT_ANSWERABLE | CONTRADICTORY",
  "answer": "concise answer, or an explicit statement that the rulebook does not specify it",
  "explanation": "reasoning that references the passages",
  "evidence": [
    {"rule_id": "XXX-000", "why": "why this passage supports the answer or is relevant"}
  ],
  "conflicts": [
    {"rule_ids": ["A-1", "B-2"], "nature": "what exactly conflicts and how the two passages differ"}
  ],
  "missing_information": "for NOT_ANSWERABLE, what is missing; otherwise empty string"
}

For ANSWERABLE: fill evidence, leave conflicts as []. For NOT_ANSWERABLE: evidence may be [] or list near-miss passages, conflicts [], fill missing_information. For CONTRADICTORY: fill conflicts with the conflicting rule_ids and put those same rules in evidence."""


def _build_user_message(question: str, passages: List[Dict]) -> str:
    lines = [f'QUESTION: "{question}"', "", "RETRIEVED PASSAGES:"]
    for p in passages:
        lines.append(
            f'\n[{p["rank"]}] rule_id={p["rule_id"]} | chapter="{p["chapter"]}" | '
            f'section="{p["section"]}" | subsection="{p["subsection"]}" | title="{p["title"]}"\n'
            f'exact_text: "{p["exact_text"]}"'
        )
    lines.append(
        "\n\nClassify the question and respond with ONLY the JSON object described in your instructions."
    )
    return "\n".join(lines)


def _extract_json(text: str) -> Dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def _validate_grounding(result: Dict, passages: List[Dict]) -> Dict:
    """Drop any citation whose rule_id was not actually retrieved (anti-hallucination)."""
    valid_ids = {p["rule_id"] for p in passages}

    cleaned_evidence = []
    for ev in result.get("evidence", []) or []:
        rid = ev.get("rule_id")
        if rid in valid_ids:
            cleaned_evidence.append(ev)
    result["evidence"] = cleaned_evidence

    cleaned_conflicts = []
    for c in result.get("conflicts", []) or []:
        rids = [r for r in (c.get("rule_ids") or []) if r in valid_ids]
        if len(rids) >= 2:
            c["rule_ids"] = rids
            cleaned_conflicts.append(c)
    result["conflicts"] = cleaned_conflicts

    # Safety net: if state is CONTRADICTORY but no valid conflict survived, downgrade.
    if result.get("state") == "CONTRADICTORY" and not cleaned_conflicts:
        result["state"] = "ANSWERABLE" if cleaned_evidence else "NOT_ANSWERABLE"
    return result


def _hydrate_citations(result: Dict, passages: List[Dict]) -> Dict:
    """Attach full passage metadata to cited rule_ids for the UI."""
    by_id = {p["rule_id"]: p for p in passages}

    for ev in result.get("evidence", []):
        p = by_id.get(ev["rule_id"])
        if p:
            ev.update(
                {
                    "chapter": p["chapter"],
                    "section": p["section"],
                    "subsection": p["subsection"],
                    "title": p["title"],
                    "exact_text": p["exact_text"],
                }
            )

    for c in result.get("conflicts", []):
        c["passages"] = []
        for rid in c["rule_ids"]:
            p = by_id.get(rid)
            if p:
                c["passages"].append(
                    {
                        "rule_id": p["rule_id"],
                        "chapter": p["chapter"],
                        "section": p["section"],
                        "subsection": p["subsection"],
                        "title": p["title"],
                        "exact_text": p["exact_text"],
                    }
                )
    return result


async def reason_over_passages(question: str, passages: List[Dict]) -> Dict:
    api_key = os.environ["EMERGENT_LLM_KEY"]

    if not passages:
        return {
            "state": "NOT_ANSWERABLE",
            "answer": "The rulebook does not appear to address this question.",
            "explanation": "No rulebook passages were retrieved as relevant to this question.",
            "evidence": [],
            "conflicts": [],
            "missing_information": "No relevant regulation was found in the rulebook for this topic.",
            "model": MODEL_NAME,
        }

    chat = LlmChat(
        api_key=api_key,
        session_id=f"rulebook-{uuid.uuid4()}",
        system_message=SYSTEM_PROMPT,
    ).with_model(MODEL_PROVIDER, MODEL_NAME)

    user_message = UserMessage(text=_build_user_message(question, passages))

    # Retry once on a malformed / invalid response so a single bad generation
    # does not surface as an error to the user.
    last_err = None
    for attempt in range(2):
        try:
            raw = await chat.send_message(user_message)
        except Exception as e:
            last_err = e
            logger.error("Gemini call failed (attempt %s): %s", attempt + 1, e)
            continue
        try:
            result = _extract_json(raw)
        except Exception as e:
            last_err = e
            logger.error("Failed to parse Gemini JSON (attempt %s): %s\nRAW: %s", attempt + 1, e, raw)
            continue
        state = result.get("state")
        if state not in {"ANSWERABLE", "NOT_ANSWERABLE", "CONTRADICTORY"}:
            last_err = ValueError(f"invalid state: {state}")
            logger.error("Invalid state from model (attempt %s): %s", attempt + 1, state)
            continue

        result = _validate_grounding(result, passages)
        result = _hydrate_citations(result, passages)
        result["model"] = MODEL_NAME
        result.setdefault("missing_information", "")
        result.setdefault("answer", "")
        result.setdefault("explanation", "")
        return result

    raise ValueError(f"Reasoning layer failed to produce a valid response: {last_err}")
