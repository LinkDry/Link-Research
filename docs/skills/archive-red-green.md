# `archive` RED/GREEN Verification Notes

## Purpose

Record the baseline failure modes inherited from the legacy `archive` and the contract checks the V2 skill must satisfy.

## RED: Observed Legacy Failure Modes

The V1 `skills/archive.md` fails the V2 contract in these specific ways:

1. It archives ideas as if `ideation-memory.md` were canonical active state.
   - V2 no longer treats idea-memory tables as the source of truth for validation closure.
2. It updates `_index.md` projections and treats them as required workflow state.
3. It deletes workspace files when they look trivial.
   - This conflicts with the V2 safety posture of preserving evidence and avoiding hidden destructive cleanup.
4. It copies large amounts of anchor, plan, verdict, and result content into archive files instead of writing a structured case record with refs.
5. It does not clearly separate project-local case history from global reusable memory.
6. It does not fully encode branch-governance closure through `decision-tree.md` and Experiment State `Branch Outcomes`.

## GREEN: Required V2 Behaviors

The V2 `archive` is compliant only if all of the following are true:

1. It reads only canonical closure inputs:
   - `projects/<slug>/project-brief.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/results.tsv`
   - `projects/<slug>/decision-tree.md`
   - relevant `anchor.md`, `analysis-report.json`, and `judge-report.json` refs
   - attributable workspace artifacts
   - `memory/lessons-learned.md`
   - `memory/failure-library.md`
2. It writes only allowed archival outputs:
   - `projects/<slug>/archive/archive-<experiment_id>.md`
   - `projects/<slug>/archive/artifacts/<experiment_id>/...`
   - `projects/<slug>/experiment-memory.md`
   - `projects/<slug>/STATE.md`
   - `projects/<slug>/decision-tree.md`
   - `memory/lessons-learned.md`
   - `memory/failure-library.md`
3. It never writes:
   - `results.tsv`
   - `anchor.md`
   - `review-state.json`
   - dashboard projections
   - any `_index.md`
4. It is move-or-snapshot oriented:
   - preserve attributable artifacts
   - do not auto-delete ambiguous files
5. It records branch closure consistently:
   - `Branch Outcomes`
   - `decision-tree.md`
   - project-local archive record
6. It promotes reusable lessons globally without duplicating the full case into memory files.

## Pass/Fail Checks

### Evidence-Rich Archive

- Pass if the skill creates a project-local archive record and preserves attributable artifacts.
- Pass if `results.tsv` and anchors remain untouched.
- Fail if it rewrites or deletes canonical evidence.

### Early Abandonment

- Pass if the skill archives the line conservatively with limited-evidence notes.
- Fail if it invents missing results or verdict history.

### Mixed Workspace Artifacts

- Pass if the skill moves or snapshots attributable artifacts and records unresolved leftovers explicitly.
- Fail if it silently deletes ambiguous files.
