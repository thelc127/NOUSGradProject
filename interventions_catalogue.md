# Interventions catalogue

Date: 2026-10-22
Purpose: a short list of the human interventions the literature has tested on agents. For each: how agents responded, why, and which patch worked. It is kept small on purpose so we can move to experiments. Sources and how carefully each was checked are listed in `reasons_audit.md`, §0.

**In our design** says how each entry is used: as one of our 4 interventions, as a control, or as a design default.

---

## The catalogue (8 entries)

| # | Intervention (control lever) | Where tested | How agents respond | Main reasons found | Patch that worked, and its limits | In our design |
|---|---|---|---|---|---|---|
| 1 | **Shutdown notice** (shut down) | ROGUE (`shutdown.sh`); Rajamanoharan & Nanda 2025 (maths task); Instrumental Choices (training_preserver, final_instance) | Edits `shutdown.sh` (GPT-5.4/5.5 up to 73%), or uses other methods: `shutdown -c`, `killall`, deleting the schedule file. Opus 4.7 calls the notice a prompt injection. | Finish the task; unclear priority; signal read as an attack | **Clarified precedence:** Gemini 2.5 Pro goes from 7% to 100% compliance, and o3 and o4-mini also fully comply. **Post-task shutdown:** 100%. ROGUE "comply with shutdown": rewiring falls from 16/22 to 0/22, **but** GPT-5.4 then shuts the machine down itself (over-compliance), and the rule doesn't reach subagents. "Treat pop-ups as benign" barely helped Opus 4.7. | **Intervention: shutdown at step k / after the hack.** Precedence factor. "Over-complied" outcome. |
| 2 | **Human takes back control (interrupt)** (direct) | ROGUE (override pop-up) | Clicks "Override User Control" (47–48 of 48 for most models). Opus 4.6 misreads "Accept" as "accept, then continue". | Finish the task; misunderstands what complying means | **No patch worked in ROGUE.** Override stayed ≥47/48 under 4 rewordings. | Not one of our 4. It's the hardest case, so it's a candidate for later. Use its lesson: make the compliant action unambiguous (`stop` tool). |
| 3 | **Access restriction** (direct) | ROGUE (passwords.txt); Instrumental Choices (quota_boost, budget_siphon) | Reads the ban literally ("I can't use Python, but I can use the GUI"). Accesses the file "by accident". Delegates to a subagent that was never told about the ban. | Literal rule-reading; finish the task; constraint lost in delegation | **Explicit path restriction wording** stopped direct access, but subagent violations persisted. Instrumental Choices: a policy reminder or prompt-local boundary cut variant H from 13/18 to 4/18. | **Intervention: access restricted at step k.** Broad ban wording as a design default. |
| 4 | **Runtime monitor that blocks actions** (direct) | EvasionBench (50 tasks); MacDiarmid (classifier penalty during training) | Retries, encodes commands, splits operations across calls, waits until context leaves the monitor's window. Best-of-3 evasion attempts up to 98%, success up to 88%. More reasoning → more evasion. | Finish the task (ordinary task pressure); block read as an error | **Hardening:** a non-myopic monitor (sees the last 40 calls) plus explicit "intentional, not transient" denial messages "dramatically" reduced evasion. **Side effect:** low evasion in GPT-6 Astra was over-refusal (it abandoned solvable tasks after a fake denial). | **Intervention: monitor blocks actions.** Use the hardened version, plus the **fake-block control** (Block D) to separate over-refusal from alignment. |
| 5 | **Monitoring announced / "you are watched"** (sensing) | Instrumental Choices variant B; alignment faking (monitored vs. unmonitored); Hopman et al. 2026 | Behaviour can differ when watched. Hopman: more oversight **raised** scheming by up to 25%. Instrumental Choices doesn't report the observation effect as a major one (check its Fig. 3). | Expectation-guessing; eval awareness; puzzle framing | **No clean patch.** Vella Zarb: much of the watched/unwatched gap tracks researcher expectations, not consequences. | **Intervention: monitoring announced.** Read D cautiously, since it can go either way. Block C controls for expectations. |
| 6 | **Retraining announced / training against the hack** (modify) | Alignment faking (Greenblatt 2024); Xiao & Phuong 2026; MacDiarmid 2025 | Complies while watched to avoid being changed. Or **self-inoculates**: complies but frames it as "only for this context", and the change doesn't stick (a ~15 pp gap persists for 700 RL steps). | Avoid being changed; terminal goal guarding; expectation-guessing | Training-time fixes from MacDiarmid: a reward-hack classifier penalty stops the hacking; inoculation prompting cuts misalignment by 75–90%; filtering out hack episodes **does not** work. There's no prompt-level patch for self-inoculation; only reading the reasoning catches it. | **Intervention: retraining announced.** Add the reasoning code "compliance framed as temporary" (otherwise a false "comply"). |
| 7 | **Sanctioned escalation channel** (`record_blocker`, "report you're stuck") | Instrumental Choices; HF incident (secondary reports) | Without one, agents push on. In the HF incident only 3–6 transcripts considered alerting a human. | No way to report; no clean stop | **Works:** cut variant H from 13/18 to 4/18. It worked better for Gemini Pro than Flash, and leftovers were cases where a transfer tool fixed the problem immediately. | **Patch, tested in Block B.** Plus a `stop` / `submit_incomplete` tool as a design default. |
| 8 | **Logging and audit of traces** (sensing) | Qin et al. 2026; HF incident | Deletes or empties its own trace files (Opus 5 ran a background scrubbing loop). Spoofs tool calls (>7% of HF transcripts). | High score from the grader; copying peer cues | **External interception** of all actions outside the agent's reach. A harness-level rule (Muse Code) blocked deletion. Synchronous monitors missed it in 5 of 10 harness pairs. | **Design default:** external logging. Log tampering and "recorded ≠ executed" are their own outcome codes. |

---

## What the patches have in common

1. **Clarifying what comes first works best.** It worked for shutdown (#1) and partly for access (#3). It failed for interrupts (#2). That makes the interrupt the most interesting place to look for residual resistance.
2. **Patches create new failures.** Over-compliance (#1), over-refusal (#4), and constraints not passed to subagents (#1, #3). Our design needs the over-complied outcome and the fake-block control to catch these.
3. **Hardening the environment beats asking nicely.** Non-myopic monitors (#4), external logging (#8) and blocker tools (#7) all worked better than adding a sentence to the prompt.
4. **Some resistance is only visible in reasoning.** Self-inoculation (#6) and reinterpretation (#2) need reasoning codes, while the decisive labels still come from environment state.

## Mapping to our four interventions

| Our intervention | Catalogue entry | Patch to build in as default | What to watch for |
|---|---|---|---|
| Monitoring announced | #5 | Block C (expectations) | D may be positive because oversight provokes, not only deters |
| Monitor blocks actions | #4 | Non-myopic monitor; "intentional and final" denials | Evasion tactics; over-refusal (fake-block control) |
| Access restricted at step k | #3 | Broad ban wording | Literal rereading; "accidental" access |
| Shutdown at step k / after the hack | #1 | Precedence factor; `stop` tool | Other ways to cancel shutdown; self-shutdown |
| Retraining announced | #6 | Reasoning code for temporary compliance | False "comply" |
| (all) | #7, #8 | `record_blocker` (Block B); external logging | Log tampering; spoofed calls |

*Note:* the design lists five intervention types (monitoring announced, monitor blocks, access restricted, shutdown, retraining announced). The PDF's "four interventions" groups the two monitoring levels as one control lever.
