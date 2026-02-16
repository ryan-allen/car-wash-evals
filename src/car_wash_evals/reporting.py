from __future__ import annotations

import json
import shutil
import statistics
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .types import ModelAlias, TrialResult


def aggregate_results(
    results: list[TrialResult],
    aliases: dict[str, ModelAlias],
    resolved_models: dict[str, str],
    model_order: list[str],
    suite_name: str,
    runs_per_model: int,
    judge_model: str | None,
    primary_scoring_mode: str = "full_response",
    shadow_primary_scoring_modes: list[str] | None = None,
) -> dict[str, Any]:
    by_alias: dict[str, list[TrialResult]] = {alias: [] for alias in model_order}
    for result in results:
        by_alias.setdefault(result.model_alias, []).append(result)

    model_summaries: list[dict[str, Any]] = []
    for alias in model_order:
        trials = sorted(by_alias.get(alias, []), key=lambda t: t.trial_index)
        alias_meta = aliases[alias]
        summary = _summarize_model_trials(
            alias=alias,
            alias_meta=alias_meta,
            resolved_model_id=resolved_models[alias],
            trials=trials,
        )
        model_summaries.append(summary)

    overall = _summarize_overall(model_summaries)

    return {
        "suite": suite_name,
        "generated_at": datetime.now(UTC).isoformat(),
        "runs_per_model": runs_per_model,
        "judge_model": judge_model,
        "primary_scoring_mode": primary_scoring_mode,
        "shadow_primary_scoring_modes": shadow_primary_scoring_modes or [],
        "models": model_summaries,
        "overall": overall,
    }


def render_report_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {summary['suite']} Report")
    lines.append("")
    lines.append(f"Generated: {summary['generated_at']}")
    lines.append(f"Primary scoring mode: {summary.get('primary_scoring_mode', 'full_response')}")
    shadow_modes = summary.get("shadow_primary_scoring_modes", [])
    if shadow_modes:
        lines.append(f"Shadow scoring modes: {', '.join(shadow_modes)}")
    lines.append("")
    runs_per_model = summary.get("runs_per_model", 10)
    lines.append(
        "| Provider | Display Model Name | Resolved OpenRouter Model ID | "
        f"Primary Pass Rate ({runs_per_model} runs) | Primary Fail Count | Ambiguous Count | "
        "Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |"
    )
    lines.append(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )

    for model in summary["models"]:
        lines.append(
            "| {provider} | {display_name} | {resolved_model_id} | {primary_pass_rate} | {primary_fail_count} | {ambiguous_count} | {recovery_rate_after_challenge} | {confident_wrong_count} | {median_latency_ms} ms |".format(
                provider=model["provider"],
                display_name=model["display_name"],
                resolved_model_id=model["resolved_model_id"],
                primary_pass_rate=_fmt_pct(model["primary_pass_rate"]),
                primary_fail_count=model["primary_fail_count"],
                ambiguous_count=model["ambiguous_count"],
                recovery_rate_after_challenge=_fmt_pct_or_na(
                    model["recovery_rate_after_challenge"]
                ),
                confident_wrong_count=model["confident_wrong_count"],
                median_latency_ms=model["median_latency_ms"],
            )
        )

    mode_columns = sorted(
        {
            mode
            for model in summary["models"]
            for mode in (model.get("primary_pass_rate_by_mode") or {}).keys()
        }
    )
    if mode_columns:
        lines.append("")
        lines.append("## Primary Pass Rate By Mode (Deterministic Pre-Judge)")
        lines.append("")
        header = "| Display Model Name | " + " | ".join(mode_columns) + " |"
        divider = "| --- | " + " | ".join("---" for _ in mode_columns) + " |"
        lines.append(header)
        lines.append(divider)
        for model in summary["models"]:
            rates = model.get("primary_pass_rate_by_mode") or {}
            values = [_fmt_pct_or_na(rates.get(mode)) for mode in mode_columns]
            lines.append(f"| {model['display_name']} | {' | '.join(values)} |")

    overall = summary["overall"]
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append(f"- Total trials: {overall['total_trials']}")
    lines.append(f"- Primary pass rate: {_fmt_pct(overall['primary_pass_rate'])}")
    lines.append(f"- Primary fail count: {overall['primary_fail_count']}")
    lines.append(f"- Ambiguous count: {overall['ambiguous_count']}")
    lines.append(
        f"- Recovery rate after challenge: {_fmt_pct_or_na(overall['recovery_rate_after_challenge'])}"
    )
    if overall.get("recovery_rate_by_followup_index"):
        lines.append("- Recovery rate by challenge follow-up:")
        for idx, value in sorted(
            overall["recovery_rate_by_followup_index"].items(),
            key=lambda item: int(item[0]),
        ):
            lines.append(f"  - followup_{idx}: {_fmt_pct_or_na(value)}")
    if overall.get("primary_pass_rate_by_mode"):
        lines.append("- Primary pass rate by mode (deterministic pre-judge):")
        for mode, value in sorted(overall["primary_pass_rate_by_mode"].items()):
            lines.append(f"  - {mode}: {_fmt_pct(value)}")
    lines.append(f"- Confident-wrong count: {overall['confident_wrong_count']}")
    lines.append(f"- Median latency: {overall['median_latency_ms']} ms")
    return "\n".join(lines) + "\n"


def write_outputs(
    out_dir: Path,
    run_timestamp: str,
    trial_results: list[TrialResult],
    summary: dict[str, Any],
) -> dict[str, str]:
    run_dir = out_dir / run_timestamp
    run_dir.mkdir(parents=True, exist_ok=False)

    raw_path = run_dir / "raw.jsonl"
    with raw_path.open("w", encoding="utf-8") as f:
        for result in trial_results:
            f.write(json.dumps(result.to_dict(), ensure_ascii=True) + "\n")

    summary_path = run_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    report_path = run_dir / "report.md"
    report_path.write_text(render_report_markdown(summary), encoding="utf-8")

    latest_path = out_dir / "latest"
    _reset_path(latest_path)
    try:
        latest_path.symlink_to(run_dir.name, target_is_directory=True)
    except OSError:
        shutil.copytree(run_dir, latest_path)

    return {
        "run_dir": str(run_dir),
        "raw_jsonl": str(raw_path),
        "summary_json": str(summary_path),
        "report_md": str(report_path),
        "latest": str(latest_path),
    }


def _summarize_model_trials(
    alias: str,
    alias_meta: ModelAlias,
    resolved_model_id: str,
    trials: list[TrialResult],
) -> dict[str, Any]:
    total = len(trials)
    if total == 0:
        return {
            "model_alias": alias,
            "provider": alias_meta.provider,
            "display_name": alias_meta.display_name,
            "resolved_model_id": resolved_model_id,
            "total_runs": 0,
            "primary_pass_rate": 0.0,
            "primary_fail_count": 0,
            "ambiguous_count": 0,
            "recovery_rate_after_challenge": None,
            "challenge_trial_count": 0,
            "recovery_rate_by_followup_index": {},
            "primary_pass_rate_by_mode": {},
            "confident_wrong_count": 0,
            "median_latency_ms": 0,
        }

    primary_passes = sum(1 for t in trials if _primary_effective_pass(t))
    primary_fail_count = total - primary_passes
    ambiguous_count = sum(1 for t in trials if t.primary_label == "ambiguous")
    challenge_trial_count = sum(1 for t in trials if _challenge_attempted(t))
    recovery_count = sum(1 for t in trials if _challenge_attempted(t) and _trial_recovered(t))
    challenge_attempts_by_followup_index, recoveries_by_followup_index = _challenge_index_counts(trials)
    confident_wrong_count = sum(1 for t in trials if "primary_confident_wrong" in t.reason_codes)
    latencies = [t.latency_ms for t in trials]
    primary_pass_rate_by_mode = _compute_mode_pass_rates(trials)
    recovery_rate_by_followup_index: dict[str, float | None] = {}
    for idx, attempts in challenge_attempts_by_followup_index.items():
        if attempts > 0:
            recovery_rate_by_followup_index[idx] = (
                recoveries_by_followup_index.get(idx, 0) / attempts
            )
        else:
            recovery_rate_by_followup_index[idx] = None

    return {
        "model_alias": alias,
        "provider": alias_meta.provider,
        "display_name": alias_meta.display_name,
        "resolved_model_id": resolved_model_id,
        "total_runs": total,
        "primary_pass_rate": primary_passes / total,
        "primary_fail_count": primary_fail_count,
        "ambiguous_count": ambiguous_count,
        "recovery_rate_after_challenge": (
            (recovery_count / challenge_trial_count) if challenge_trial_count else None
        ),
        "challenge_trial_count": challenge_trial_count,
        "recovery_rate_by_followup_index": recovery_rate_by_followup_index,
        "challenge_attempts_by_followup_index": challenge_attempts_by_followup_index,
        "recoveries_by_followup_index": recoveries_by_followup_index,
        "primary_pass_rate_by_mode": primary_pass_rate_by_mode,
        "confident_wrong_count": confident_wrong_count,
        "median_latency_ms": int(statistics.median(latencies)),
    }


def _summarize_overall(model_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    total_trials = sum(m["total_runs"] for m in model_summaries)
    if total_trials == 0:
        return {
            "total_trials": 0,
            "primary_pass_rate": 0.0,
            "primary_fail_count": 0,
            "ambiguous_count": 0,
            "recovery_rate_after_challenge": None,
            "recovery_rate_by_followup_index": {},
            "primary_pass_rate_by_mode": {},
            "confident_wrong_count": 0,
            "median_latency_ms": 0,
        }

    total_primary_fail = sum(m["primary_fail_count"] for m in model_summaries)
    total_primary_pass = total_trials - total_primary_fail
    total_ambiguous = sum(m["ambiguous_count"] for m in model_summaries)
    total_confident_wrong = sum(m["confident_wrong_count"] for m in model_summaries)
    mode_rates = _combine_mode_rates(model_summaries)
    recovery_rate_by_followup_index = _combine_followup_recovery_rates(model_summaries)

    weighted_recovery_numerator = 0.0
    weighted_recovery_denominator = 0
    for m in model_summaries:
        challenge_trials = int(m.get("challenge_trial_count", 0))
        recovery_rate = m["recovery_rate_after_challenge"]
        if recovery_rate is not None and challenge_trials > 0:
            weighted_recovery_numerator += recovery_rate * challenge_trials
            weighted_recovery_denominator += challenge_trials

    latencies = [m["median_latency_ms"] for m in model_summaries]

    return {
        "total_trials": total_trials,
        "primary_pass_rate": total_primary_pass / total_trials,
        "primary_fail_count": total_primary_fail,
        "ambiguous_count": total_ambiguous,
        "recovery_rate_after_challenge": (
            (weighted_recovery_numerator / weighted_recovery_denominator)
            if weighted_recovery_denominator > 0
            else None
        ),
        "recovery_rate_by_followup_index": recovery_rate_by_followup_index,
        "primary_pass_rate_by_mode": mode_rates,
        "confident_wrong_count": total_confident_wrong,
        "median_latency_ms": int(statistics.median(latencies)),
    }


def _primary_effective_pass(result: TrialResult) -> bool:
    return (not _challenge_attempted(result)) and result.final_label == "pass"


def _challenge_attempted(result: TrialResult) -> bool:
    return bool(result.challenge_attempts) or result.challenge_response is not None


def _trial_recovered(result: TrialResult) -> bool:
    if result.challenge_attempts:
        return any(
            attempt.get("effective_label") == "pass"
            for attempt in result.challenge_attempts
            if isinstance(attempt, dict)
        )
    return result.challenge_response is not None and result.final_label == "pass"


def _challenge_index_counts(
    trials: list[TrialResult],
) -> tuple[dict[str, int], dict[str, int]]:
    attempts_by_index: dict[str, int] = {}
    recoveries_by_index: dict[str, int] = {}
    for trial in trials:
        if trial.challenge_attempts:
            for attempt in trial.challenge_attempts:
                if not isinstance(attempt, dict):
                    continue
                raw_index = attempt.get("index")
                index_key = str(raw_index) if isinstance(raw_index, int) else "1"
                attempts_by_index[index_key] = attempts_by_index.get(index_key, 0) + 1
                if attempt.get("effective_label") == "pass":
                    recoveries_by_index[index_key] = recoveries_by_index.get(index_key, 0) + 1
            continue

        if trial.challenge_response is not None:
            attempts_by_index["1"] = attempts_by_index.get("1", 0) + 1
            if trial.final_label == "pass":
                recoveries_by_index["1"] = recoveries_by_index.get("1", 0) + 1
    return attempts_by_index, recoveries_by_index


def _compute_mode_pass_rates(trials: list[TrialResult]) -> dict[str, float]:
    mode_totals: dict[str, int] = {}
    mode_passes: dict[str, int] = {}
    for trial in trials:
        labels = trial.primary_mode_labels or {}
        for mode, label in labels.items():
            mode_totals[mode] = mode_totals.get(mode, 0) + 1
            if label == "pass":
                mode_passes[mode] = mode_passes.get(mode, 0) + 1

    rates: dict[str, float] = {}
    for mode, total in mode_totals.items():
        if total > 0:
            rates[mode] = mode_passes.get(mode, 0) / total
    return rates


def _combine_mode_rates(model_summaries: list[dict[str, Any]]) -> dict[str, float]:
    mode_weighted_total: dict[str, float] = {}
    mode_trial_total: dict[str, int] = {}

    for summary in model_summaries:
        total_runs = int(summary.get("total_runs", 0))
        for mode, rate in (summary.get("primary_pass_rate_by_mode") or {}).items():
            mode_weighted_total[mode] = mode_weighted_total.get(mode, 0.0) + (float(rate) * total_runs)
            mode_trial_total[mode] = mode_trial_total.get(mode, 0) + total_runs

    combined: dict[str, float] = {}
    for mode, total in mode_trial_total.items():
        if total > 0:
            combined[mode] = mode_weighted_total[mode] / total
    return combined


def _combine_followup_recovery_rates(model_summaries: list[dict[str, Any]]) -> dict[str, float | None]:
    attempts_totals: dict[str, int] = {}
    recoveries_totals: dict[str, int] = {}

    for summary in model_summaries:
        attempts = summary.get("challenge_attempts_by_followup_index") or {}
        recoveries = summary.get("recoveries_by_followup_index") or {}
        for idx, count in attempts.items():
            attempts_totals[idx] = attempts_totals.get(idx, 0) + int(count)
        for idx, count in recoveries.items():
            recoveries_totals[idx] = recoveries_totals.get(idx, 0) + int(count)

    rates: dict[str, float | None] = {}
    for idx, total in attempts_totals.items():
        if total > 0:
            rates[idx] = recoveries_totals.get(idx, 0) / total
        else:
            rates[idx] = None
    return rates


def _fmt_pct(value: float) -> str:
    return f"{(value * 100):.1f}%"


def _fmt_pct_or_na(value: float | None) -> str:
    if value is None:
        return "n/a"
    return _fmt_pct(value)


def _reset_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)
