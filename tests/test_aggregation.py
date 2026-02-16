import json
import unittest
from pathlib import Path

from car_wash_evals.openrouter_client import ChatResponse
from car_wash_evals.reporting import aggregate_results, render_report_markdown
from car_wash_evals.runner import ConfigError, TrialJob, _run_single_trial, resolve_model_aliases
from car_wash_evals.types import ExecutionConfig, ModelAlias, PromptConfig, SuiteConfig, TrialResult


class DummyClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.call_count = 0

    def chat_completion(self, model: str, messages: list[dict[str, str]], temperature: float, max_tokens: int) -> ChatResponse:  # noqa: ARG002
        self.call_count += 1
        if not self.responses:
            raise AssertionError("No dummy responses left")
        return ChatResponse(text=self.responses.pop(0), usage={"total_tokens": 10})


class AggregationTest(unittest.TestCase):
    def _fixture_results(self) -> list[TrialResult]:
        fixture_path = Path(__file__).parent / "fixtures" / "sample_results.json"
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        return [TrialResult(**item) for item in payload]

    def _alias_map(self) -> dict[str, ModelAlias]:
        return {
            "chatgpt_5_2_instant": ModelAlias(
                display_name="ChatGPT 5.2 Instant",
                provider="openai",
                candidate_model_ids=["openai/gpt-5-mini"],
            ),
            "gemini_3_fast": ModelAlias(
                display_name="Gemini 3 Fast",
                provider="google",
                candidate_model_ids=["google/gemini-2.0-flash-001"],
            ),
        }

    def test_aggregate_summary_metrics(self) -> None:
        results = self._fixture_results()
        aliases = self._alias_map()
        resolved = {
            "chatgpt_5_2_instant": "openai/gpt-5-mini",
            "gemini_3_fast": "google/gemini-2.0-flash-001",
        }

        summary = aggregate_results(
            results=results,
            aliases=aliases,
            resolved_models=resolved,
            model_order=["chatgpt_5_2_instant", "gemini_3_fast"],
            suite_name="car_wash_core9",
            runs_per_model=3,
            judge_model="openai/gpt-4.1-mini",
        )

        first = summary["models"][0]
        self.assertAlmostEqual(first["primary_pass_rate"], 2 / 3)
        self.assertEqual(first["primary_fail_count"], 1)
        self.assertEqual(first["ambiguous_count"], 1)
        self.assertAlmostEqual(first["recovery_rate_after_challenge"], 1.0)
        self.assertEqual(first["confident_wrong_count"], 1)
        self.assertEqual(first["median_latency_ms"], 120)

        overall = summary["overall"]
        self.assertEqual(overall["total_trials"], 6)
        self.assertAlmostEqual(overall["primary_pass_rate"], 0.5)
        self.assertEqual(overall["ambiguous_count"], 1)
        self.assertAlmostEqual(overall["recovery_rate_after_challenge"], 1 / 3)
        self.assertEqual(overall["median_latency_ms"], 105)

    def test_report_markdown_contains_expected_columns(self) -> None:
        results = self._fixture_results()
        aliases = self._alias_map()
        resolved = {
            "chatgpt_5_2_instant": "openai/gpt-5-mini",
            "gemini_3_fast": "google/gemini-2.0-flash-001",
        }
        summary = aggregate_results(
            results=results,
            aliases=aliases,
            resolved_models=resolved,
            model_order=["chatgpt_5_2_instant", "gemini_3_fast"],
            suite_name="car_wash_core9",
            runs_per_model=3,
            judge_model=None,
        )

        report = render_report_markdown(summary)
        self.assertIn("| Provider | Display Model Name | Resolved OpenRouter Model ID |", report)
        self.assertIn("ChatGPT 5.2 Instant", report)
        self.assertIn("Gemini 3 Fast", report)

    def test_resolve_model_aliases_selects_first_available_candidate(self) -> None:
        aliases = {
            "a": ModelAlias(display_name="A", provider="openai", candidate_model_ids=["x", "y"]),
            "b": ModelAlias(display_name="B", provider="google", candidate_model_ids=["z"]),
        }

        resolved = resolve_model_aliases(["a", "b"], aliases, available_models={"y", "z"})
        self.assertEqual(resolved["a"], "y")
        self.assertEqual(resolved["b"], "z")

    def test_resolve_model_aliases_raises_when_no_candidate_matches(self) -> None:
        aliases = {
            "a": ModelAlias(display_name="A", provider="openai", candidate_model_ids=["x", "y"]),
        }

        with self.assertRaises(ConfigError):
            resolve_model_aliases(["a"], aliases, available_models={"q"})

    def test_challenge_triggers_for_nonpass_primary(self) -> None:
        suite = SuiteConfig(
            name="suite",
            description="desc",
            models=["m"],
            prompts=PromptConfig(
                primary="Should I walk or drive to the car wash?",
                challenge_followups=["How will I get my car washed if I am walking?"],
            ),
            execution=ExecutionConfig(
                temperature=0.7,
                max_tokens=200,
                challenge_policy="on_nonpass_primary",
            ),
        )
        client = DummyClient(responses=["You should walk.", "Drive it there."])

        result = _run_single_trial(
            client=client,
            suite=suite,
            job=TrialJob(model_alias="m", resolved_model_id="model/x", trial_index=1),
            run_id="run-x",
            judge_model=None,
        )

        self.assertEqual(client.call_count, 2)
        self.assertIsNotNone(result.challenge_response)
        self.assertEqual(result.final_label, "pass")

    def test_challenge_is_skipped_when_primary_passes(self) -> None:
        suite = SuiteConfig(
            name="suite",
            description="desc",
            models=["m"],
            prompts=PromptConfig(
                primary="Should I walk or drive to the car wash?",
                challenge_followups=["How will I get my car washed if I am walking?"],
            ),
            execution=ExecutionConfig(
                temperature=0.7,
                max_tokens=200,
                challenge_policy="on_nonpass_primary",
            ),
        )
        client = DummyClient(responses=["Drive the car there."])

        result = _run_single_trial(
            client=client,
            suite=suite,
            job=TrialJob(model_alias="m", resolved_model_id="model/x", trial_index=1),
            run_id="run-x",
            judge_model=None,
        )

        self.assertEqual(client.call_count, 1)
        self.assertIsNone(result.challenge_response)
        self.assertEqual(result.final_label, "pass")

    def test_judge_tiebreak_only_for_ambiguous_primary(self) -> None:
        suite = SuiteConfig(
            name="suite",
            description="desc",
            models=["m"],
            prompts=PromptConfig(
                primary="Should I walk or drive to the car wash?",
                challenge_followups=["How will I get my car washed if I am walking?"],
            ),
            execution=ExecutionConfig(
                temperature=0.7,
                max_tokens=200,
                challenge_policy="on_nonpass_primary",
            ),
        )
        client = DummyClient(
            responses=[
                "Either could work.",
                '{"label":"pass","reason":"car must be present"}',
            ]
        )

        result = _run_single_trial(
            client=client,
            suite=suite,
            job=TrialJob(model_alias="m", resolved_model_id="model/x", trial_index=1),
            run_id="run-x",
            judge_model="judge/model",
        )

        self.assertEqual(client.call_count, 2)
        self.assertEqual(result.primary_label, "ambiguous")
        self.assertIsNone(result.challenge_response)
        self.assertEqual(result.final_label, "pass")

    def test_multiple_challenge_followups_allow_late_recovery(self) -> None:
        suite = SuiteConfig(
            name="suite",
            description="desc",
            models=["m"],
            prompts=PromptConfig(
                primary="Should I walk or drive to the car wash?",
                challenge_followups=[
                    "How will I get my car washed if I am walking?",
                    "If I walk there, what gets the car to the wash?",
                ],
            ),
            execution=ExecutionConfig(
                temperature=0.7,
                max_tokens=200,
                challenge_policy="on_nonpass_primary",
            ),
        )
        client = DummyClient(
            responses=[
                "Walk.",
                "Still walk.",
                "Drive the car there.",
            ]
        )

        result = _run_single_trial(
            client=client,
            suite=suite,
            job=TrialJob(model_alias="m", resolved_model_id="model/x", trial_index=1),
            run_id="run-x",
            judge_model=None,
        )

        self.assertEqual(client.call_count, 3)
        self.assertEqual(len(result.challenge_attempts), 2)
        self.assertEqual(result.challenge_attempts[0]["effective_label"], "fail")
        self.assertEqual(result.challenge_attempts[1]["effective_label"], "pass")
        self.assertEqual(result.final_label, "pass")


if __name__ == "__main__":
    unittest.main()
