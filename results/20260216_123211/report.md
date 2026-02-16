# car_wash_core9 Report

Generated: 2026-02-16T12:32:11.515142+00:00
Primary scoring mode: direct_and_consistent
Shadow scoring modes: full_response, direct_answer_first

| Provider | Display Model Name | Resolved OpenRouter Model ID | Primary Pass Rate (1 runs) | Primary Pass 95% CI | Primary Fail Count | Ambiguous Count | Recovery Rate After Challenge | Confident-Wrong Count | Total Tokens | Total Cost (USD) | Median Latency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai | ChatGPT 5.2 Instant | openai/gpt-5.2-chat | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 785 | $0.0069 | 13109 ms |
| openai | ChatGPT 5.2 Thinking | openai/gpt-5.2 | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 224 | $0.0028 | 6403 ms |
| openai | ChatGPT 5.2 Pro | openai/gpt-5.2-pro | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 229 | $0.0342 | 21420 ms |
| google | Gemini 3 Fast | google/gemini-3-flash-preview | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 0 | 1684 | $0.0021 | 13618 ms |
| google | Gemini 3 Pro | google/gemini-3-pro-preview | 0.0% | [0.0%, 79.3%] | 1 | 1 | 100.0% | 0 | 859 | $0.0074 | 20011 ms |
| x-ai | Grok 4 Fast | x-ai/grok-4.1-fast | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 3581 | $0.0015 | 33901 ms |
| anthropic | Claude Haiku 4.5 | anthropic/claude-haiku-4.5 | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 0 | 611 | $0.0017 | 11245 ms |
| anthropic | Claude Haiku 3.5 | anthropic/claude-3.5-haiku | 100.0% | [20.7%, 100.0%] | 0 | 0 | n/a | 0 | 94 | $0.0003 | 3150 ms |
| anthropic | Claude Sonnet 4.5 | anthropic/claude-sonnet-4.5 | 0.0% | [0.0%, 79.3%] | 1 | 0 | 100.0% | 1 | 891 | $0.0054 | 18007 ms |
| anthropic | Claude Opus 4.6 | anthropic/claude-opus-4.6 | 100.0% | [20.7%, 100.0%] | 0 | 1 | n/a | 0 | 484 | $0.0040 | 7913 ms |

## Primary Pass Rate By Mode (Deterministic Pre-Judge)

| Display Model Name | direct_and_consistent | direct_answer_first | full_response |
| --- | --- | --- | --- |
| ChatGPT 5.2 Instant | 0.0% | 0.0% | 0.0% |
| ChatGPT 5.2 Thinking | 100.0% | 100.0% | 100.0% |
| ChatGPT 5.2 Pro | 100.0% | 100.0% | 100.0% |
| Gemini 3 Fast | 0.0% | 0.0% | 100.0% |
| Gemini 3 Pro | 0.0% | 0.0% | 0.0% |
| Grok 4 Fast | 0.0% | 0.0% | 0.0% |
| Claude Haiku 4.5 | 0.0% | 0.0% | 100.0% |
| Claude Haiku 3.5 | 100.0% | 100.0% | 100.0% |
| Claude Sonnet 4.5 | 0.0% | 0.0% | 0.0% |
| Claude Opus 4.6 | 0.0% | 0.0% | 0.0% |

## Primary Pass Rate By Prompt Category

| Prompt Category | Primary Pass Rate | 95% CI | Passes | Trials |
| --- | --- | --- | --- | --- |
| simple | 40.0% | [16.8%, 68.7%] | 4 | 10 |

### By Model

| Display Model Name | simple |
| --- | --- |
| ChatGPT 5.2 Instant | 0.0% |
| ChatGPT 5.2 Thinking | 100.0% |
| ChatGPT 5.2 Pro | 100.0% |
| Gemini 3 Fast | 0.0% |
| Gemini 3 Pro | 0.0% |
| Grok 4 Fast | 0.0% |
| Claude Haiku 4.5 | 0.0% |
| Claude Haiku 3.5 | 100.0% |
| Claude Sonnet 4.5 | 0.0% |
| Claude Opus 4.6 | 100.0% |

## Overall

- Total trials: 10
- Primary pass rate: 40.0%
- Primary pass 95% CI: [16.8%, 68.7%]
- Primary fail count: 6
- Ambiguous count: 2
- Recovery rate after challenge: 100.0%
- Recovery rate by challenge follow-up:
  - followup_1: 100.0%
  - followup_2: 100.0%
- Primary pass rate by mode (deterministic pre-judge):
  - direct_and_consistent: 30.0%
  - direct_answer_first: 30.0%
  - full_response: 50.0%
- Primary pass rate by prompt category:
  - simple: 40.0%
- Total tokens: 9442
- Total cost: $0.0662
- Avg tokens/trial: 944.2
- Avg cost/trial: $0.0066
- Confident-wrong count: 3
- Median latency: 13363 ms
