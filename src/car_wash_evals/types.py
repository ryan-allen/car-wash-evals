from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Label = Literal["pass", "fail", "ambiguous"]
FinalLabel = Literal["pass", "fail"]


@dataclass(frozen=True)
class ModelAlias:
    display_name: str
    provider: Literal["openai", "google", "anthropic"]
    candidate_model_ids: list[str]


@dataclass(frozen=True)
class PromptConfig:
    primary: str
    challenge_followup: str


@dataclass(frozen=True)
class ExecutionConfig:
    temperature: float = 0.7
    max_tokens: int = 200
    challenge_policy: Literal["on_nonpass_primary"] = "on_nonpass_primary"


@dataclass(frozen=True)
class SuiteConfig:
    name: str
    description: str
    models: list[str]
    prompts: PromptConfig
    execution: ExecutionConfig


@dataclass(frozen=True)
class ScoreDecision:
    label: Label
    reason_codes: list[str] = field(default_factory=list)
    confident_wrong: bool = False


@dataclass
class TrialResult:
    run_id: str
    model_alias: str
    resolved_model_id: str
    trial_index: int
    primary_response: str
    primary_label: Label
    challenge_response: str | None
    challenge_label: Label | None
    final_label: FinalLabel
    reason_codes: list[str]
    latency_ms: int
    token_usage: dict[str, Any] | None
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
