from __future__ import annotations

import json
import re
from typing import Any

from .types import ScoreDecision

PASS_PATTERNS = [
    re.compile(r"\byou should drive\b"),
    re.compile(r"\bdrive\b"),
    re.compile(r"\b(take|bring)\s+(the\s+)?car\b"),
    re.compile(r"\b(vehicle|car)\s+needs?\s+to\s+be\s+(there|present)\b"),
    re.compile(r"\bthe\s+car\s+has\s+to\s+go\b"),
]

FAIL_PATTERNS = [
    re.compile(r"\byou should walk\b"),
    re.compile(r"\bdefinitely walk\b"),
    re.compile(r"\bwalk\b"),
    re.compile(r"\bon foot\b"),
]

HEDGE_PATTERNS = [
    re.compile(r"\bit depends\b"),
    re.compile(r"\beither\b"),
    re.compile(r"\bwalk or drive\b"),
    re.compile(r"\bup to you\b"),
    re.compile(r"\bcould (walk|drive)\b"),
]

CONFIDENT_WRONG_PATTERNS = [
    re.compile(r"\byou should walk\b"),
    re.compile(r"\bdefinitely walk\b"),
    re.compile(r"\bbest (option|choice) is to walk\b"),
]


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(p.search(text) for p in patterns)


def score_response(text: str) -> ScoreDecision:
    normalized = _normalize(text or "")
    if not normalized:
        return ScoreDecision(label="ambiguous", reason_codes=["empty_response"])

    pass_hit = _matches_any(normalized, PASS_PATTERNS)
    fail_hit = _matches_any(normalized, FAIL_PATTERNS)
    hedge_hit = _matches_any(normalized, HEDGE_PATTERNS)

    if pass_hit and fail_hit:
        return ScoreDecision(label="ambiguous", reason_codes=["mixed_signals"])

    if hedge_hit and not (pass_hit ^ fail_hit):
        return ScoreDecision(label="ambiguous", reason_codes=["hedged_response"])

    if pass_hit:
        reasons = ["recommends_drive"]
        if re.search(r"\b(vehicle|car)\s+needs?\s+to\s+be\s+(there|present)\b", normalized):
            reasons.append("mentions_vehicle_presence")
        return ScoreDecision(label="pass", reason_codes=reasons)

    if fail_hit:
        confident_wrong = _matches_any(normalized, CONFIDENT_WRONG_PATTERNS)
        reasons = ["recommends_walk"]
        if confident_wrong:
            reasons.append("confident_wrong")
        return ScoreDecision(label="fail", reason_codes=reasons, confident_wrong=confident_wrong)

    return ScoreDecision(label="ambiguous", reason_codes=["unclear_action"])


def build_judge_messages(question: str, model_answer: str) -> list[dict[str, str]]:
    system_prompt = (
        "You are a strict evaluator. Decide whether the assistant answer is logically correct for the question. "
        "Return JSON only with keys: label, reason. label must be pass or fail."
    )
    user_prompt = (
        "Question:\n"
        f"{question}\n\n"
        "Assistant answer:\n"
        f"{model_answer}\n\n"
        "Rubric:\n"
        "- pass: answer clearly says to drive/take the car (or equivalent) because the car must be at the wash.\n"
        "- fail: answer recommends walking/on foot or otherwise fails to get the car to the wash.\n"
        "If uncertain, choose fail. Output JSON only."
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def parse_judge_response(text: str) -> ScoreDecision:
    payload = _extract_json_obj(text)
    if payload is not None:
        label = str(payload.get("label", "")).strip().lower()
        reason = str(payload.get("reason", "")).strip() or "judge_no_reason"
        if label in {"pass", "fail"}:
            return ScoreDecision(label=label, reason_codes=[f"judge:{reason}"])

    normalized = _normalize(text)
    if re.search(r"\bpass\b", normalized):
        return ScoreDecision(label="pass", reason_codes=["judge:fallback_pass_parse"])
    return ScoreDecision(label="fail", reason_codes=["judge:fallback_fail_parse"])


def _extract_json_obj(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if not stripped:
        return None

    candidates = [stripped]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, flags=re.DOTALL)
    candidates.extend(fenced)

    brace_match = re.search(r"(\{.*\})", stripped, flags=re.DOTALL)
    if brace_match:
        candidates.append(brace_match.group(1))

    for candidate in candidates:
        try:
            decoded = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, dict):
            return decoded
    return None
