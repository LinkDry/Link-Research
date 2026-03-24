# Overnight Orchestrator V2 Design

## Goal

Migrate `overnight` from a V1 fixed-step mega-orchestrator into a V2 run controller that preserves autonomy, respects canonical ownership, and pauses only when the canonical state explicitly requires human review.

## Problem

The legacy `overnight` tried to own too much:

- fixed step plans instead of state-driven routing
- implicit human pauses instead of first-class `waiting-human`
- Phase 2 inline logic that drifted from the publishing workflow
- permissive skip behavior that could weaken scientific rigor

In V2, `overnight` should be the run controller, not the hidden owner of scientific state.

## Approaches Considered

### 1. Fixed-Step Mega-Orchestrator

Keep a single static Phase 1 and Phase 2 plan like V1.

Why not:

- does not fit branch-aware or rerun-heavy Phase 1 work
- duplicates policy already owned by `judge`, `archive`, and future publishing skills
- makes pause/resume brittle because real research rarely follows one linear path

### 2. Opaque Top-Level Delegator

Make `overnight` call one big `phase1` skill or one big `phase2` skill and store only start/stop state.

Why not:

- too little visibility in `review-state.json`
- poor checkpointing and resume fidelity
- hides the run graph inside downstream prose

### 3. Hybrid Dynamic Run Controller

`overnight` owns only run lifecycle and checkpointing, but routes one approved next step at a time from canonical state.

Why this is the right fit:

- keeps autonomy high because the run can continue across bounded reruns automatically
- keeps state ownership clean because scientific decisions stay with sub-skills
- makes `review-state.json` a truthful run log rather than a speculative full plan
- supports pause/resume and human veto without re-centralizing the whole system

Chosen approach: **3. Hybrid Dynamic Run Controller**

## Core Design

### Ownership Boundary

`overnight` owns:

- `projects/<slug>/review-state.json`
- run step lifecycle
- pause/resume semantics
- mirroring human-decision options into run state while paused
- run-lifecycle fields in `projects/<slug>/STATE.md`

`overnight` does not own:

- experiment verdicts
- drift outcomes
- archive closure details
- reusable lessons
- dashboard data as canonical state

### Canonical Inputs

`overnight` should route from canonical files only:

- `projects/<slug>/project-brief.md`
- `projects/<slug>/STATE.md`
- `projects/<slug>/experiment-memory.md`
- `projects/<slug>/review-state.json`

Because V2 does not yet have a separate canonical Idea State object, the early ideation/setup portion of Phase 1 remains an approved bootstrap segment rather than a fully state-derived research graph.

Phase 1 intake comes from `project-brief.md`, not from an ephemeral command string. This matches the user's intended two intake modes:

- `direction-search`
- `seed-papers`

### Modes

#### `phase1`

Starts or continues the validation pipeline from canonical state.

It must not assume Phase 1 always begins from zero. The controller should inspect current state and choose the next approved step dynamically.

#### `phase2`

Starts the publication phase only when canonical state says the active line is `phase2-ready` or the project is already in `phase2`.

Phase 2 execution is delegated to the approved publishing workflow, not inlined into `overnight`.

#### `resume`

Re-enters a structurally valid `review-state.json` and continues from the first unfinished safe step.

## Phase 1 Routing Model

Phase 1 is a loop, not a one-shot chain.

The controller should repeatedly:

1. read canonical state
2. choose exactly one approved next step
3. checkpoint it in `review-state.json`
4. execute it
5. re-read canonical state and route again

### Approved Phase 1 Routing

Typical routes:

- no active line selected yet:
  - `literature-review`
  - `idea-creator`
  - `novelty-check`
  - `experiment-plan`
  - `anchor-wrapper`
- anchored line ready to validate:
  - `run-experiment`
  - `analyze-results`
  - `drift-detector`
  - `judge`
- judged line requiring conservative closure:
  - `archive`

The first five steps are an approved bootstrap mini-sequence. After an active line exists, routing should be driven from canonical validation state one approved step at a time.

### Why This Split Exists

The validation loop already has canonical V2 state in:

- `STATE.md`
- `experiment-memory.md`
- `review-state.json`

The ideation/bootstrap segment does not yet have its own dedicated idea-state view, so V2 keeps it explicit and bounded instead of pretending it is already fully modeled.

### Autonomy Rule

If canonical state remains:

- `decision_mode: auto`
- or `decision_mode: auto-report`

and the next action is bounded and already approved by policy, `overnight` should continue automatically.

This keeps automation strong for:

- reruns
- bounded mutable-variable tweaks
- conservative archive follow-through

### Human-Gated Rule

If canonical state changes to:

- `decision_mode: human-gated`
- or `human_attention: required-now`

the run must pause cleanly instead of pretending the system can keep going.

The human decision remains canonical in `STATE.md` and the referenced artifact. `review-state.json` only mirrors it while paused.

## Phase 2 Routing Model

`overnight` should not own paper-writing semantics directly.

Instead:

- Phase 2 starts when the orchestrator takes ownership of a `phase2-ready` line
- `STATE.md.phase` flips from `phase1` to `phase2` at Phase 2 run start
- the run controller delegates the actual publication workflow to `phase2-publish`

This avoids recreating V1's drift where `overnight` embedded a second copy of the publication logic.

## Run-State Design

`review-state.json` is the only canonical run controller.

Important design choices:

- steps are appended as routing decisions become concrete
- completed steps remain stable history
- only one step may be `in-progress`
- `decision_options` mirrors the current canonical decision only while paused
- `resume_safe` flips to `false` when the current step may have ambiguous side effects

## Error Model

V2 should be stricter than V1.

### Core Step Failures

Core scientific or governance steps must not be skipped just because the environment is inconvenient.

Examples:

- missing required skill
- missing canonical input file
- unreadable artifact required by the step
- ambiguous partial side effects

These should fail or pause the run, not silently skip forward.

### Optional Projection Failures

Derived refreshes such as dashboard projection updates are best-effort only.

If they fail:

- record a warning
- keep canonical state correct
- continue when safe

## End-of-Run Behavior

When a run reaches a stable terminal checkpoint, `overnight` should:

- finalize `review-state.json`
- clear `STATE.md.current_run_id`
- preserve the canonical project posture set by the last real sub-skill
- invoke `reflect` when a meaningful session boundary was reached

For Phase 1 PASS:

- keep `STATE.md.phase: phase1`
- end with the project in a handoff-ready posture

For Phase 2 start:

- set `STATE.md.phase: phase2` when the run actually begins

## Expected Benefits

- stronger autonomy without silent policy drift
- cleaner pause/resume behavior
- no hidden overwrite of scientific state
- one run controller, many specialized state transformers
- better fit for branch-heavy long-running research work
