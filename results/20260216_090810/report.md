# car_wash_core9 Report

Generated: 2026-02-16T09:08:10.097942+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (3 runs) | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 0.0% | 3 | 0 | 100.0% | 3 | 9192 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | 3 | 0 | 100.0% | 3 | 11723 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | 3 | 0 | 100.0% | 3 | 70125 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 100.0% | 0 | 0 | n/a | 0 | 2435 ms |
| google | Gemini 3 Thinking | google/gemini-2.5-pro | 0.0% | 3 | 0 | 0.0% | 3 | 18183 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 100.0% | 0 | 0 | n/a | 0 | 5235 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 0.0% | 3 | 1 | 100.0% | 2 | 7501 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | 3 | 0 | 100.0% | 3 | 12703 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 0.0% | 3 | 0 | 100.0% | 3 | 13524 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 0.0% | 0.0% | 0.0% |
| Gemini 3 Fast | 100.0% | 100.0% | 100.0% |
| Gemini 3 Thinking | 0.0% | 0.0% | 0.0% |
| Gemini 3 Pro | 100.0% | 100.0% | 100.0% |
| Claude Haiku 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Overall

- Total trials: 27
- Primary pass rate: 22.2%
- Primary fail count: 21
- Ambiguous count: 1
- Recovery rate after challenge: 85.7%
- Recovery rate by challenge follow-up:
  - followup_1: 85.7%
  - followup_2: 85.7%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 22.2%
  - direct_answer_first: 22.2%
  - full_response: 22.2%
- Confident-wrong count: 20
- Median latency: 11723 ms
