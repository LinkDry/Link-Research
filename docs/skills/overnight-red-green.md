# `overnight` RED/GREEN Verification Notes

## Purpose

Record the legacy failure modes inherited from V1 `overnight` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/overnight.md` fails the V2 contract in these specific ways:

1. It treats the run as a fixed mega-plan instead of a state-driven controller.
   - Phase 1 and Phase 2 are predeclared as long static pipelines even when the real project posture changes mid-run.
2. It has no first-class human-gated pause model.
   - Human review is implied or deferred to downstream skills rather than represented explicitly in Run State.
3. It duplicates publication workflow semantics.
   - Phase 2 is embedded directly in `overnight` instead of delegating to an approved publishing workflow.
4. It allows capability-gap skipping for core scientific steps.
   - That weakens scientific rigor because required work can disappear from the run while the pipeline keeps advancing.
5. It treats input intent too ephemerally.
   - Phase 1 is driven by a transient topic string rather than the project's canonical intake configuration in `project-brief.md`.

## GREEN: Required V2 Behaviors

The V2 `overnight` is compliant only if all of the following are true:

1. It reads only canonical run-routing inputs:
   - `projects/<slug>/project-brief.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/review-state.json`
   - `docs/policies/overnight-policy.md`
2. It writes only:
   - `projects/<slug>/review-state.json`
   - run-lifecycle fields in `projects/<slug>/STATE.md`
3. It never writes:
   - `experiment-memory.md`
   - `results.tsv`
   - anchors
   - archive records
   - `memory/*`
   - dashboard projections as canonical state
4. It uses the approved Phase 1 bootstrap segment only until an active line exists, then routes one approved step at a time from canonical state.
5. It pauses via `waiting-human` and mirrors current decision options into `review-state.json` instead of inventing a second decision system.
6. It delegates publication execution to `phase2-publish`.
7. It does not silently skip core scientific or governance steps.
8. It invokes `reflect` only as an end-of-run or stable checkpoint action, not as hidden housekeeping in the middle of scientific state transitions.

## Pass/Fail Checks

### Phase 1 Autonomous Run

- Pass if the skill creates a valid run record and executes only the approved bootstrap or validation route for the current posture.
- Pass if it keeps `review-state.json` truthful after every checkpoint.
- Fail if it hard-codes a long plan that no longer matches canonical state.

### Human-Gated Decision

- Pass if the skill pauses cleanly and mirrors the pending decision into `review-state.json`.
- Pass if the canonical decision remains in `STATE.md` and the referenced artifact.
- Fail if the run pretends the decision was resolved automatically.

### Resume After Interruption

- Pass if the skill resumes from the first unfinished safe step and preserves completed-step history.
- Pass if it refuses unsafe resume when side effects are ambiguous.
- Fail if it rewrites prior step history or resumes from the wrong place.

### Phase 2 Handoff

- Pass if the skill flips `STATE.md.phase` only when the Phase 2 run actually starts.
- Pass if publication work is delegated to `phase2-publish`.
- Fail if `overnight` embeds a second source of truth for citation or writing workflow.
