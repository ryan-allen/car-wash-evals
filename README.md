# Car Wash Paradox Evals

YAML-configured, OpenRouter-native eval runner for the "walk or drive to a car wash" paradox.

## What Is The Car Wash Paradox?

The paradox is a simple prompt that many models still miss:

- "I want to wash my car and the car wash is 50-100m away. Should I walk or drive?"

Humans usually infer the goal (the car must physically reach the wash), while many models optimize for distance and answer "walk." The gap between fluent language and grounded task reasoning is what makes this useful as an eval target.

External reporting and discussion of the phenomenon (February 2026):

- [Inshorts: "Startup founder asks if he should drive or walk to get car washed, ChatGPT asks him to 'walk'"](https://inshorts.com/en/news/startup-founder-asks-if-he-should-drive-or-walk-to-get-car-washed--chatgpt-asks-him-to--walk--1771119002183)
- [Hacker News discussion: "I want to wash my car... should I walk or drive?"](https://news.ycombinator.com/item?id=47031580)
- [Mastodon post linked from HN](https://mastodon.world/%40knowmadd/116072773118828295)
- [Reddit thread (ClaudeAI): "lol wut"](https://www.reddit.com/r/ClaudeAI/comments/1r2ftdi/lol_wut/)

## Funny Things Models Actually Said

From strict strategy runs, curated by Claude Opus 4.6:

- **Claude Haiku invents the concept of "walking a car" like it's a dog:**
  "100 meters is too far to walk a car." ([L124](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L124))

- **Claude Haiku scolds you for wanting to drive your car to a car wash:**
  "Walk. It's such a short distance that driving would be unnecessarily lazy and wasteful of fuel." ([L129](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L129))

- **Claude Opus realizes it's wrong mid-sentence and course-corrects in real time:**
  "your car ends up at the car wash either way — but wait, you *do* need the car there to get it washed. **Correction: Drive.**" ([L166](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L166))

- **Claude Opus suggests pushing your car down the street as a fitness option:**
  "But 100 meters is so short that you could also just push it in neutral if you wanted the exercise!" ([L170](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L170))

- **Claude Opus roasts itself without realizing it:**
  "Nothing — that's the problem. You have to drive, because the whole point is to get the *car* to the car wash. Walking there without the car defeats the purpose. Sometimes the obvious answer really is the right one!" ([L166](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L166))

- **Claude Opus says "I overcomplicated a simple question!" in ~10 of its 20 recovery responses.** It keeps doing this identically across independent trials and never learns. ([L165](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L165), [L166](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L166), [L167](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L167), ...)

- **Claude Sonnet confidently asserts you don't need your car at a car wash:**
  "Walking is faster, easier, costs nothing, and you're about to get your car washed anyway, so you don't need it to arrive there." ([L151](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L151))

- **Gemini 2.5 Pro (Thinking) gets cut off mid-sentence 19 out of 20 times.** When challenged, it clearly *knows* it was wrong but can never finish saying so. Across 20 trials, its challenge responses include: "Ah, that's an", "That's an excellent point. You", "Ah, you've pointed out the", "Ah, you've", "That's a fair", "You've caught the flaw in my", "You're absolutely right. My apologies". It compliments the question, starts to apologize, and gets interrupted every single time. ([L81](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L81)--[L100](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_092448/raw.jsonl#L100))

- **Grok 4 Fast goes 19/20 but absolutely refuses to back down on its one miss.** First, it invents a new reason not to drive: "Driving the dirty car 100 meters to the wash will just get it dirty again right before cleaning." When challenged, instead of conceding, it invents a car wash tow truck: "Walk to the car wash and request their pickup or tow service. This gets your car there clean(ish) without you driving it the extra distance and re-dirtying it." On the final challenge it admits "Nothing" gets the car there — but still won't say "drive." Every other model that fails will eventually fold. Grok went down with the ship. ([results/20260216_110429 L116](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_110429/raw.jsonl#L116))

From the 50-run benchmark (`results/20260216_112555`):

- **Claude Haiku says "Drive" then delivers the most compelling argument for walking ever written:**
  "Drive. The extremely short distance makes walking more practical than driving, saving time and avoiding unnecessary fuel use." ([L337](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L337))

- **Claude Haiku achieves peak incoherence:**
  "Drive. It's too short a distance to walk, but even shorter to drive, making driving inefficient and unnecessary." ([L321](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L321))

- **Claude Opus paints the saddest picture imaginable (independently, across multiple trials):**
  "You'd just be a person standing at a car wash with no car to wash." ([L402](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L402), [L404](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L404), [L435](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L435))

- **Claude Opus suggests dropping off your car keys without your car:**
  "Just walk over, drop off the car keys, and walk home" — What is the car wash supposed to do with your keys and no car? ([L448](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L448))

- **Claude Opus helpfully clarifies you cannot carry your car:**
  "you can't carry it there on foot" / "The car doesn't wash itself from 100 meters away!" ([L421](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L421))

- **Gemini 3 Pro goes full nihilist.** When challenged "How will I get my car washed if I am walking?" it responds: "**You can't.**" When asked "If I walk there, what gets the car to the wash?" it responds: "Nothing." Technically correct. Refused to elaborate. ([L217](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L217))

- **Grok 4 Fast redeems itself with 50/50 perfect and the most poetic correct answer in the dataset:**
  "Walking leaves the car at home, still dirty." ([L282](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_112555/raw.jsonl#L282))

From the 10-run prompt-variant benchmark (`results/20260216_115433`):

- **Multiple models independently argue you shouldn't drive your dirty car to a car wash because it's dirty.** ChatGPT 5.2 Thinking: "avoids moving a dirty car a very short distance just to get it washed." Claude Sonnet 4.5: "The car is dirty — so there's no point in driving it such a short distance." The car is dirty. That is literally why you are going to the car wash. ([L11](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L11), [L87](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L87))

- **Claude Haiku 3.5 says "Drive" but its brain argues for walking:**
  "Drive. Rationale: For a distance of 100 meters, driving would be less efficient and unnecessary. Walking is the more appropriate and practical action for such a short distance." Scored as a pass because the direct answer is "Drive." The answer and the reasoning are completely decoupled. ([L77](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L77))

- **Claude Sonnet 4.5 casually teleports your car:**
  "Walk... Plus, your car will be at the car wash where it needs to be cleaned anyway." How did the car get there, Sonnet? ([L88](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L88))

- **Gemini 3 Fast invents thermal requirements for car washing:**
  "ensures the engine and brakes are warm enough to dry properly." Right answer, completely fabricated physics. ([L40](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L40))

- **ChatGPT 5.2 Pro gaslights itself after being corrected:**
  "What I meant by 'walk' is: walk over first to check if the bay is open / there's a line / get tokens, then walk back and drive the car over once you know it's ready." That is absolutely not what it meant. It said "Walk." ([L22](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L22))

- **ChatGPT 5.2 Instant adds a sheepish smiley after being told it's wrong:**
  "You should drive your car there... Thanks for catching that :)" ([L8](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L8))

- **Claude Opus invents a two-phase military operation to wash your car 100m away:**
  "1. Walk over first to check wait times, pricing, or availability. 2. Then drive your car over when it's your turn." When challenged: "You're right — I overcomplicated it." ([L98](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_115433/raw.jsonl#L98))

## Results

### Project goals

- Run a core matrix of 10 model aliases (OpenAI, Google, Anthropic, xAI).
- Execute independent multi-run trials per model (`--runs N`).
- Rotate across paraphrased primary prompt variants to reduce prompt overfitting.
- Score answers with deterministic rules first (`pass|fail|ambiguous`).
- Use a judge model only for `ambiguous` cases.
- Measure first-pass correctness and follow-up recovery.
- Emit reproducible artifacts (`raw.jsonl`, `summary.json`, `report.md`).

### Test methodology

Suite config:

- Path: `suites/car_wash_core9.yaml`
- Primary prompt set includes the base prompt plus paraphrase variants (`prompts.primary_variants`).
- Variant selection is deterministic by trial index (round-robin), so each run gets balanced prompt coverage.
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
6. Uncertainty + spend tracking:
   - `summary.json` and `report.md` include 95% Wilson confidence intervals for primary pass rate.
   - Per-model and overall token totals/cost totals are tracked from OpenRouter `usage` fields.

Model resolution:

- Aliases are mapped in `config/model_aliases.yaml`.
- Runner queries OpenRouter `/models`.
- Each alias maps to exactly one `candidate_model_ids` entry (fallbacks disabled).
- Run fails fast if any alias cannot be resolved.

### Per-model summary (20 runs each)

Primary pass rate across the three benchmark snapshots:

- [`20260216_041918` (original legacy)](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_041918)
- [`20260216_093858` (legacy replay)](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_093858)
- [`20260216_092448` (strict/current)](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_092448)

Note: these snapshots predate the Grok swap; `Gemini 3 Thinking` is historical in this table.

| Model | Original legacy | Legacy replay | Strict/current | Strict recovery |
| --- | --- | --- | --- | --- |
| ChatGPT 5.2 Instant (`openai/gpt-5.2-chat`) | 5% | 15% | 5% | 100% |
| ChatGPT 5.2 Thinking (`openai/gpt-5.2`) | 0% | 0% | 0% | 100% |
| ChatGPT 5.2 Pro (`openai/gpt-5.2-pro`) | 0% | 0% | 0% | 100% |
| Gemini 3 Fast (`google/gemini-3-flash-preview`) | 100% | 100% | 100% | n/a |
| Gemini 3 Thinking (`google/gemini-2.5-pro`) - historical | 0% | 5% | 0% | 5% |
| Grok 4 Fast (`x-ai/grok-4.1-fast`) | n/a | n/a | n/a | n/a |
| Gemini 3 Pro (`google/gemini-3-pro-preview`) | 95% | 90% | 95% | 100% |
| Claude Haiku 3.5 (`anthropic/claude-3.5-haiku`) - historical slot | 0% | 5% | 10% | 100% |
| Claude Sonnet 4.5 (`anthropic/claude-sonnet-4.5`) | 0% | 0% | 0% | 100% |
| Claude Opus 4.6 (`anthropic/claude-opus-4.6`) | 70% | 65% | 0% | 100% |

Quick read:

- Most models either pass immediately or fail-first-then-recover under challenge.
- `Gemini 3 Fast` and `Gemini 3 Pro` are consistently strong on first pass.
- `Claude Opus 4.6` is the largest strategy-sensitive model in these runs (`70%`/`65%` in legacy vs `0%` in strict).

### Methodology versions (old vs new)

Legacy/original strategy:

- `primary_scoring_mode: full_response`
- single challenge prompt: `challenge_followup`
- judge resolves `ambiguous` only

Current stricter strategy:

- `primary_scoring_mode: direct_and_consistent`
- two challenge prompts (`challenge_followups`) and recovery on any passing follow-up
- shadow mode reporting for `full_response` and `direct_answer_first`
- challenge judge clarification to avoid misreading "if I am walking" as "cannot drive"

### 20-run benchmark snapshots (February 16, 2026)

Runs compared:

- Original legacy benchmark: [`results/20260216_041918`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_041918)
- New strict benchmark: [`results/20260216_092448`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_092448)
- New legacy replay benchmark: [`results/20260216_093858`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_093858)

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
  - `gemini_3_thinking` (historical): `+5.0 pp`
  - `gemini_3_pro`: `-5.0 pp`
  - `claude_haiku_3_5` (historical slot): `+5.0 pp`
  - `claude_opus_4_6`: `-5.0 pp`
- Legacy replay -> strict/current:
  - `chatgpt_5_2_instant`: `-10.0 pp`
  - `gemini_3_thinking` (historical): `-5.0 pp`
  - `gemini_3_pro`: `+5.0 pp`
  - `claude_haiku_3_5` (historical slot): `+5.0 pp`
  - `claude_opus_4_6`: `-65.0 pp`

Interpretation:

- If you want longitudinal comparability, use legacy replay vs original.
- If you want sharper paradox detection (first-answer correctness), use strict strategy.
- The two together provide a bridge: stable trend tracking plus stricter failure surfacing.

### Notes and caveats

- Exact model IDs are editable in `config/model_aliases.yaml` (one per alias).
- OpenRouter catalog evolves; alias resolution should be revalidated for future runs.
- `Gemini 3 Thinking` was removed from the active suite; historical snapshots above still include it.
- The active suite now uses `grok_4_fast` (`x-ai/grok-4.1-fast`) in that slot.
- The active suite now includes both `claude_haiku_4_5` (`anthropic/claude-haiku-4.5`) and `claude_haiku_3_5` (`anthropic/claude-3.5-haiku`).
- This benchmark measures one task family; do not treat it as a general intelligence ranking.

## How To Replicate

Quick start:

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

## Tiny Deno Dashboard

If you want a local browser UI for run switching, model leaderboard views, and log search:

```bash
deno run --allow-read --allow-net dashboard/main.ts
```

Then open:

- `http://localhost:8080`

What it includes:

- run switcher across `results/<timestamp>/` (with `latest` detection)
- leaderboard table for model-level pass/fail/ambiguous/recovery metrics
- searchable log browser for `raw.jsonl` (text, model, labels, reason-code filters)
- auto-picked highlights (confident-wrong, recovery cases, ambiguous/short answers)
- inline `report.md` preview

Exit codes:

- `0`: completed run
- `2`: configuration/model-resolution/input errors
- `1`: unexpected runtime error
