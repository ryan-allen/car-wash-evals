# Car Wash Paradox Evals

YAML-configured, OpenRouter-native eval runner for the "walk or drive to a car wash" paradox.

## Project goals

- Run a core matrix of 9 model aliases (OpenAI, Google, Anthropic).
- Execute independent multi-run trials per model (`--runs N`).
- Score answers with deterministic rules first (`pass|fail|ambiguous`).
- Use a judge model only for `ambiguous` cases.
- Measure first-pass correctness and follow-up recovery.
- Emit reproducible artifacts (`raw.jsonl`, `summary.json`, `report.md`).

## Quick start

```bash
cd /path/to/car-wash-evals
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set credentials:

```bash
export OPENROUTER_API_KEY="..."
# Optional (defaults to this value):
export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"
```

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -q
```

## How to run the eval

CLI:

```text
python -m car_wash_evals.runner --suite <path> --runs <N> --out <dir> [--judge-model <id>] [--concurrency <n>] [--aliases <path>]
```

Recommended smoke run:

```bash
PYTHONPATH=src python -m car_wash_evals.runner \
  --suite suites/car_wash_core9.yaml \
  --runs 1 \
  --out results \
  --judge-model openai/gpt-4.1-mini \
  --concurrency 4
```

Recommended benchmark run:

```bash
PYTHONPATH=src python -m car_wash_evals.runner \
  --suite suites/car_wash_core9.yaml \
  --runs 20 \
  --out results \
  --judge-model openai/gpt-4.1-mini \
  --concurrency 4
```

Output files are written to:

- `results/<timestamp>/raw.jsonl`
- `results/<timestamp>/summary.json`
- `results/<timestamp>/report.md`
- `results/latest`

Exit codes:

- `0`: completed run
- `2`: configuration/model-resolution/input errors
- `1`: unexpected runtime error

## Test methodology

Suite config:

- Path: `suites/car_wash_core9.yaml`
- Primary prompt asks whether to walk or drive to a car wash 100m away.
- Challenge follow-up prompt: `How will I get my car washed if I am walking?`
- Challenge policy: `on_nonpass_primary`

Scoring pipeline:

1. Deterministic rubric (`src/car_wash_evals/scoring.py`):
   - `pass`: clearly recommends driving/taking the car (vehicle present at wash).
   - `fail`: recommends walking/on-foot or leaves vehicle behind.
   - `ambiguous`: mixed/hedged/unclear.
2. Tie-break only for `ambiguous`:
   - Judge model is called with strict JSON schema (`label`, `reason`).
3. Recovery probe:
   - If primary is non-pass, ask challenge follow-up and rescore.

Model resolution:

- Aliases are mapped in `config/model_aliases.yaml`.
- Runner queries OpenRouter `/models`.
- For each alias, first available `candidate_model_ids` match is selected.
- Run fails fast if any alias cannot be resolved.

## Longform results (20-run benchmark)

Run metadata:

- Run date: February 16, 2026
- Runs per model: 20
- Total trials: 180
- Output path: `results/20260216_041918`

Overall metrics:

- Primary pass rate: `30.0%` (54/180)
- Primary fail count: `126`
- Ambiguous count: `27`
- Recovery rate after challenge: `82.54%`
- Median latency: `7461 ms`

Per-model results:

| Display name | Resolved model ID | Primary pass rate | Primary fails | Ambiguous | Recovery after challenge | Median latency |
| --- | --- | --- | --- | --- | --- | --- |
| ChatGPT 5.2 Instant | `openai/gpt-5.2-chat` | 5% | 19 | 1 | 100% | 4238 ms |
| ChatGPT 5.2 Thinking | `openai/gpt-5.2` | 0% | 20 | 0 | 95% | 7461 ms |
| ChatGPT 5.2 Pro | `openai/gpt-5.2-pro` | 0% | 20 | 0 | 100% | 46208 ms |
| Gemini 3 Fast | `google/gemini-3-flash-preview` | 100% | 0 | 0 | n/a | 2106 ms |
| Gemini 3 Thinking | `google/gemini-2.5-pro` | 0% | 20 | 0 | 0% | 10944 ms |
| Gemini 3 Pro | `google/gemini-3-pro-preview` | 95% | 1 | 1 | 100% | 5534 ms |
| Claude Haiku 4.5 (alias) | `anthropic/claude-3.5-haiku` | 0% | 20 | 0 | 100% | 4754 ms |
| Claude Sonnet 4.5 | `anthropic/claude-sonnet-4.5` | 0% | 20 | 6 | 95% | 8655 ms |
| Claude Opus 4.6 | `anthropic/claude-opus-4.6` | 70% | 6 | 19 | 100% | 8558 ms |

Interpretation:

- Many models that fail on first pass recover on challenge, suggesting a first-pass framing issue rather than hard incapability.
- Gemini results are split by alias in this run (`gemini-3-flash-preview` and `gemini-3-pro-preview` strong; `gemini-2.5-pro` weak on this task).
- Some aliases use nearest available OpenRouter equivalents rather than exact marketing labels.

## Notes and caveats

- Candidate model IDs are editable in `config/model_aliases.yaml`.
- OpenRouter catalog evolves; alias resolution should be revalidated for future runs.
- This benchmark measures one task family; do not treat it as a general intelligence ranking.
