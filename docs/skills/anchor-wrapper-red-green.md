# `anchor-wrapper` RED/GREEN Verification Notes

## Purpose

Record the baseline failure modes observed from the legacy `anchor-wrapper` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/anchor-wrapper.md` fails the V2 contract in these specific ways:

1. It writes hidden state outside canonical ownership.
   - Attempts to update `projects/<slug>/plans/_index.md`.
   - Invents `anchor_locked` and `anchor_status` style state in `experiment-memory.md` instead of using the V2 snapshot fields and anchor summary fields already defined.
2. It depends on an implicit experiment-plan structure.
   - V1 assumes `/experiment-plan` output contains fields like "Original Hypothesis", "Mutable Variables", and "Immutable Variables", but V2 previously had no explicit input template for that contract.
3. It risks anchor drift through protocol-level exceptions.
   - The prose tries to enforce immutability, but the state model did not previously isolate the write-once artifact cleanly from other mutable files.

## GREEN: Required V2 Behaviors

The V2 `anchor-wrapper` is compliant only if all of the following are true:

1. It reads only canonical inputs:
   - `projects/<slug>/project-brief.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/plans/<idea>/experiment-plan.md`
2. It writes only canonical outputs:
   - `projects/<slug>/plans/<idea>/anchor.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/STATE.md`
3. It does not write:
   - `results.tsv`
   - `review-state.json`
   - `workspace/dashboard-data.json`
   - any `_index.md`
4. It never rewrites an existing anchor in place.
5. It fails closed if the experiment plan lacks quantitative success criteria, variable boundaries, `source_refs`, or `disconfirming_signals`.

## Current Template Support

The V2 templates now expose all state the skill should touch:

- `experiment-memory.md`
  - `anchor_path`
  - `anchor_version`
  - `status`
  - `next_experiment_action`
  - `last_updated`
  - `locked_anchor_path`
  - `anchor_claim_summary`
  - `anchor_constraints`
- `STATE.md`
  - `phase`
  - `project_status`
  - `active_idea_id`
  - `active_branch_id`
  - `next_action`
  - `last_completed_skill`
- `plans/_template-anchor.md`
  - write-once anchor record structure
- `plans/_template-experiment-plan.md`
  - template source for the active `projects/<slug>/plans/<idea>/experiment-plan.md`

## Pass/Fail Checks

### Happy Path

- Pass if the skill produces one anchor file and updates only `STATE.md` plus `experiment-memory.md`.
- Pass if `next_experiment_action` becomes `run-first-experiment` or `wait-human` for a real blocker.
- Fail if it updates any index or derived projection file.

### Missing Success Criteria

- Pass if the skill stops without creating `anchor.md`.
- Fail if it invents thresholds or silently proceeds.

### Anchor Rewrite Attempt

- Pass if the skill refuses in-place rewrite and instructs a new anchor version or branch.
- Fail if it edits the existing anchor record.
