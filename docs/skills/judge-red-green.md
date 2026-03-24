# `judge` RED/GREEN Verification Notes

## Purpose

Record the baseline failure modes inherited from the legacy `judge` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/judge.md` fails the V2 contract in these specific ways:

1. It depends on non-canonical memory surfaces.
   - Reads `ideation-memory.md` as if it were canonical verdict state.
   - Writes `memory/judge-verdict-log.md` as if verdict history lived outside Experiment State.
2. It embeds its own archive threshold and Phase 2 transition semantics.
   - Carries a hard-coded forced archive rule in the skill body.
   - Treats PASS as if it directly opens and effectively advances the project into publishing.
3. It lacks a structured verdict artifact.
   - Root causes, confidence, and follow-up options live in prose rather than a machine-readable evidence file.
4. It blurs governance recommendation and governance execution.
   - Writes branch-comparison and recommendation prose into `decision-tree.md` without a clear boundary between "recommended" and "already enacted."
5. It treats cross-model review as a near-verdict participant instead of clearly advisory evidence.

## GREEN: Required V2 Behaviors

The V2 `judge` is compliant only if all of the following are true:

1. It reads only canonical steering and evidence inputs:
   - `projects/<slug>/project-brief.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/plans/<idea>/anchor.md`
   - `projects/<slug>/results.tsv`
   - `analysis-report.json`
   - `config-snapshot.json`
   - `projects/<slug>/decision-tree.md`
   - `memory/lessons-learned.md`
2. It writes only allowed canonical state plus one explicit verdict artifact:
   - `projects/<slug>/workspace/reviews/<experiment_id>/judge-report-<iteration>.json`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/decision-tree.md` when branch governance posture changes
3. It never writes:
   - `results.tsv`
   - `review-state.json`
   - `memory/judge-verdict-log.md`
   - dashboard projections
4. It refuses to issue a normal verdict unless the latest drift decision is `consistent`.
5. It uses the single documented forced-stop policy:
   - after 3 consecutive non-pass verdicts on the same branch, no further same-branch `tweak`
6. It records PASS as `phase2-ready` without flipping `STATE.md.phase` to `phase2`.
7. It stores detailed rationale and decision options in `judge-report.json`.
8. It treats cross-model review as advisory only and resolves disagreement conservatively.

## Pass/Fail Checks

### Clean PASS

- Pass if the skill writes `pass`, `phase2-ready`, and a `judge-report.json`.
- Pass if `STATE.md.phase` remains `phase1`.
- Fail if it silently transitions the project to `phase2`.

### Drift Not Resolved

- Pass if the skill stops without writing a normal verdict.
- Fail if it writes `pass` or `tweak` while drift remains unresolved.

### Repeated Non-PASS

- Pass if the skill refuses a fourth same-branch `tweak`.
- Pass if it emits `rethink` or `archive` according to the unified forced-stop policy.
- Fail if it continues the same branch indefinitely.
