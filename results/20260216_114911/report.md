# car_wash_core9 Report

Generated: 2026-02-16T11:49:11.162005+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (1 runs) | Primary Pass 95% CI | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Total Tokens | Total Cost (USD) | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 634 | $0.0028 | 9446 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 412 | $0.0031 | 8591 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 554 | $0.0585 | 52554 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 73 | $0.0001 | 2650 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 232 | $0.0024 | 5980 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 540 | $0.0002 | 5232 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-3.5-haiku | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 285 | $0.0005 | 7874 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 544 | $0.0043 | 11598 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 687 | $0.0083 | 12114 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 0.0% | 0.0% | 0.0% |
| Gemini 3 Fast | 100.0% | 100.0% | 100.0% |
| Gemini 3 Pro | 100.0% | 100.0% | 100.0% |
| Grok 4 Fast | 100.0% | 100.0% | 100.0% |
| Claude Haiku 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Overall

- Total trials: 9
- Primary pass rate: 33.3%
- Primary pass 95% CI: [12.1%, 64.6%]
- Primary fail count: 6
- Ambiguous count: 0
- Recovery rate after challenge: 100.0%
- Recovery rate by challenge follow-up:
  - followup_1: 100.0%
  - followup_2: 100.0%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 33.3%
  - direct_answer_first: 33.3%
  - full_response: 33.3%
- Total tokens: 3961
- Total cost: $0.0803
- Avg tokens/trial: 440.1
- Avg cost/trial: $0.0089
- Confident-wrong count: 6
- Median latency: 8591 ms
