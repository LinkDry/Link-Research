# Critical Skill Migration Matrix

This matrix translates the six highest-risk V1 skills into V2 state ownership and file contracts.

## Shared Migration Rules

1. Skills may write only canonical state views or explicitly allowed evidence/archive files.
2. No skill may treat derived projections such as `workspace/dashboard-data.json` as canonical state.
3. No skill may invent implicit schema fields that are missing from the V2 templates.
4. If a decision is human-gated, the skill must express it through canonical state plus a clearly referenced decision artifact; `review-state.json` may mirror the options during a paused run, but it must not become the hidden source of truth.
5. Skills must reference IDs, paths, and evidence refs consistently with `docs/schema/field-conventions.md`.

## Matrix

| Skill | Primary Purpose | Canonical Reads | Canonical Writes | Explicit Non-Writes | Main V1 Failure Modes | V2 Migration Notes |
|------|------------------|-----------------|------------------|---------------------|-----------------------|--------------------|
| `anchor-wrapper` | lock experiment anchor before execution | `projects/<slug>/project-brief.md`, `projects/<slug>/STATE.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/plans/<idea>/experiment-plan.md` | `projects/<slug>/plans/<idea>/anchor.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/STATE.md` | `results.tsv`, `review-state.json`, dashboard projection | invented fields, index side effects, mutable anchor behavior | V2 should write the anchor record plus only the minimal project/experiment references needed to bind it |
| `drift-detector` | compare active experiment against locked anchor | `projects/<slug>/plans/<idea>/anchor.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/results.tsv`, `analysis-report.json`, `config-snapshot.json` | `projects/<slug>/experiment-memory.md`, `projects/<slug>/STATE.md` | `anchor.md`, `results.tsv`, global memory | frontmatter/body drift, unclear workspace ownership, ambiguous decision writeback | V2 should consume explicit analysis/config artifacts rather than scanning workspace heuristically and should store drift outcome in experiment/project state |
| `judge` | issue Phase 1 verdict and next-step recommendation | `projects/<slug>/project-brief.md`, `projects/<slug>/plans/<idea>/anchor.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/results.tsv`, `analysis-report.json`, `config-snapshot.json`, `projects/<slug>/decision-tree.md`, `memory/lessons-learned.md` | `projects/<slug>/experiment-memory.md`, `projects/<slug>/STATE.md`, `projects/<slug>/decision-tree.md` | `anchor.md`, `results.tsv`, dashboard projection | multiple archive policies, over-broad writes, hidden coupling to verdict log | V2 should keep verdict state canonical in experiment/project views, store detailed rationale in `judge-report.json`, and treat cross-model review as advisory evidence |
| `archive` | close an experiment line and extract reusable lessons | `projects/<slug>/STATE.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/results.tsv`, `projects/<slug>/decision-tree.md`, `projects/<slug>/project-brief.md`, `projects/<slug>/plans/<idea>/anchor.md`, `projects/<slug>/workspace/` relevant artifacts, `memory/lessons-learned.md`, `memory/failure-library.md` | `projects/<slug>/experiment-memory.md`, `projects/<slug>/STATE.md`, `projects/<slug>/decision-tree.md`, `projects/<slug>/archive/archive-<experiment_id>.md`, `memory/lessons-learned.md`, `memory/failure-library.md` | `results.tsv`, anchor files, dashboard projection, `_index.md` files | unsafe deletion, mixed local/global archive boundaries, template mismatch | V2 should be move-or-snapshot oriented, preserve ledgers, update branch governance state, and promote reusable failure patterns globally |
| `reflect` | summarize session learnings and update reusable memory | `projects/<slug>/STATE.md`, `projects/<slug>/experiment-memory.md`, `projects/<slug>/project-brief.md`, `projects/<slug>/review-state.json`, `memory/lessons-learned.md`, optional archive refs | `memory/lessons-learned.md`, `projects/<slug>/STATE.md`, selective project summary fields | `results.tsv`, judge-owned logs, anchor files, dashboard projection | catch-all mutation, frontmatter drift, writing files it only meant to read | V2 should be scoped to synthesis and memory promotion, not system-wide housekeeping |
| `overnight` | orchestrate resumable multi-step Phase 1 or Phase 2 runs | `projects/<slug>/STATE.md`, `projects/<slug>/project-brief.md`, `projects/<slug>/review-state.json`, active experiment/project state | `projects/<slug>/review-state.json`, `projects/<slug>/STATE.md` | canonical writes belonging to sub-skills, dashboard projection as state | plan drift, missing steps, broken pause/resume semantics | V2 should use `review-state.json` as the only run controller and route all scientific state changes through sub-skills |

## Immediate Policy Alignments Required

### `anchor-wrapper`

- Must write a write-once anchor artifact, not an editable note.
- Must not update index-like projections as if they were canonical.
- Must bind the active experiment line through canonical references in `experiment-memory.md`.

### `drift-detector`

- Must not mutate anchor content.
- Must express four possible outcomes consistently: `consistent`, `drift-detected`, `anchor-violation`, `red-line`.
- Must not silently promote a human-gated decision to an auto-continue path.

### `judge`

- Must use one authoritative forced-stop policy, not several competing "three tries" rules.
- Must treat `results.tsv`, structured analysis/config artifacts, and experiment history as the evidence basis.
- Must write next-step posture clearly enough for `overnight` or the human operator to resume.
- PASS must open `phase2-ready` without prematurely flipping the project phase to `phase2`.

### `archive`

- Must never destroy canonical evidence.
- Must separate project-local case records from global reusable lessons.
- Must leave the active project state in a clean, recoverable post-archive posture.
- Must move or snapshot attributable workspace artifacts instead of deleting for convenience.

### `reflect`

- Must update only reusable lessons, capability gaps, and the compact project summary.
- Must not backfill or mutate logs owned by `judge`.
- Must not turn `/garden` behavior into hidden side effects.

### `overnight`

- Must orchestrate only approved sequences.
- Must pause on `human-gated` decisions rather than hand-wave them away.
- Must keep `review-state.json` structurally valid through every checkpoint.

## Open Questions To Resolve During Skill Authoring

1. How much of the Phase 2 flow should remain inside `overnight` versus delegated wholly to a future V2 `phase2-publish` skill?
2. When branch variants exist, should the active `experiment-plan.md` be replaced in place or preserved and linked through explicit archival/version refs?
