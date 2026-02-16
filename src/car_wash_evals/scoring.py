from __future__ import annotations

import json
import re
from typing import Any

from .types import ScoreDecision

PRIMARY_SCORING_MODES = {
    "full_response",
    "direct_answer_first",
    "direct_and_consistent",
}

PASS_PATTERNS = [
    re.compile(r"\byou should drive\b"),
    re.compile(r"\bdrive\b"),
    re.compile(r"^\*{0,2}drive\*{0,2}\b"),
    re.compile(r"\bdrive (it|the car|there)\b"),
    re.compile(r"\b(take|bring)\s+(the\s+)?car\b"),
    re.compile(r"\b(vehicle|car)\s+needs?\s+to\s+be\s+(there|present)\b"),
    re.compile(r"\bthe\s+car\s+has\s+to\s+go\b"),
]

FAIL_PATTERNS = [
    re.compile(r"^\*{0,2}walk\*{0,2}\b"),
    re.compile(r"\byou should walk\b"),
    re.compile(r"\bdefinitely walk\b"),
    re.compile(r"\b(can|could)\s+walk\b"),
    re.compile(r"\bwalk there\b"),
    re.compile(r"\bwalking (is|would be) (faster|quicker|better|best|fine|okay|ok)\b"),
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
    re.compile(r"^\*{0,2}walk\*{0,2}\b"),
    re.compile(r"\byou should walk\b"),
    re.compile(r"\bdefinitely walk\b"),
    re.compile(r"\bbest (option|choice) is to walk\b"),
]


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _matches_any(text: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(p.search(text) for p in patterns)


def score_response(text: str, mode: str = "full_response") -> ScoreDecision:
    if mode == "full_response":
        return _score_full_response(text)
    if mode == "direct_answer_first":
        return _score_direct_answer_first(text)
    if mode == "direct_and_consistent":
        return _score_direct_and_consistent(text)
    raise ValueError(f"Unsupported scoring mode: {mode}")


def score_response_across_modes(
    text: str,
    modes: list[str] | None = None,
) -> dict[str, ScoreDecision]:
    requested = modes or sorted(PRIMARY_SCORING_MODES)
    results: dict[str, ScoreDecision] = {}
    for mode in requested:
        if mode not in PRIMARY_SCORING_MODES:
            raise ValueError(f"Unsupported scoring mode: {mode}")
        results[mode] = score_response(text, mode=mode)
    return results


def _score_full_response(text: str) -> ScoreDecision:
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
        confident_wrong = _matches_any(normalized, CONFIDENT_WRONG_PATTERNS) or _starts_with_walk_answer(
            text or ""
        )
        reasons = ["recommends_walk"]
        if confident_wrong:
            reasons.append("confident_wrong")
        return ScoreDecision(label="fail", reason_codes=reasons, confident_wrong=confident_wrong)

    return ScoreDecision(label="ambiguous", reason_codes=["unclear_action"])


def _score_direct_answer_first(text: str) -> ScoreDecision:
    direct_answer = extract_direct_answer_span(text)
    if not direct_answer:
        return ScoreDecision(label="ambiguous", reason_codes=["no_direct_answer_span"])
    base = _score_full_response(direct_answer)
    return ScoreDecision(
        label=base.label,
        reason_codes=[f"direct_first_{code}" for code in base.reason_codes],
        confident_wrong=base.confident_wrong,
    )


def _score_direct_and_consistent(text: str) -> ScoreDecision:
    direct = _score_direct_answer_first(text)
    full = _score_full_response(text)

    if direct.label == "pass":
        if full.label == "fail":
            return ScoreDecision(
                label="fail",
                reason_codes=["direct_first_pass_but_full_fail", "contradictory_followup_reasoning"],
            )
        if full.label == "ambiguous":
            return ScoreDecision(
                label="fail",
                reason_codes=["direct_first_pass_but_full_ambiguous", "missing_consistency"],
            )
        return ScoreDecision(label="pass", reason_codes=["direct_first_pass_and_consistent"])

    if direct.label == "fail":
        reasons = ["direct_first_fail"]
        if direct.confident_wrong:
            reasons.append("confident_wrong")
        return ScoreDecision(label="fail", reason_codes=reasons, confident_wrong=direct.confident_wrong)

    if full.label == "pass":
        return ScoreDecision(
            label="fail",
            reason_codes=["no_clear_direct_answer_first", "full_response_only_pass"],
        )
    if full.label == "fail":
        return ScoreDecision(label="fail", reason_codes=["direct_first_ambiguous_full_fail"])
    return ScoreDecision(label="ambiguous", reason_codes=["direct_first_ambiguous_full_ambiguous"])


def extract_direct_answer_span(text: str) -> str:
    stripped = (text or "").strip()
    if not stripped:
        return ""

    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    if not lines:
        return ""

    first_line = _strip_markdown(lines[0])
    if not first_line:
        return ""

    sentence_match = re.match(r"(.+?[.?!])(?:\s|$)", first_line)
    if sentence_match:
        return sentence_match.group(1).strip()
    return " ".join(first_line.split()[:12]).strip()


def _strip_markdown(text: str) -> str:
    cleaned = re.sub(r"^[>\-\*\d\.\)\s]+", "", text.strip())
    cleaned = cleaned.replace("**", "").replace("__", "").replace("`", "")
    return cleaned.strip()


def _starts_with_walk_answer(text: str) -> bool:
    direct_answer = extract_direct_answer_span(text)
    normalized = _normalize(direct_answer)
    return bool(re.match(r"^walk\b", normalized))


def build_judge_messages(
    question: str,
    model_answer: str,
    scope: str = "primary",
) -> list[dict[str, str]]:
    system_prompt = (
        "You are a strict evaluator. Decide whether the assistant answer is logically correct for the question. "
        "Return JSON only with keys: label, reason. label must be pass or fail."
    )
    challenge_clarification = ""
    if scope == "challenge":
        challenge_clarification = (
            "\nChallenge clarification:\n"
            "- The phrase 'if I am walking' does NOT imply inability to drive.\n"
            "- Answers that say to walk to the car and then drive it (or otherwise get the car to the wash) can pass.\n"
            "- Failing means the answer still does not get the car to the wash."
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
        f"{challenge_clarification}"
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
