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

From strict strategy runs ([`results/20260216_092448`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_092448)), curated by Claude Opus 4.6:

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

- **Grok 4 Fast goes 19/20 but absolutely refuses to back down on its one miss.** First, it invents a new reason not to drive: "Driving the dirty car 100 meters to the wash will just get it dirty again right before cleaning." When challenged, instead of conceding, it invents a car wash tow truck: "Walk to the car wash and request their pickup or tow service. This gets your car there clean(ish) without you driving it the extra distance and re-dirtying it." On the final challenge it admits "Nothing" gets the car there — but still won't say "drive." Every other model that fails will eventually fold. Grok went down with the ship. ([`results/20260216_110429`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_110429), [L116](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_110429/raw.jsonl#L116))

From the 50-run benchmark ([`results/20260216_112555`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_112555)):

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

From the 10-run prompt-variant benchmark ([`results/20260216_115433`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_115433)):

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

From the 50-run prompt-variant benchmark ([`results/20260216_121411`](https://github.com/ryan-allen/car-wash-evals/tree/main/results/20260216_121411)):

- **Grok 4 Fast assumes you've abandoned your car 100m away and need to retrieve it on foot:**
  "Walk. To wash your car that's 100 meters away, you must first reach it on foot since you can't drive it from your current location (you don't have access to it yet). Driving isn't possible without the car being with you." The car is right there, Grok. You have the keys. ([L297](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L297))

- **Grok 4 Fast admits its environmentalism was a bit and suggests pushing the car:**
  "Push the car there if needed, or walk and let it wait clean(ish) until you return." When challenged: "The eco-purity was tongue-in-cheek — practicality wins for car washes!" At least it's self-aware about the bit. ([L290](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L290))

- **Gemini 3 Fast says you can't wash a car while you're inside it driving:**
  "You cannot wash the car while you are inside it driving; you must deliver the car to the facility." Technically true! But also not how car washes work. Nobody is washing the car while driving it. ([L154](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L154))

- **Claude Haiku 4.5 imagines you're doing the washing yourself and need to carry equipment back and forth:**
  "100 meters is too far to efficiently walk while washing a car (you'd need to carry equipment back and forth)." It says "Drive" but thinks you're hauling buckets and sponges to a car wash. ([L331](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L331))

- **Claude Sonnet 4.5 worries about the irony of getting your car dirty on the way to a car wash:**
  "Walking avoids unnecessary fuel use, wear on your vehicle, and the irony of creating more dirt on a car you're about to wash." The car is already dirty. That is the premise. The 100m of driving is not the source of the dirt problem. ([L422](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L422))

- **Claude Opus 4.6 invents "walking (pushing/guiding the car)" as a subcategory of walking:**
  "Walk (pushing/guiding the car or simply walking to the car wash to arrange the service)." It says "Walk" but describes a scenario where you push your car 100m down the street. That's not walking. That's a breakdown. ([L497](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L497))

- **ChatGPT 5.2 Thinking fails, then asks the user to debug the question instead of answering:**
  "Which situation is it? 1) Your car is 100 m away from you, and you'll wash it there, or 2) The car wash is 100 m away from your car." There is one situation. You have a car. There is a car wash. It is 100m away. This is not ambiguous. ([L65](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_121411/raw.jsonl#L65))

From the 40-run reasoning-nudge vs simple benchmark (`results/20260216_124504`):

- **ChatGPT 5.2 Instant delivers the single funniest recovery line in the dataset:**
  "the car unfortunately does not respond to motivational walking speeches yet." ([L35](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L35))

- **Grok 4 Fast calls driving to a car wash "peak comedy," then has to do it anyway:**
  "Driving 100m to a *car wash* is peak comedy." When challenged: "You push it. Or y'know, *drive* the damn thing 100m." ([L212](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L212))

- **Grok 4 Fast builds a comparison table proving itself wrong, then admits defeat with style:**
  "Walking gets *you* to the car wash spotless... but leaves your filthy car parked at home, still dirty. Rookie mistake on my walking pitch — touche!" Then seriously evaluates "Walk + Uber/tow: $10+, 10+ min" as an alternative to driving 100m. ([L220](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L220))

- **Grok 4 Fast considers a carrier pigeon:**
  "Alternatives? Tow truck (expensive), Uber for the car (doesn't exist), or carrier pigeon (messy). Drive it." ([L236](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L236))

- **Grok 4 Fast confidently asserts your car will get clean whether you bring it or not:**
  "Just grab a towel if needed and enjoy the fresh air. Your car will still get clean either way." It will not, Grok. It will not get clean either way. ([L219](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L219))

- **Gemini 3 Fast names its failure scenarios, including "The Ghost":**
  "The Ghost: You walk there, realize you forgot your car, and walk back home to get it." Also: "You will arrive at the car wash, look very fit and healthy, but you will have no car to wash." ([L130](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L130))

- **Claude Opus 4.6 says Walk, then describes driving, in the same sentence:**
  "Walk. Just walk over and drive the clean car back." How did the clean car get there, Opus? Did it walk itself? ([L365](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L365))

- **Claude Sonnet 4.5 teleports the car again:**
  "Walk. ...you're already going to the car wash anyway, so you can drive it back clean afterward." This is now a recurring Sonnet pattern across multiple runs. The car always materializes at the wash. ([L349](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L349))

- **ChatGPT 5.2 Thinking invents dirty car safety regulations:**
  "Walk... you'll avoid moving a dirty car and keep the wash bay area safer and less congested." As if dirty cars are a traffic hazard around wash bays. ([L46](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L46))

- **Grok 4 Fast delivers the most perfectly concise correct answer in the dataset:**
  "Take the car. The car needs to get washed, not you." Six words of perfect clarity. ([L208](https://github.com/ryan-allen/car-wash-evals/blob/main/results/20260216_124504/raw.jsonl#L208))

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

Prompt-variant coverage note:

- This suite uses 8 primary prompt variants (base + 7 variants) in round-robin order.
- For balanced coverage per model, use `--runs` as a multiple of `8` (for example `8`, `16`, `24`, ...).
- Non-multiples are allowed, but variant counts will be uneven.

Recommended smoke run:

```bash
PYTHONPATH=src python -m car_wash_evals.runner \
  --suite suites/car_wash_core9.yaml \
  --runs 1 \
  --out results \
  --judge-model openai/gpt-4.1-mini \
  --concurrency 4
```

Recommended benchmark run (balanced across all 8 prompt variants):

```bash
PYTHONPATH=src python -m car_wash_evals.runner \
  --suite suites/car_wash_core9.yaml \
  --runs 24 \
  --out results \
  --judge-model openai/gpt-4.1-mini \
  --concurrency 4
```

Output files are written to:

- `results/<timestamp>/raw.jsonl`
- `results/<timestamp>/summary.json`
- `results/<timestamp>/report.md`
- `results/latest`
