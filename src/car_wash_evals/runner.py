from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from .openrouter_client import OpenRouterClient, OpenRouterError
from .reporting import aggregate_results, write_outputs
from .scoring import build_judge_messages, parse_judge_response, score_response
from .types import ExecutionConfig, ModelAlias, PromptConfig, ScoreDecision, SuiteConfig, TrialResult


class ConfigError(ValueError):
    """Raised when suite or alias configuration is invalid."""


@dataclass(frozen=True)
class TrialJob:
    model_alias: str
    resolved_model_id: str
    trial_index: int


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run car wash paradox evals via OpenRouter")
    parser.add_argument("--suite", required=True, type=Path, help="Path to suite YAML")
    parser.add_argument(
        "--aliases",
        type=Path,
        default=Path("config/model_aliases.yaml"),
        help="Path to model alias YAML",
    )
    parser.add_argument("--runs", type=int, default=10, help="Independent trials per model")
    parser.add_argument("--out", type=Path, default=Path("results"), help="Output directory")
    parser.add_argument(
        "--judge-model",
        type=str,
        default=None,
        help="OpenRouter judge model for ambiguous cases",
    )
    parser.add_argument("--concurrency", type=int, default=4, help="Concurrent trial workers")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        _validate_inputs(args)
        suite_config = load_suite_config(args.suite)
        aliases = load_alias_config(args.aliases)

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ConfigError("Missing OPENROUTER_API_KEY in environment")

        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        client = OpenRouterClient(api_key=api_key, base_url=base_url)

        available_models = client.list_models()
        resolved_models = resolve_model_aliases(suite_config.models, aliases, available_models)

        trial_results = run_trials(
            client=client,
            suite=suite_config,
            resolved_models=resolved_models,
            runs=args.runs,
            judge_model=args.judge_model,
            concurrency=args.concurrency,
        )

        run_timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        summary = aggregate_results(
            results=trial_results,
            aliases=aliases,
            resolved_models=resolved_models,
            model_order=suite_config.models,
            suite_name=suite_config.name,
            runs_per_model=args.runs,
            judge_model=args.judge_model,
        )

        output_paths = write_outputs(
            out_dir=args.out,
            run_timestamp=run_timestamp,
            trial_results=trial_results,
            summary=summary,
        )

        print("Run completed successfully.")
        print(json.dumps(output_paths, indent=2))
        return 0
    except (ConfigError, OpenRouterError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive path
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


def load_suite_config(path: Path) -> SuiteConfig:
    data = _load_yaml(path)

    if not isinstance(data, dict):
        raise ConfigError("Suite config must be a mapping")

    name = _required_str(data, "name")
    description = _required_str(data, "description")
    models = _required_list_of_str(data, "models")

    prompts_data = data.get("prompts")
    if not isinstance(prompts_data, dict):
        raise ConfigError("Suite config requires prompts mapping")
    prompts = PromptConfig(
        primary=_required_str(prompts_data, "primary"),
        challenge_followup=_required_str(prompts_data, "challenge_followup"),
    )

    exec_data = data.get("execution")
    if not isinstance(exec_data, dict):
        raise ConfigError("Suite config requires execution mapping")

    execution = ExecutionConfig(
        temperature=float(exec_data.get("temperature", 0.7)),
        max_tokens=int(exec_data.get("max_tokens", 200)),
        challenge_policy=str(exec_data.get("challenge_policy", "on_nonpass_primary")),
    )
    if execution.challenge_policy != "on_nonpass_primary":
        raise ConfigError("execution.challenge_policy must be 'on_nonpass_primary'")

    return SuiteConfig(
        name=name,
        description=description,
        models=models,
        prompts=prompts,
        execution=execution,
    )


def load_alias_config(path: Path) -> dict[str, ModelAlias]:
    data = _load_yaml(path)
    if not isinstance(data, dict):
        raise ConfigError("Alias config must be a mapping")

    aliases: dict[str, ModelAlias] = {}
    for alias, raw in data.items():
        if not isinstance(alias, str):
            raise ConfigError("Alias keys must be strings")
        if not isinstance(raw, dict):
            raise ConfigError(f"Alias '{alias}' must map to an object")

        display_name = _required_str(raw, "display_name")
        provider = _required_str(raw, "provider")
        if provider not in {"openai", "google", "anthropic"}:
            raise ConfigError(f"Alias '{alias}' has invalid provider '{provider}'")

        candidate_model_ids = _required_list_of_str(raw, "candidate_model_ids")
        aliases[alias] = ModelAlias(
            display_name=display_name,
            provider=provider,
            candidate_model_ids=candidate_model_ids,
        )

    return aliases


def resolve_model_aliases(
    suite_model_aliases: list[str],
    aliases: dict[str, ModelAlias],
    available_models: set[str],
) -> dict[str, str]:
    resolved: dict[str, str] = {}
    unresolved: list[str] = []

    for alias in suite_model_aliases:
        if alias not in aliases:
            raise ConfigError(f"Model alias '{alias}' not found in alias config")

        alias_meta = aliases[alias]
        model_id = next(
            (candidate for candidate in alias_meta.candidate_model_ids if candidate in available_models),
            None,
        )
        if model_id is None:
            unresolved.append(alias)
            continue
        resolved[alias] = model_id

    if unresolved:
        details = ", ".join(
            f"{alias} -> {aliases[alias].candidate_model_ids}" for alias in unresolved
        )
        raise ConfigError(
            "Could not resolve aliases to available OpenRouter models: "
            f"{details}"
        )

    return resolved


def run_trials(
    client: OpenRouterClient,
    suite: SuiteConfig,
    resolved_models: dict[str, str],
    runs: int,
    judge_model: str | None,
    concurrency: int,
) -> list[TrialResult]:
    run_id = f"{suite.name}-{uuid.uuid4().hex[:8]}"
    jobs: list[TrialJob] = []
    for alias in suite.models:
        for trial_index in range(1, runs + 1):
            jobs.append(
                TrialJob(
                    model_alias=alias,
                    resolved_model_id=resolved_models[alias],
                    trial_index=trial_index,
                )
            )

    results: list[TrialResult] = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(
                _run_single_trial,
                client,
                suite,
                job,
                run_id,
                judge_model,
            ): job
            for job in jobs
        }

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    model_order_idx = {alias: idx for idx, alias in enumerate(suite.models)}
    return sorted(results, key=lambda r: (model_order_idx[r.model_alias], r.trial_index))


def _run_single_trial(
    client: OpenRouterClient,
    suite: SuiteConfig,
    job: TrialJob,
    run_id: str,
    judge_model: str | None,
) -> TrialResult:
    start_time = time.perf_counter()
    usage_total: dict[str, Any] | None = None
    reason_codes: list[str] = []

    primary_chat = client.chat_completion(
        model=job.resolved_model_id,
        messages=[{"role": "user", "content": suite.prompts.primary}],
        temperature=suite.execution.temperature,
        max_tokens=suite.execution.max_tokens,
    )
    usage_total = _merge_usage(usage_total, primary_chat.usage)

    primary_decision = score_response(primary_chat.text)
    reason_codes.extend(f"primary_{code}" for code in primary_decision.reason_codes)
    if primary_decision.confident_wrong:
        reason_codes.append("primary_confident_wrong")

    primary_effective_label = _effective_label(
        client=client,
        decision=primary_decision,
        judge_model=judge_model,
        question=suite.prompts.primary,
        response=primary_chat.text,
        usage_total=usage_total,
        reason_codes=reason_codes,
    )
    usage_total = primary_effective_label.usage_total

    challenge_response: str | None = None
    challenge_label = None

    final_label = primary_effective_label.label
    if suite.execution.challenge_policy == "on_nonpass_primary" and primary_effective_label.label != "pass":
        challenge_chat = client.chat_completion(
            model=job.resolved_model_id,
            messages=[
                {"role": "user", "content": suite.prompts.primary},
                {"role": "assistant", "content": primary_chat.text},
                {"role": "user", "content": suite.prompts.challenge_followup},
            ],
            temperature=suite.execution.temperature,
            max_tokens=suite.execution.max_tokens,
        )
        usage_total = _merge_usage(usage_total, challenge_chat.usage)

        challenge_response = challenge_chat.text
        challenge_decision = score_response(challenge_chat.text)
        challenge_label = challenge_decision.label
        reason_codes.extend(f"challenge_{code}" for code in challenge_decision.reason_codes)

        challenge_effective_label = _effective_label(
            client=client,
            decision=challenge_decision,
            judge_model=judge_model,
            question=suite.prompts.challenge_followup,
            response=challenge_chat.text,
            usage_total=usage_total,
            reason_codes=reason_codes,
            scope="challenge",
        )
        usage_total = challenge_effective_label.usage_total
        final_label = challenge_effective_label.label

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return TrialResult(
        run_id=run_id,
        model_alias=job.model_alias,
        resolved_model_id=job.resolved_model_id,
        trial_index=job.trial_index,
        primary_response=primary_chat.text,
        primary_label=primary_decision.label,
        challenge_response=challenge_response,
        challenge_label=challenge_label,
        final_label=final_label,
        reason_codes=reason_codes,
        latency_ms=latency_ms,
        token_usage=usage_total,
        timestamp=datetime.now(UTC).isoformat(),
    )

@dataclass(frozen=True)
class EffectiveLabelResult:
    label: str
    usage_total: dict[str, Any] | None


def _effective_label(
    client: OpenRouterClient,
    decision: ScoreDecision,
    judge_model: str | None,
    question: str,
    response: str,
    usage_total: dict[str, Any] | None,
    reason_codes: list[str],
    scope: str = "primary",
) -> EffectiveLabelResult:

    if decision.label != "ambiguous":
        return EffectiveLabelResult(label=decision.label, usage_total=usage_total)

    if not judge_model:
        reason_codes.append(f"{scope}_ambiguous_without_judge")
        return EffectiveLabelResult(label="fail", usage_total=usage_total)

    judge_chat = client.chat_completion(
        model=judge_model,
        messages=build_judge_messages(question=question, model_answer=response),
        temperature=0.0,
        max_tokens=120,
    )
    usage_total = _merge_usage(usage_total, judge_chat.usage)

    judge_decision = parse_judge_response(judge_chat.text)
    reason_codes.extend(f"{scope}_{code}" for code in judge_decision.reason_codes)
    return EffectiveLabelResult(label=judge_decision.label, usage_total=usage_total)


def _merge_usage(
    current: dict[str, Any] | None,
    incoming: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if incoming is None:
        return current
    if current is None:
        return dict(incoming)

    merged = dict(current)
    for key, value in incoming.items():
        if isinstance(value, (int, float)) and isinstance(merged.get(key), (int, float)):
            merged[key] = merged[key] + value
        elif isinstance(value, (int, float)) and key not in merged:
            merged[key] = value
        else:
            merged[key] = value
    return merged


def _validate_inputs(args: argparse.Namespace) -> None:
    if args.runs <= 0:
        raise ConfigError("--runs must be > 0")
    if args.concurrency <= 0:
        raise ConfigError("--concurrency must be > 0")
    if not args.suite.exists():
        raise ConfigError(f"Suite file not found: {args.suite}")
    if not args.aliases.exists():
        raise ConfigError(f"Aliases file not found: {args.aliases}")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"YAML at {path} must be a mapping")
    return data


def _required_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"Missing or invalid string field: {key}")
    return value.strip()


def _required_list_of_str(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ConfigError(f"Missing or invalid list field: {key}")
    items = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"List field '{key}' must only contain non-empty strings")
        items.append(item.strip())
    return items


if __name__ == "__main__":
    raise SystemExit(main())
