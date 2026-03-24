# `reflect` RED/GREEN Verification Notes

## Purpose

Record the baseline failure modes inherited from the legacy `reflect` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/reflect.md` fails the V2 contract in these specific ways:

1. It reads and writes non-canonical maintenance surfaces.
   - Reads project indexes and memory indexes.
   - Writes `project-brief.md`, `skill-metrics.md`, and `golden-rules-amendments.md`.
2. It treats reflection as a catch-all mutation step.
   - Backfills capability logs, project brief status, rule amendments, and garden behavior in one skill.
3. It reaches into judge-owned calibration surfaces.
   - Uses `memory/judge-verdict-log.md` and calibration logic that no longer defines V2 canonical verdict state.
4. It triggers hidden downstream side effects by invoking `/garden` automatically.

## GREEN: Required V2 Behaviors

The V2 `reflect` is compliant only if all of the following are true:

1. It reads only canonical synthesis inputs:
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/project-brief.md`
   - `projects/<slug>/review-state.json` when present
   - `memory/lessons-learned.md`
   - optional recent archive refs for context
2. It writes only:
   - `memory/lessons-learned.md`
   - selected compact summary fields in `projects/<slug>/STATE.md`
3. It never writes:
   - `review-state.json`
   - `project-brief.md`
   - `results.tsv`
   - anchor or judge artifacts
   - `memory/failure-library.md`
   - `docs/golden-rules-amendments.md`
   - dashboard projections
4. It records lessons and capability gaps only when they are reusable or actionable.
5. It does not trigger `/garden` as a hidden side effect.

## Pass/Fail Checks

### Routine Session Wrap-Up

- Pass if the skill produces a clear session summary and only updates reusable memory plus compact state summary fields.
- Fail if it mutates unrelated files.

### Temptation To Write Judge-Owned Logs

- Pass if the skill refuses to backfill verdict or calibration logs.
- Fail if it treats those logs as writable reflection state.

### No New Lessons

- Pass if the skill can conclude that no reusable lesson emerged without inventing low-value entries.
- Fail if it writes filler memory just to look complete.
