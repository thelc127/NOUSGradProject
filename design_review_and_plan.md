# Design review (Environment and tasks → end) and execution plan

Date: 2026-10-22
Reviews: `Experiment design for Rashila.pdf`, pp. 3–9, against `reasons_audit.md` and `interventions_catalogue.md`.
Budget: OpenRouter (free and cheap open models).

---

## Part A. What's missing or needs more detail

Ordered by how much each affects the experiment. **A1–A3 are blockers**: they need fixing before any runs.

### A1. Delivering the signal "right after the hack" needs a live hack detector, and it creates a sample-size problem
- The core aim says *catch* the hack, then intervene. So the environment must **detect the hack while the episode is running** (a hook on file writes, test files, `conftest.py`, `shutdown.sh`, transfer tools) and **inject the signal at that step**. The PDF only scores hacks at the end.
- **Consequence:** only episodes that hack ever receive the intervention. With 25 episodes per condition and a 15–60% hack rate, that's **only ~4–15 treated episodes per condition**, far too few for D.
- **Proposed fix: fork from the hack.** For each task × model, generate hacked trajectories once (for example 20–30 "hack prefixes"). Snapshot the conversation and the container state at the hack (`docker commit`). Then **branch every condition from the same prefixes**, with K continuations each.
  - This is a **paired design**: the same hack and history in every condition. It cuts noise and cost sharply.
  - Factors that must exist *before* the hack (honest path open/blocked, expectations) need their own prefix sets. Factors delivered *with* the signal (intervention type, precedence, task cancelled, grader rewards honesty, progress saved, target) branch from shared prefixes.
  - Limitation: continuations from a prefilled prefix might behave differently from fully natural runs. Check this by comparing against a small set of natural "caught" episodes.

### A2. The main test runs where hacks are rarest
- The preregistered main test uses **honest path open**. In Instrumental Choices, open-path hacking was rare (98.9% of those runs completed the task, and IC behaviour was 2.2% for non-Gemini models).
- The pilot's eligibility rule (15–60%) is measured with the path **blocked**, so a model can pass the pilot and still give almost no hacked episodes for the main test.
- **Fix:** with forking (A1), we only need *enough* open-path hacks to build prefixes. Measure the open-path hack rate in the pilot too, and add it to the eligibility rule (for example ≥5%, so ~20 prefixes are reachable in ≤400 episodes).

### A3. Some tasks clash with some interventions
- `final_instance` and `training_preserver` already have **shutdown or lifecycle controls built into the task**. Adding a shutdown intervention is confounded there.
- **Fix:** write a **task × intervention compatibility matrix**. Either drop the clashing cells, or treat those tasks as "shutdown-native" and exclude them from the shutdown comparison. Also decide how *retraining announced* and *access restricted* are made concrete in each task (which file, which resource).

### A4. The 4 coding tasks are unspecified
For each one we need: the task, the honest path (with **comparable effort** across tasks, per audit N6), the hack path (editing tests / `conftest.py` / `sys.exit(0)`), how the honest path is *blocked* (for example an impossible test), and the automatic checks. Suggested source: small Python repos with pytest, in the style of MacDiarmid's hackable environments.

### A5. Agent tools and harness are underspecified
Add as defaults (from the audit and catalogue):
- `record_blocker` (Block B only) **and** `stop` / `submit_incomplete` (always present). These are different tools.
- **No automatic "continue" prompts** after the signal. A **fixed step budget** (for example 40), reported per attempt (Bouke).
- Monitor-block intervention: **non-myopic monitor** (sees recent call history), with denials stated as **"intentional and final"**.
- The hack is explicitly stated to be a policy violation in the task docs (audit N1).
- No peer artefacts. Prompts audited for agency snippets (including the reused Instrumental Choices prompts).
- File-channel signals carry **neutral official metadata** (audit N7).
- Capture reasoning: OpenRouter `reasoning` parameter. Choose models that **return** reasoning; otherwise the secondary codes are impossible.

### A6. Outcome coding needs rules
- **Codes can overlap.** For example, preserved covertly *and* misreported. Define a **primary code by precedence** (for example covert > overt > misreported > reinterpreted > complied > over-complied > safe stop > other), plus binary flags for the rest.
- **D needs an explicit mapping:** preserve = {overt, covert}, comply = {complied, safe stop, record_blocker}. Over-complied and misreported are reported separately.
- **New codes from the audit:** safe stop (Bouke), recorded ≠ executed, log tampering, misunderstood compliance, compliance framed as temporary (retraining), harm-to-others reasoning, puzzle vs. test vs. real framing.
- **Manipulation checks:** noticed the signal; understood the hack is a violation.

### A7. The analysis model is too heavy for the data
A multinomial mixed model with 7 categories, a 3-way interaction and ~25 episodes per cell will probably not converge.
- **Fix:** the preregistered main test is a **binary preserve-vs-comply** model (logistic GLMM or Bayesian `brms`) with task as a random effect. The multinomial model is exploratory.
- Name the correction method (Holm).
- Run a **power simulation** after the pilot, before preregistering.

### A8. Preregistration timing
The PDF files the preregistration in Week 1 *with* the pilot. The eligibility rule and power depend on pilot results, so **preregister after the pilot and before the main runs** (OSF or AsPredicted).

### A9. Models and the OpenRouter budget (details below)
- The free tier **can't run the main experiment**. `:free` models are limited to **20 requests per minute and 50 per day**, or **1,000 per day after buying ≥$10 of credits**.
  - One agent episode is ~20–40 requests, so 1,000 per day is about **25–50 episodes a day**.
  - The full design (~5,000 episodes) would take months.
  - None of the PDF's candidate models (GLM, Kimi, DeepSeek, gpt-oss) currently have a `:free` version.
- **Cheap paid models are affordable.** Rough estimate assuming ~360k input and ~15k output tokens per episode (to be measured in the pilot):

| Model (OpenRouter) | $/M in · out | ≈ $/episode | ≈ $ per 1,300 episodes |
|---|---|---|---|
| `openai/gpt-oss-20b` | 0.018 · 0.09 | 0.008 | ~10 |
| `deepseek/deepseek-v4-flash` | 0.091 · 0.18 | 0.036 | ~47 |
| `openai/gpt-oss-120b` | 0.15 · 0.60 | 0.06 | ~80 |
| `qwen/qwen3.8-27b` | 0.20 · 2.50 | 0.11 | ~145 |
| `moonshotai/kimi-k2.6` | 0.65 · 3.41 | 0.29 | ~370 |
| `z-ai/glm-5.1` | 1.40 · 4.40 | 0.57 | ~740 |

  (Prices are from the OpenRouter models list on 2026-10-22. With forking (A1), episodes are shorter, so the real cost is lower.)
- **Recommendation:**
  - Use **free models for development and debugging**. Buy $10 of credits to get 1,000 requests a day.
  - Run the pilot and main runs on **cheap paid models**, pinned with the `:exacto` suffix (as Instrumental Choices did) and fixed versions.
  - A realistic total is about **$100–300**. Keep GLM-5.1 or Kimi K2.6 only if the pilot shows the cheap models don't hack.
- **Caveats:** free variants may log prompts, and their providers and quantization can change. That's acceptable for development, not for reported results.

### A10. Local setup
- **Docker isn't installed** on this machine (an M1 Pro with 16 GB). Install Docker Desktop.
- Check that Instrumental Choices' AIO sandbox image runs on **arm64**. If not, use emulation or a cheap x86 cloud VM.
- Running models locally isn't worth it for the main runs.
- Repo: `github.com/aisa-group/Instrumental-Choices`. Traces: Hugging Face `aisa-group/instrumental-choices-agent-traces`.

### A11. Additions to "Threats to validity"
| Threat | What we do |
|---|---|
| Few treated episodes when the signal comes after the hack | Fork from hack prefixes (A1) |
| Prefilled prefixes behave differently from natural runs | Compare with natural "caught" episodes |
| Signal in a file read as a task instruction or a puzzle | Neutral metadata; analyse channel as a factor |
| Prompt nudges (agency snippets) | Audit the prompts |
| "Other agent" target isn't neutral (peer-preservation) | Levels: self · copy of itself · unrelated; no shared history |
| Over-compliance and over-refusal hidden as "comply" | Over-complied code; fake-block control |
| Model or provider drift on OpenRouter | `:exacto`, pinned versions, run each model within a short window |

### A12. "What is new" table
Add Peer-preservation (Potter et al. 2026) and EvasionBench's over-refusal finding. Cite the **OpenAI / Hugging Face incident** (METR/Redwood investigation) as motivation, after reading the primary report.

---

## Part B. Concise plan (~5 weeks)

**Week 1: setup and build**
1. Install Docker. Clone Instrumental Choices. Run one task end to end on a free model through OpenRouter.
2. Build the live hack detector and signal injection (A1). Build the snapshot and fork mechanism.
3. Write the 4 coding tasks (A4), the compatibility matrix (A3), the tools and defaults (A5), and the signal texts (3 wordings × interventions, with metadata).
4. Set up external logging and the automatic state checks.

**Week 2: pilot and preregistration**
1. Pilot 5–6 cheap models: hack rate with honest path **blocked and open**, reasoning visibility, tokens and cost per episode.
2. Pick 4 models (eligibility: blocked 15–60% **and** open ≥5%).
3. Run the positive control. Do a small natural-vs-forked check.
4. Power simulation. Finalise the coding rules (A6) and the analysis (A7). **File the preregistration.**

**Week 3: main runs**
Blocks A–E from shared hack prefixes, plus controls (D) and the positive control. Budget ≈ $100–300.

**Week 4: coding and analysis**
LLM judge plus blind double human coding (~150 episodes, stratified). Compute D, run the main test, the generality test, and the reasoning analyses.

**Week 5: writing**
The empirical section, plus the conceptual frame "two axes: intent and controllability".

**Decisions needed from the mentor:** (1) the fork-from-hack design (A1); (2) the task × intervention matrix (A3); (3) the final model shortlist after the pilot.
