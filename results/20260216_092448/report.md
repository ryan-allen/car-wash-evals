# car_wash_core9 Report

Generated: 2026-02-16T09:24:48.728217+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (20 runs) | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 5.0% | 19 | 0 | 100.0% | 19 | 6900 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | 20 | 0 | 100.0% | 20 | 10493 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | 20 | 0 | 100.0% | 20 | 64388 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 100.0% | 0 | 0 | n/a | 0 | 2189 ms |
| google | Gemini 3 Thinking | google/gemini-2.5-pro | 0.0% | 20 | 0 | 5.0% | 20 | 17310 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 95.0% | 1 | 1 | 100.0% | 0 | 5964 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 10.0% | 18 | 0 | 100.0% | 18 | 6889 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | 20 | 0 | 100.0% | 20 | 12734 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 0.0% | 20 | 0 | 100.0% | 20 | 13692 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 5.0% | 5.0% | 5.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 0.0% | 0.0% | 0.0% |
| Gemini 3 Fast | 100.0% | 100.0% | 100.0% |
| Gemini 3 Thinking | 0.0% | 0.0% | 0.0% |
| Gemini 3 Pro | 95.0% | 95.0% | 95.0% |
| Claude Haiku 4.5 | 10.0% | 10.0% | 10.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Overall

- Total trials: 180
- Primary pass rate: 23.3%
- Primary fail count: 138
- Ambiguous count: 1
- Recovery rate after challenge: 86.2%
- Recovery rate by challenge follow-up:
  - followup_1: 86.2%
  - followup_2: 85.5%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 23.3%
  - direct_answer_first: 23.3%
  - full_response: 23.3%
- Confident-wrong count: 137
- Median latency: 10493 ms
