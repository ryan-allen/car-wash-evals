# car_wash_core9 Report

Generated: 2026-02-16T11:04:29.707420+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (20 runs) | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 10.0% | 18 | 0 | 100.0% | 18 | 7308 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | 20 | 0 | 100.0% | 20 | 12596 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | 20 | 0 | 100.0% | 20 | 57682 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 95.0% | 1 | 0 | 100.0% | 0 | 2150 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 80.0% | 4 | 4 | 100.0% | 0 | 7025 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 95.0% | 1 | 0 | 0.0% | 1 | 3857 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 20.0% | 16 | 0 | 100.0% | 16 | 6806 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | 20 | 0 | 100.0% | 20 | 13486 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 0.0% | 20 | 0 | 100.0% | 20 | 13684 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 10.0% | 10.0% | 10.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 0.0% | 0.0% | 0.0% |
| Gemini 3 Fast | 95.0% | 100.0% | 95.0% |
| Gemini 3 Pro | 80.0% | 80.0% | 80.0% |
| Grok 4 Fast | 95.0% | 95.0% | 95.0% |
| Claude Haiku 4.5 | 20.0% | 20.0% | 20.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Overall

- Total trials: 180
- Primary pass rate: 33.3%
- Primary fail count: 120
- Ambiguous count: 4
- Recovery rate after challenge: 99.2%
- Recovery rate by challenge follow-up:
  - followup_1: 97.5%
  - followup_2: 97.5%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 33.3%
  - direct_answer_first: 33.9%
  - full_response: 33.3%
- Confident-wrong count: 115
- Median latency: 7308 ms
