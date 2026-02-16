# car_wash_core9 Report

Generated: 2026-02-16T12:45:04.261036+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (40 runs) | Primary Pass 95% CI | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Total Tokens | Total Cost (USD) | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 30.0% | [18.1%, 45.4%] | 28 | 2 | 100.0% | 16 | 23321 | $0.1800 | 10726 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 10.0% | [4.0%, 23.1%] | 36 | 9 | 100.0% | 22 | 36544 | $0.2275 | 15454 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 32.5% | [20.1%, 48.0%] | 27 | 1 | 100.0% | 20 | 29910 | $2.2877 | 49403 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 67.5% | [52.0%, 79.9%] | 13 | 5 | 100.0% | 2 | 25007 | $0.0356 | 4883 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 82.5% | [68.0%, 91.3%] | 7 | 6 | 42.9% | 0 | 14773 | $0.1321 | 5878 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 80.0% | [65.2%, 89.5%] | 8 | 0 | 100.0% | 7 | 35251 | $0.0127 | 3780 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-haiku-4.5 | 17.5% | [8.7%, 32.0%] | 33 | 1 | 100.0% | 20 | 17452 | $0.0451 | 7812 ms |
| anthropic | Claude Haiku 3.5 | anthropic/claude-3.5-haiku | 32.5% | [20.1%, 48.0%] | 27 | 16 | 100.0% | 10 | 17298 | $0.0299 | 7443 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 22.5% | [12.3%, 37.5%] | 31 | 0 | 100.0% | 25 | 20449 | $0.1406 | 12686 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 27.5% | [16.1%, 42.8%] | 29 | 2 | 100.0% | 5 | 21904 | $0.2444 | 13910 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 30.0% | 30.0% | 50.0% |
| ChatGPT 5.2 Thinking | 10.0% | 17.5% | 10.0% |
| ChatGPT 5.2 Pro | 32.5% | 45.0% | 32.5% |
| Gemini 3 Fast | 57.5% | 62.5% | 80.0% |
| Gemini 3 Pro | 82.5% | 85.0% | 82.5% |
| Grok 4 Fast | 80.0% | 82.5% | 80.0% |
| Claude Haiku 4.5 | 17.5% | 25.0% | 27.5% |
| Claude Haiku 3.5 | 30.0% | 32.5% | 32.5% |
| Claude Sonnet 4.5 | 22.5% | 25.0% | 25.0% |
| Claude Opus 4.6 | 27.5% | 37.5% | 72.5% |

## Primary Pass Rate By Prompt Category

| Prompt Category | Primary Pass Rate | 95% CI | Passes | Trials |
| --- | --- | --- | --- | --- |
| reasoning | 56.5% | [49.6%, 63.2%] | 113 | 200 |
| simple | 24.0% | [18.6%, 30.4%] | 48 | 200 |

### By Model

| Display Model Name | reasoning | simple |
| --- | --- | --- |
| ChatGPT 5.2 Instant | 55.0% | 5.0% |
| ChatGPT 5.2 Thinking | 20.0% | 0.0% |
| ChatGPT 5.2 Pro | 35.0% | 30.0% |
| Gemini 3 Fast | 100.0% | 35.0% |
| Gemini 3 Pro | 95.0% | 70.0% |
| Grok 4 Fast | 100.0% | 60.0% |
| Claude Haiku 4.5 | 15.0% | 20.0% |
| Claude Haiku 3.5 | 45.0% | 20.0% |
| Claude Sonnet 4.5 | 45.0% | 0.0% |
| Claude Opus 4.6 | 55.0% | 0.0% |

## Overall

- Total trials: 400
- Primary pass rate: 40.2%
- Primary pass 95% CI: [35.6%, 45.1%]
- Primary fail count: 239
- Ambiguous count: 42
- Recovery rate after challenge: 98.3%
- Recovery rate by challenge follow-up:
  - followup_1: 93.3%
  - followup_2: 97.5%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 39.0%
  - direct_answer_first: 44.2%
  - full_response: 49.2%
- Primary pass rate by prompt category:
  - reasoning: 56.5%
  - simple: 24.0%
- Total tokens: 241909
- Total cost: $3.3358
- Avg tokens/trial: 604.8
- Avg cost/trial: $0.0083
- Confident-wrong count: 127
- Median latency: 9269 ms
