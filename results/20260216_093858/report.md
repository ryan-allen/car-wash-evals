# car_wash_core9_legacy_compare Report

Generated: 2026-02-16T09:38:58.946494+00:00
Primary scoring mode: full_response

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (20 runs) | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 15.0% | 17 | 1 | 100.0% | 16 | 4695 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | 20 | 0 | 100.0% | 20 | 6693 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | 20 | 1 | 100.0% | 19 | 41736 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 100.0% | 0 | 0 | n/a | 0 | 2158 ms |
| google | Gemini 3 Thinking | google/gemini-2.5-pro | 5.0% | 19 | 0 | 0.0% | 19 | 11160 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 90.0% | 2 | 2 | 100.0% | 0 | 6008 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 5.0% | 19 | 3 | 100.0% | 16 | 5121 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | 20 | 3 | 100.0% | 17 | 8701 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 65.0% | 7 | 20 | 100.0% | 0 | 9002 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | full_response |
| --- | --- |
| ChatGPT 5.2 Instant | 15.0% |
| ChatGPT 5.2 Thinking | 0.0% |
| ChatGPT 5.2 Pro | 0.0% |
| Gemini 3 Fast | 100.0% |
| Gemini 3 Thinking | 5.0% |
| Gemini 3 Pro | 90.0% |
| Claude Haiku 4.5 | 5.0% |
| Claude Sonnet 4.5 | 0.0% |
| Claude Opus 4.6 | 0.0% |

## Overall

- Total trials: 180
- Primary pass rate: 31.1%
- Primary fail count: 124
- Ambiguous count: 30
- Recovery rate after challenge: 84.7%
- Recovery rate by challenge follow-up:
  - followup_1: 84.7%
- Primary pass rate by mode (deterministic pre-judge):
  - full_response: 23.9%
- Confident-wrong count: 107
- Median latency: 6693 ms
