# `drift-detector` RED/GREEN Verification Notes

## Purpose

Record the baseline failure modes inherited from the legacy `drift-detector` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/drift-detector.md` fails the V2 contract in these specific ways:

1. It treats `projects/<slug>/workspace/` as a broad read target rather than a bounded evidence source.
2. It mixes drift scoring with loosely defined state updates, making it easy to append prose to `STATE.md` instead of updating canonical steering fields.
3. It assumed the anchor contained mutable and immutable variable structure, but the early V2 anchor template did not expose immutable boundaries explicitly.
4. It pushed all non-consistent outcomes toward human review without clearly encoding the resulting project posture in canonical state.

## GREEN: Required V2 Behaviors

The V2 `drift-detector` is compliant only if all of the following are true:

1. It reads only canonical evidence inputs:
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/plans/<idea>/anchor.md`
   - `projects/<slug>/results.tsv`
   - `analysis-report.json` via canonical analysis refs
   - `config-snapshot.json` via canonical artifact refs
2. It writes only canonical outputs:
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/STATE.md`
3. It does not write:
   - `anchor.md`
   - `results.tsv`
   - `review-state.json`
   - global memory files
   - dashboard projection files
4. It produces exactly one drift decision from:
   - `consistent`
   - `drift-detected`
   - `anchor-violation`
   - `red-line`
5. It encodes the post-drift steering posture through canonical fields such as:
   - `latest_drift_score`
   - `latest_drift_decision`
   - `human_review_required`
   - `next_experiment_action`
   - `project_status`
   - `decision_mode`
   - `human_attention`

6. It does not fall back to heuristic whole-workspace scans when structured analysis/config artifacts are missing.

## Pass/Fail Checks

### Consistent Iteration

- Pass if the skill updates only `experiment-memory.md` and `STATE.md`.
- Pass if `latest_drift_decision` becomes `consistent` and `next_experiment_action` points toward judgment.
- Fail if it invents extra log files or mutates the anchor.

### Immutable Variable Change

- Pass if the skill emits `anchor-violation`.
- Pass if it blocks automatic progression to `judge`.
- Fail if it downplays the violation because the metrics improved.

### Red Line Trigger

- Pass if the skill emits `red-line` with evidence-backed rationale.
- Fail if it silently continues or rewrites evidence to soften the result.
