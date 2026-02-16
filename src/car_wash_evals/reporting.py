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
        "models": model_summaries,
        "overall": overall,
    }


def render_report_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {summary['suite']} Report")
    lines.append("")
    lines.append(f"Generated: {summary['generated_at']}")
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
            "confident_wrong_count": 0,
            "median_latency_ms": 0,
        }

    primary_passes = sum(1 for t in trials if _primary_effective_pass(t))
    primary_fail_count = total - primary_passes
    ambiguous_count = sum(1 for t in trials if t.primary_label == "ambiguous")
    challenge_attempts = sum(1 for t in trials if t.challenge_response is not None)
    recovery_count = sum(
        1 for t in trials if t.challenge_response is not None and t.final_label == "pass"
    )
    confident_wrong_count = sum(1 for t in trials if "primary_confident_wrong" in t.reason_codes)
    latencies = [t.latency_ms for t in trials]

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
            (recovery_count / challenge_attempts) if challenge_attempts else None
        ),
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
            "confident_wrong_count": 0,
            "median_latency_ms": 0,
        }

    total_primary_fail = sum(m["primary_fail_count"] for m in model_summaries)
    total_primary_pass = total_trials - total_primary_fail
    total_ambiguous = sum(m["ambiguous_count"] for m in model_summaries)
    total_confident_wrong = sum(m["confident_wrong_count"] for m in model_summaries)

    weighted_recovery_numerator = 0.0
    weighted_recovery_denominator = 0
    for m in model_summaries:
        total_runs = m["total_runs"]
        primary_fail = m["primary_fail_count"]
        recovery_rate = m["recovery_rate_after_challenge"]
        if recovery_rate is not None and primary_fail > 0:
            weighted_recovery_numerator += recovery_rate * primary_fail
            weighted_recovery_denominator += primary_fail

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
        "confident_wrong_count": total_confident_wrong,
        "median_latency_ms": int(statistics.median(latencies)),
    }


def _primary_effective_pass(result: TrialResult) -> bool:
    return result.challenge_response is None and result.final_label == "pass"


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
