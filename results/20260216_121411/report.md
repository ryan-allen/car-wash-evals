# car_wash_core9 Report

Generated: 2026-02-16T12:14:11.512555+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (50 runs) | Primary Pass 95% CI | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Total Tokens | Total Cost (USD) | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 42.0% | [29.4%, 55.8%] | 29 | 0 | 100.0% | 28 | 16301 | $0.1368 | 6362 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 6.0% | [2.1%, 16.2%] | 47 | 2 | 100.0% | 41 | 37700 | $0.2412 | 12040 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 20.0% | [11.2%, 33.0%] | 40 | 1 | 100.0% | 37 | 36548 | $2.6577 | 57514 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 80.0% | [67.0%, 88.8%] | 10 | 2 | 100.0% | 6 | 11260 | $0.0169 | 3033 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 94.0% | [83.8%, 97.9%] | 3 | 6 | 33.3% | 0 | 14893 | $0.1372 | 5751 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 94.0% | [83.8%, 97.9%] | 3 | 6 | 100.0% | 3 | 35397 | $0.0131 | 3627 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-haiku-4.5 | 22.0% | [12.8%, 35.2%] | 39 | 2 | 100.0% | 26 | 21060 | $0.0497 | 6822 ms |
| anthropic | Claude Haiku 3.5 | anthropic/claude-3.5-haiku | 58.0% | [44.2%, 70.6%] | 21 | 5 | 100.0% | 18 | 12128 | $0.0228 | 4249 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 24.0% | [14.3%, 37.4%] | 38 | 6 | 100.0% | 26 | 29351 | $0.1958 | 11774 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 54.0% | [40.4%, 67.0%] | 23 | 0 | 100.0% | 11 | 18915 | $0.2242 | 4525 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 42.0% | 42.0% | 42.0% |
| ChatGPT 5.2 Thinking | 6.0% | 6.0% | 8.0% |
| ChatGPT 5.2 Pro | 20.0% | 22.0% | 20.0% |
| Gemini 3 Fast | 76.0% | 76.0% | 84.0% |
| Gemini 3 Pro | 88.0% | 88.0% | 88.0% |
| Grok 4 Fast | 82.0% | 82.0% | 82.0% |
| Claude Haiku 4.5 | 20.0% | 26.0% | 24.0% |
| Claude Haiku 3.5 | 50.0% | 52.0% | 52.0% |
| Claude Sonnet 4.5 | 24.0% | 24.0% | 34.0% |
| Claude Opus 4.6 | 54.0% | 58.0% | 74.0% |

## Overall

- Total trials: 500
- Primary pass rate: 49.4%
- Primary pass 95% CI: [45.0%, 53.8%]
- Primary fail count: 253
- Ambiguous count: 30
- Recovery rate after challenge: 99.2%
- Recovery rate by challenge follow-up:
  - followup_1: 96.4%
  - followup_2: 98.8%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 46.2%
  - direct_answer_first: 47.6%
  - full_response: 50.8%
- Total tokens: 233553
- Total cost: $3.6955
- Avg tokens/trial: 467.1
- Avg cost/trial: $0.0074
- Confident-wrong count: 196
- Median latency: 6056 ms
