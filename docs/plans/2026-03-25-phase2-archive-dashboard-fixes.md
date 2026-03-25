# Phase2 Archive Dashboard Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove the current V2 dead-end and contract drift by adding the missing `phase2-publish` skill, making archive records valid for early-abandonment cases, and resyncing the dashboard template projection with canonical template state.

**Architecture:** Keep the repo schema-first and conservative. Add one minimal but real V2 `phase2-publish` skill so `overnight` can delegate Phase 2 to something concrete. Tighten `archive` contracts so missing anchor or plan context is represented as `null` rather than invented. Then regenerate the template dashboard placeholder so it matches current Project, Experiment, and Run template state instead of stale pre-fix assumptions.

**Tech Stack:** Markdown skill specs, Markdown policy and view contracts, JSON template projections, schema-first V2 repo

---

### Task 1: Add The Missing V2 `phase2-publish` Skill

**Files:**
- Create: `skills/phase2-publish/SKILL.md`

**Step 1: Re-read the current Phase 2 delegation contract**

Run:

```powershell
Get-Content docs/policies/overnight-policy.md
Get-Content skills/overnight/SKILL.md
Get-Content docs/views/judge-report-view.md
```

Expected: the Phase 2 handoff and delegation semantics are visible before authoring the skill.

**Step 2: Write the minimal V2 publication workflow**

The skill must:

- gate on `next_experiment_action: phase2-ready` or active `phase2`
- read only canonical project and experiment state plus referenced evidence artifacts
- write publication outputs only under `projects/<slug>/papers/` plus steering updates in `STATE.md`
- keep `results.tsv`, anchors, `review-state.json`, and dashboard projections outside its write surface
- stop conservatively on fundamental publication-time integrity flaws

**Step 3: Verify the new skill contract**

Run:

```powershell
rg -n "phase2-ready|papers/|Must Not Write|review-state.json|results.tsv|dashboard" skills/phase2-publish/SKILL.md
```

Expected: the skill exposes the intended V2 read/write boundaries and Phase 2 gate.

### Task 2: Make Archive Records Valid For Early-Abandonment Cases

**Files:**
- Modify: `skills/archive/SKILL.md`
- Modify: `docs/policies/archive-policy.md`
- Modify: `docs/views/archive-record-view.md`
- Modify: `projects/_template/archive/archive-exp-template.md`

**Step 1: Relax locked-claim context safely**

Document that for early-abandonment or pre-anchor closures:

- `anchor_path`
- `anchor_version`
- `claim_summary`
- `plan_ref`

may be `null`, and must not be invented.

**Step 2: Keep the evidence-rich archive example intact**

The template should still show the normal archived-snapshot path, but explicitly indicate that those fields become `null` when the line never produced a lockable claim context.

**Step 3: Align memory back-reference wording**

The archive template should allow either concrete row refs or stable IDs for `lesson_ref` and `failure_library_ref`, matching the Memory State contract.

### Task 3: Complete Archive Neutral Reset Defaults

**Files:**
- Modify: `docs/policies/archive-policy.md`

**Step 1: Add the missing compact-summary defaults**

Define exact neutral defaults for the `experiment-memory.md` summary blocks that `skills/archive` already says it must reset:

- `Anchor Summary`
- `Latest Evidence Summary`
- `Latest Analysis Block`

**Step 2: Verify those defaults match the template**

Run:

```powershell
Get-Content projects/_template/experiment-memory.md
rg -n "locked_anchor_path|anchor_claim_summary|primary_signal_summary|recommended_next_action" docs/policies/archive-policy.md
```

Expected: the policy defaults now mirror the template placeholders.

### Task 4: Resync The Dashboard Template Projection

**Files:**
- Modify: `projects/_template/workspace/dashboard-data.json`

**Step 1: Re-derive the placeholder values from canonical templates**

Match the dashboard template to:

- `projects/_template/STATE.md`
- `projects/_template/experiment-memory.md`
- `projects/_template/review-state.json`

while respecting that dashboard data is derived and should reflect no active run when `STATE.md.current_run_id` is `null`.

**Step 2: Keep the file non-canonical**

Do not add new state fields here that exist nowhere else.

**Step 3: Verify the JSON**

Run:

```powershell
Get-Content projects/_template/workspace/dashboard-data.json | ConvertFrom-Json | Out-Null
```

Expected: no JSON parse error.

### Task 5: Verify, Review, And Push

**Files:**
- Review: `skills/phase2-publish/SKILL.md`
- Review: `skills/archive/SKILL.md`
- Review: `docs/policies/archive-policy.md`
- Review: `docs/views/archive-record-view.md`
- Review: `projects/_template/archive/archive-exp-template.md`
- Review: `projects/_template/workspace/dashboard-data.json`

**Step 1: Run focused consistency checks**

Run:

```powershell
git diff --check
rg -n "phase2-publish|phase2-ready|anchor_path|plan_ref|lesson_ref|failure_library_ref|dashboard-data" skills docs projects/_template
```

Expected: no patch-formatting issues and the new contract terms resolve cleanly.

**Step 2: Review git status**

Run:

```powershell
git status --short --branch
```

Expected: only the targeted fix files are modified.

**Step 3: Commit and push**

Run:

```powershell
git add docs/plans/2026-03-25-phase2-archive-dashboard-fixes.md skills/phase2-publish/SKILL.md skills/archive/SKILL.md docs/policies/archive-policy.md docs/views/archive-record-view.md projects/_template/archive/archive-exp-template.md projects/_template/workspace/dashboard-data.json
git commit -m "docs: fix phase2 handoff and archive template regressions"
git push origin link-research-v2-main
```

Expected: the branch is recoverable on GitHub with this fix batch included.
