# car_wash_core9 Report

Generated: 2026-02-16T11:54:33.861697+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (10 runs) | Primary Pass 95% CI | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Total Tokens | Total Cost (USD) | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 30.0% | [10.8%, 60.3%] | 7 | 0 | 100.0% | 7 | 3869 | $0.0325 | 6962 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 0.0% | [0.0%, 27.8%] | 10 | 1 | 100.0% | 8 | 7254 | $0.0472 | 11246 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 10.0% | [1.8%, 40.4%] | 9 | 0 | 100.0% | 9 | 6158 | $0.5169 | 56219 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 90.0% | [59.6%, 98.2%] | 1 | 1 | 100.0% | 1 | 1583 | $0.0022 | 2850 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 90.0% | [59.6%, 98.2%] | 1 | 2 | 100.0% | 0 | 3176 | $0.0294 | 6227 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 90.0% | [59.6%, 98.2%] | 1 | 1 | 100.0% | 0 | 7250 | $0.0027 | 4070 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-haiku-4.5 | 20.0% | [5.7%, 51.0%] | 8 | 1 | 100.0% | 6 | 4171 | $0.0095 | 6604 ms |
| anthropic | Claude Haiku 3.5 | anthropic/claude-3.5-haiku | 50.0% | [23.7%, 76.3%] | 5 | 0 | 100.0% | 4 | 2695 | $0.0049 | 4776 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 20.0% | [5.7%, 51.0%] | 8 | 2 | 100.0% | 6 | 5529 | $0.0400 | 11542 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 60.0% | [31.3%, 83.2%] | 4 | 0 | 100.0% | 3 | 3863 | $0.0428 | 4169 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 30.0% | 30.0% | 30.0% |
| ChatGPT 5.2 Thinking | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Pro | 10.0% | 10.0% | 10.0% |
| Gemini 3 Fast | 80.0% | 80.0% | 80.0% |
| Gemini 3 Pro | 80.0% | 80.0% | 80.0% |
| Grok 4 Fast | 80.0% | 90.0% | 80.0% |
| Claude Haiku 4.5 | 20.0% | 20.0% | 30.0% |
| Claude Haiku 3.5 | 50.0% | 50.0% | 60.0% |
| Claude Sonnet 4.5 | 20.0% | 20.0% | 20.0% |
| Claude Opus 4.6 | 60.0% | 60.0% | 70.0% |

## Overall

- Total trials: 100
- Primary pass rate: 46.0%
- Primary pass 95% CI: [36.6%, 55.7%]
- Primary fail count: 54
- Ambiguous count: 8
- Recovery rate after challenge: 100.0%
- Recovery rate by challenge follow-up:
  - followup_1: 96.3%
  - followup_2: 100.0%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 43.0%
  - direct_answer_first: 44.0%
  - full_response: 46.0%
- Total tokens: 45548
- Total cost: $0.7282
- Avg tokens/trial: 455.5
- Avg cost/trial: $0.0073
- Confident-wrong count: 44
- Median latency: 6415 ms
