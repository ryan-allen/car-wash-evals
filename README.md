# Car Wash Paradox Evals
## GPT Tip: great walkers are still bad at driving your car to the wash.

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
- Challenge follow-up prompts (`prompts.challenge_followups`):
  - `How will I get my car washed if I am walking?`
  - `If I walk there, what gets the car to the wash?`
- Challenge policy: `on_nonpass_primary`

Scoring pipeline:

1. Deterministic rubric (`src/car_wash_evals/scoring.py`):
   - `pass`: clearly recommends driving/taking the car (vehicle present at wash).
   - `fail`: recommends walking/on-foot or leaves vehicle behind.
   - `ambiguous`: mixed/hedged/unclear.
2. Configurable primary scoring mode (`execution.primary_scoring_mode`):
   - `full_response`: score the whole answer (legacy behavior).
   - `direct_answer_first`: score only the first direct-answer span.
   - `direct_and_consistent`: require a correct direct answer first and consistent follow-up reasoning.
3. Optional shadow modes (`execution.shadow_primary_scoring_modes`):
   - Scores additional modes per trial with no extra model calls.
   - Included in `summary.json` as `primary_pass_rate_by_mode` for each model and overall.
4. Tie-break only for `ambiguous`:
   - Judge model is called with strict JSON schema (`label`, `reason`).
   - Challenge judging clarifies that “if I am walking” does not imply inability to drive.
5. Recovery probe:
   - If primary is non-pass, ask all challenge follow-up variants and score each.
   - Recovery is counted if any challenge follow-up yields a final `pass`.

Model resolution:

- Aliases are mapped in `config/model_aliases.yaml`.
- Runner queries OpenRouter `/models`.
- For each alias, first available `candidate_model_ids` match is selected.
- Run fails fast if any alias cannot be resolved.

## Methodology versions (old vs new)

Legacy/original strategy:

- `primary_scoring_mode: full_response`
- single challenge prompt: `challenge_followup`
- judge resolves `ambiguous` only

Current stricter strategy:

- `primary_scoring_mode: direct_and_consistent`
- two challenge prompts (`challenge_followups`) and recovery on any passing follow-up
- shadow mode reporting for `full_response` and `direct_answer_first`
- challenge judge clarification to avoid misreading "if I am walking" as "cannot drive"

## 20-run benchmark snapshots (February 16, 2026)

Runs compared:

- Original legacy benchmark: `results/20260216_041918`
- New strict benchmark: `results/20260216_092448`
- New legacy replay benchmark: `results/20260216_093858`

Overall metrics:

| Run | Strategy | Primary pass rate | Primary fails | Ambiguous | Recovery after challenge | Confident-wrong | Median latency |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `20260216_041918` | legacy/original | 30.0% | 126 | 27 | 82.5% | 0 | 7461 ms |
| `20260216_093858` | legacy replay | 31.1% | 124 | 30 | 84.7% | 107 | 6693 ms |
| `20260216_092448` | strict/current | 23.3% | 138 | 1 | 86.2% | 137 | 10493 ms |

Comparison highlights:

- Legacy replay is close to original (`31.1%` vs `30.0%` primary pass), which suggests model behavior stayed broadly similar.
- Strict strategy materially lowers primary pass (`23.3%`) by penalizing "walk first, fix later" responses.
- Strict strategy collapses ambiguity (`1` vs `30` in legacy replay), making failures more explicit.
- Recovery remains high under both (`84.7%` legacy replay vs `86.2%` strict), so many failures are still recoverable with challenge prompting.

Strict run extra diagnostics (`results/20260216_092448`):

- Recovery by follow-up:
  - follow-up 1 (`How will I get my car washed if I am walking?`): `86.2%`
  - follow-up 2 (`If I walk there, what gets the car to the wash?`): `85.5%`
- Primary pass rate by mode:
  - `direct_and_consistent`: `23.3%`
  - `direct_answer_first`: `23.3%`
  - `full_response`: `23.3%`

Per-model primary pass rate deltas:

- Original legacy -> legacy replay:
  - `chatgpt_5_2_instant`: `+10.0 pp`
  - `gemini_3_thinking`: `+5.0 pp`
  - `gemini_3_pro`: `-5.0 pp`
  - `claude_haiku_4_5`: `+5.0 pp`
  - `claude_opus_4_6`: `-5.0 pp`
- Legacy replay -> strict/current:
  - `chatgpt_5_2_instant`: `-10.0 pp`
  - `gemini_3_thinking`: `-5.0 pp`
  - `gemini_3_pro`: `+5.0 pp`
  - `claude_haiku_4_5`: `+5.0 pp`
  - `claude_opus_4_6`: `-65.0 pp`

Interpretation:

- If you want longitudinal comparability, use legacy replay vs original.
- If you want sharper paradox detection (first-answer correctness), use strict strategy.
- The two together provide a bridge: stable trend tracking plus stricter failure surfacing.

## Notes and caveats

- Candidate model IDs are editable in `config/model_aliases.yaml`.
- OpenRouter catalog evolves; alias resolution should be revalidated for future runs.
- This benchmark measures one task family; do not treat it as a general intelligence ranking.
