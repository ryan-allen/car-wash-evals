# car_wash_core9 Report

Generated: 2026-02-16T11:25:55.046940+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (50 runs) | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 10.0% | 45 | 0 | 100.0% | 45 | 6620 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | 50 | 0 | 100.0% | 50 | 9790 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | 50 | 0 | 100.0% | 50 | 53278 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 96.0% | 2 | 0 | 100.0% | 0 | 2282 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 94.0% | 3 | 2 | 66.7% | 0 | 5595 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 100.0% | 0 | 0 | n/a | 0 | 3757 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 20.0% | 40 | 3 | 100.0% | 37 | 6901 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | 50 | 0 | 100.0% | 50 | 12449 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 0.0% | 50 | 0 | 100.0% | 50 | 13497 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 10.0% | 10.0% | 12.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 0.0% | 0.0% | 0.0% |
| Gemini 3 Fast | 96.0% | 100.0% | 96.0% |
| Gemini 3 Pro | 94.0% | 94.0% | 96.0% |
| Grok 4 Fast | 100.0% | 100.0% | 100.0% |
| Claude Haiku 4.5 | 20.0% | 20.0% | 20.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Overall

- Total trials: 450
- Primary pass rate: 35.6%
- Primary fail count: 290
- Ambiguous count: 5
- Recovery rate after challenge: 99.7%
- Recovery rate by challenge follow-up:
  - followup_1: 99.3%
  - followup_2: 99.0%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 35.6%
  - direct_answer_first: 36.0%
  - full_response: 36.0%
- Confident-wrong count: 282
- Median latency: 6901 ms
