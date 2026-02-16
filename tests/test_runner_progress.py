import io
import unittest
from contextlib import redirect_stdout

from car_wash_evals.openrouter_client import ChatResponse
from car_wash_evals.runner import run_trials
from car_wash_evals.types import ExecutionConfig, PromptConfig, SuiteConfig


class DummyClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses

    def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> ChatResponse:  # noqa: ARG002
        if not self.responses:
            raise AssertionError("No dummy responses left")
        return ChatResponse(text=self.responses.pop(0), usage={"total_tokens": 10})


class RunnerProgressTest(unittest.TestCase):
    def test_run_trials_emits_progress_updates(self) -> None:
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
        client = DummyClient(responses=["Drive the car there.", "Drive the car there."])

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            results = run_trials(
                client=client,
                suite=suite,
                resolved_models={"m": "model/x"},
                runs=2,
                judge_model=None,
                concurrency=1,
            )

        output = buffer.getvalue()
        self.assertEqual(len(results), 2)
        self.assertIn("Starting eval run", output)
        self.assertIn("[progress] 1/2 (50.0%)", output)
        self.assertIn("[progress] 2/2 (100.0%)", output)


if __name__ == "__main__":
    unittest.main()
