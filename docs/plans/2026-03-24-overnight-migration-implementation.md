# Overnight Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate V2 `overnight` into a dynamic, resumable run controller that preserves autonomy while respecting the canonical ownership boundaries of `judge`, `archive`, and `reflect`.

**Architecture:** Define a single overnight policy, tighten the migration specs around exact changed and untouched files, then author the V2 `skills/overnight/SKILL.md` as a state-driven router over `STATE.md`, `experiment-memory.md`, and `review-state.json`. Keep publication semantics delegated to `phase2-publish` so `overnight` owns run lifecycle rather than paper logic.

**Tech Stack:** Markdown policy docs, Markdown skill specs, JSON run-state contract, schema-first V2 repository

---

### Task 1: Write The Overnight Design And Policy Surface

**Files:**
- Create: `docs/plans/2026-03-24-overnight-orchestrator-design.md`
- Create: `docs/policies/overnight-policy.md`
- Modify: `docs/skills/critical-skill-migration-matrix.md`

**Step 1: Re-read the current V2 run-control contracts**

Run:

```powershell
Get-Content docs/schema/run-state.md
Get-Content docs/views/review-state-view.md
Get-Content docs/schema/project-state.md
```

Expected: the existing V2 ownership boundaries and run-state fields are visible before policy writing.

**Step 2: Write the overnight design and policy**

Document:

- dynamic phase routing instead of a fixed mega-plan
- autonomy-first continuation rules
- human-gated pause rules
- Phase 2 delegation to `phase2-publish`
- strict error handling for core scientific steps

**Step 3: Tighten the migration matrix**

Record that V2 `overnight`:

- writes only `review-state.json` and run-lifecycle fields in `STATE.md`
- does not own scientific state
- delegates Phase 2 execution to the publishing workflow

**Step 4: Verify the policy language**

Run:

```powershell
rg -n "phase2-publish|human-gated|review-state.json|STATE.md" docs/policies/overnight-policy.md docs/skills/critical-skill-migration-matrix.md docs/plans/2026-03-24-overnight-orchestrator-design.md
```

Expected: all key ownership and routing terms are present.

### Task 2: Tighten The RED/GREEN Spec For Overnight

**Files:**
- Create: `docs/skills/overnight-red-green.md`
- Modify: `docs/skills/critical-skill-baseline-scenarios.md`

**Step 1: Capture the legacy failure modes**

Write the RED section around:

- fixed-step orchestration drift
- missing first-class human pause semantics
- Phase 2 duplication
- permissive skip behavior for core steps

**Step 2: Define the V2 GREEN requirements**

Require:

- dynamic routing from canonical state
- pause via `waiting-human`
- mirrored decision options only in run state
- no direct writes to experiment, archive, or memory state

**Step 3: Tighten baseline scenarios**

Add exact changed and untouched file expectations for the `overnight` scenarios in `docs/skills/critical-skill-baseline-scenarios.md`.

**Step 4: Verify scenario coverage**

Run:

```powershell
rg -n "## `overnight`|changed files|untouched files|waiting-human|phase2" docs/skills/overnight-red-green.md docs/skills/critical-skill-baseline-scenarios.md
```

Expected: the overnight scenarios now specify concrete file effects and pause behavior.

### Task 3: Author The V2 Overnight Skill

**Files:**
- Create: `skills/overnight/SKILL.md`

**Step 1: Re-read the migrated governance skills**

Run:

```powershell
Get-Content skills/judge/SKILL.md
Get-Content skills/archive/SKILL.md
Get-Content skills/reflect/SKILL.md
```

Expected: overnight handoff rules are grounded in current migrated contracts, not memory.

**Step 2: Write the minimal V2 skill**

The skill must:

- read only canonical run-routing inputs
- initialize or resume `review-state.json`
- choose one approved next step at a time
- pause when `STATE.md` says the run is human-gated
- finalize with `reflect` at stable run boundaries

**Step 3: Add explicit non-write boundaries**

Ensure the skill says it must not write:

- `experiment-memory.md`
- `results.tsv`
- anchors
- archive records
- memory files directly
- dashboard projection as canonical state

**Step 4: Verify the skill contract**

Run:

```powershell
rg -n "Must Not Write|phase2-publish|waiting-human|resume_safe|reflect" skills/overnight/SKILL.md
```

Expected: the skill text exposes the key V2 guardrails and lifecycle checkpoints.

### Task 4: Align Run-State Docs With Dynamic Routing

**Files:**
- Modify: `docs/schema/run-state.md`
- Modify: `docs/views/review-state-view.md`

**Step 1: Add dynamic-step guidance**

Clarify that `steps[]` may grow as routing decisions become concrete, while completed records remain stable.

**Step 2: Add pause/resume guidance**

Clarify:

- paused human decisions are mirrored, not owned, in `review-state.json`
- resuming requires the current decision posture to be cleared or advanced canonically

**Step 3: Verify the run-state docs**

Run:

```powershell
rg -n "append|mirrors|resume|waiting-human|completed steps" docs/schema/run-state.md docs/views/review-state-view.md
```

Expected: the dynamic-routing and pause/resume rules are explicit.

### Task 5: Verify, Commit, And Push

**Files:**
- Review: `docs/policies/overnight-policy.md`
- Review: `docs/skills/overnight-red-green.md`
- Review: `skills/overnight/SKILL.md`
- Review: `docs/schema/run-state.md`
- Review: `docs/views/review-state-view.md`

**Step 1: Run a focused diff review**

Run:

```powershell
git diff -- docs/policies/overnight-policy.md docs/skills/overnight-red-green.md skills/overnight/SKILL.md docs/schema/run-state.md docs/views/review-state-view.md docs/skills/critical-skill-migration-matrix.md docs/skills/critical-skill-baseline-scenarios.md
```

Expected: only the intended overnight migration surfaces changed.

**Step 2: Confirm git status**

Run:

```powershell
git status --short --branch
```

Expected: only the overnight migration files are staged or modified.

**Step 3: Commit**

Run:

```powershell
git add docs/policies/overnight-policy.md docs/skills/overnight-red-green.md skills/overnight/SKILL.md docs/schema/run-state.md docs/views/review-state-view.md docs/skills/critical-skill-migration-matrix.md docs/skills/critical-skill-baseline-scenarios.md docs/plans/2026-03-24-overnight-orchestrator-design.md docs/plans/2026-03-24-overnight-migration-implementation.md
git commit -m "docs: migrate v2 overnight contract and skill"
```

Expected: a clean commit containing the overnight migration.

**Step 4: Push**

Run:

```powershell
git push origin link-research-v2-main
```

Expected: remote branch updated for recoverability.
