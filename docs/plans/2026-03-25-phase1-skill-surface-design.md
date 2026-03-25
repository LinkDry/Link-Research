# Link-Research V2 Phase 1 Skill Surface Design

**Goal:** Complete the missing V2 Phase 1 skill surface so `overnight` can route a full idea-to-evidence validation loop without relying on undefined bootstrap or execution steps.

## Problem

The V2 rebuild already has the core governance spine:

- `anchor-wrapper`
- `drift-detector`
- `judge`
- `archive`
- `reflect`
- `overnight`

But `overnight` still delegates six Phase 1 skills that do not yet exist in-repo:

- `literature-review`
- `idea-creator`
- `novelty-check`
- `experiment-plan`
- `run-experiment`
- `analyze-results`

That leaves the orchestration path structurally incomplete even though the downstream governance layer is now stable.

## Design Principles

1. Bootstrap artifacts are durable but non-canonical.
2. Canonical state must remain in `STATE.md`, `experiment-memory.md`, `review-state.json`, and `results.tsv`.
3. Evidence artifacts must remain explicit and machine-readable where downstream skills depend on them.
4. The missing skills should plug into the existing V2 ownership model rather than invent a parallel one.
5. Automation should stay strong for routine routing, but the skills must remain conservative about integrity and traceability.

## Chosen Surface Split

### Bootstrap Planning Artifacts

The first three skills produce durable bootstrap artifacts under:

- `projects/<slug>/workspace/bootstrap/literature-review.md`
- `projects/<slug>/workspace/bootstrap/idea-candidates.md`
- `projects/<slug>/workspace/bootstrap/novelty-check.md`

These files are:

- planning inputs or review artifacts
- repository-traceable
- intentionally non-canonical

They help bridge the current absence of a dedicated Idea State object without polluting canonical experiment state too early.

### Canonical Planning And Evidence Artifacts

The remaining three skills write only to already approved canonical or evidence paths:

- `projects/<slug>/plans/<idea>/experiment-plan.md`
- `projects/<slug>/results.tsv`
- `projects/<slug>/workspace/results/<result-group-id>/config-snapshot.json`
- `projects/<slug>/workspace/results/<result-group-id>/analysis-report.json`
- canonical steering updates in `STATE.md`
- canonical experiment updates in `experiment-memory.md`
- branch register updates in `decision-tree.md` when a new active line is formally established

## Skill Roles

### `literature-review`

Bootstrap a scoped landscape scan from `project-brief.md`, recent lessons, and failure patterns.

Primary output:

- one literature review artifact

Canonical impact:

- Phase 1 starts
- steering summary points to idea generation next

### `idea-creator`

Turn the literature scan into 2-5 concrete candidate ideas with bounded claims, novelty basis, and early failure signals.

Primary output:

- one idea-candidate set artifact

Canonical impact:

- steering summary points to novelty filtering next

### `novelty-check`

Filter the idea set conservatively and choose one primary candidate for planning.

Primary output:

- one novelty-check artifact with the chosen `idea_id`

Canonical impact:

- `STATE.md.active_idea_id` may become non-null before the active experiment line exists
- the next action becomes plan authoring

### `experiment-plan`

Create the first concrete line plan or the next bounded branch plan using the existing `experiment-plan.md` contract.

Primary output:

- `projects/<slug>/plans/<idea>/experiment-plan.md`

Canonical impact:

- an active experiment line is instantiated or replaced in `experiment-memory.md`
- `STATE.md.active_idea_id` and `active_branch_id` are aligned
- `decision-tree.md` reflects the active planned branch

### `run-experiment`

Record one attributable execution event as canonical evidence.

Primary outputs:

- appended `results.tsv` rows
- one `config-snapshot.json`
- optional attributable result-bundle files under the result-group directory

Canonical impact:

- latest result refs and iteration state in `experiment-memory.md`
- steering summary points to `analyze-results`

### `analyze-results`

Interpret the latest result group conservatively into a machine-readable analysis artifact.

Primary output:

- one `analysis-report.json`

Canonical impact:

- `latest_analysis_ref` becomes current
- steering summary points to `drift-detector`

## Key State Rules

### Before `experiment-plan`

Canonical experiment state should remain inactive:

- no active `experiment_id`
- no active `branch_id`
- no anchor

Bootstrap artifacts carry the temporary ideation context.

### After `experiment-plan`

The canonical active line exists, even before anchoring:

- `experiment_id` is set
- `idea_id` is set
- `branch_id` is set
- `status: planned`
- `anchor_path: null`

### After `run-experiment`

There is new evidence, but no interpretation yet:

- `latest_result_ref` points to the latest result group
- `latest_analysis_ref` remains `null` until analysis exists
- prior drift or judge state should not silently remain current for the new iteration

### After `analyze-results`

There is structured interpretation, but still no verdict:

- `latest_analysis_ref` points to `analysis-report.json`
- `drift-detector` remains the next integrity gate

## Non-Goals

- no dedicated Idea State object in this batch
- no new runner framework for executing experiments
- no dashboard redesign in this batch
- no branch-scoped path migration in this batch

## Expected Outcome

After this batch:

- `overnight` will no longer depend on undefined Phase 1 skills
- bootstrap outputs will have stable repository-visible contracts
- the idea-to-anchor-to-evidence path will be fully represented inside V2
