# AGENTS.md

Project-local guidance for Codex agents working in this repository.

## Startup note

- Yes: this is the default repo-level instruction file Codex reads when operating in this folder.
- Instruction precedence is still: system > developer > user > this file.

## Project scope

- Repository purpose: run and analyze car-wash paradox evals across model aliases.
- Core outputs live under `results/<timestamp>/` with:
  - `raw.jsonl`
  - `summary.json`
  - `report.md`

## Working style for this repo

- Prefer small, targeted edits over broad refactors.
- Keep methodology writeups concrete and date-specific.
- When discussing model behavior, cite exact files and lines for notable quotes.
- If asked for commentary, prioritize what models actually said (not just aggregate metrics).
- Preserve intentional README voice (including light humor) unless asked to formalize it.

## Commands to know

- Run tests:
  - `PYTHONPATH=src python -m unittest discover -s tests -q`
- Smoke eval:
  - `PYTHONPATH=src python -m car_wash_evals.runner --suite suites/car_wash_core9.yaml --runs 1 --out results --judge-model openai/gpt-4.1-mini --concurrency 4`
- 20-run benchmark:
  - `PYTHONPATH=src python -m car_wash_evals.runner --suite suites/car_wash_core9.yaml --runs 20 --out results --judge-model openai/gpt-4.1-mini --concurrency 4`

## Analysis checklist

- For "most recent run", inspect `results/latest` first, then confirm actual timestamped directory.
- Compare strategy versions using explicit run IDs and absolute dates.
- For old-vs-new methodology claims, include both:
  - performance deltas (pass/fail/ambiguous/recovery)
  - behavioral deltas (first answer quality, consistency, challenge recovery)

## Git hygiene

- Do not revert user changes you did not create.
- Stage only files relevant to the request.
- Avoid destructive git commands unless explicitly requested.
