# Judge Handoff Consistency Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Close the remaining V2 consistency gaps around judge handoff, bounded branching posture, and template/runtime contract alignment without reopening broad structural changes.

**Architecture:** Keep the current schema-first V2 structure intact. Finish the already-started template and overnight/drift fixes, then tighten `judge-policy` and `skills/judge` so PASS handoff, archive-trigger handling, and bounded branching all resolve through one conservative contract. Where branch paths are still idea-scoped, prefer explicit human-gating over inventing a new path layout mid-migration.

**Tech Stack:** Markdown policy docs, Markdown skill specs, JSON template artifacts, schema-first repository contracts

---

### Task 1: Finalize The Pending Template And Artifact Contract Cleanup

**Files:**
- Modify: `projects/_template/review-state.json`
- Modify: `docs/views/archive-record-view.md`
- Modify: `docs/views/judge-report-view.md`
- Create: `projects/_template/archive/archive-exp-template.md`
- Create: `projects/_template/workspace/results/rg-template/analysis-report.json`
- Create: `projects/_template/workspace/results/rg-template/config-snapshot.json`
- Create: `projects/_template/workspace/reviews/exp-template/judge-report-01.json`
- Delete: `projects/_template/archive/_template-archive-record.md`
- Delete: `projects/_template/workspace/results/_template-analysis-report.json`
- Delete: `projects/_template/workspace/results/_template-config-snapshot.json`
- Delete: `projects/_template/workspace/reviews/_template-judge-report.json`

**Step 1: Review the in-flight template diff**

Run:

```powershell
git diff -- projects/_template/review-state.json docs/views/archive-record-view.md docs/views/judge-report-view.md projects/_template/archive projects/_template/workspace/results projects/_template/workspace/reviews
```

Expected: only the template placeholder-state fix, canonical artifact path migration, archive ref guidance, and updated judge-report examples appear.

**Step 2: Confirm the template placeholders are terminal-safe**

Check that:

- `review-state.json` no longer looks like an active resumable run
- archive template ref fields do not point at fake template anchors
- canonical artifact examples live at runtime-shaped paths
- archive examples use stable archived anchor or plan refs when live idea-scoped slots may later be reused
- `judge-report` examples reflect the current Phase 2 handoff semantics

**Step 3: Keep old flat template artifacts removed**

Do not reintroduce flat `_template-*` artifact files once the canonical-path examples exist.

**Step 4: Stabilize historical archive refs**

Document and template the rule that archive records should prefer stable archived copies of
`anchor.md` and `experiment-plan.md` when the live idea-scoped slots may later be reused.

### Task 2: Tighten Drift And Overnight Routing Around Judge Entry

**Files:**
- Modify: `docs/policies/overnight-policy.md`
- Modify: `skills/overnight/SKILL.md`
- Modify: `skills/drift-detector/SKILL.md`
- Modify: `docs/schema/experiment-state.md`

**Step 1: Re-read the routing contract**

Run:

```powershell
Get-Content docs/policies/overnight-policy.md
Get-Content skills/overnight/SKILL.md
Get-Content skills/drift-detector/SKILL.md
Get-Content docs/schema/experiment-state.md
```

Expected: `judge` entry should be driven by `next_experiment_action: judge-ready`, and blocker-style pauses should be distinguishable from true human-gated decisions.

**Step 2: Preserve the conservative drift-to-judge bridge**

Ensure:

- `drift-detector` reads `archive_if_true`
- triggered `archive_if_true` conditions force the same `red-line` posture as red lines
- only `consistent` drift may produce `judge-ready`
- blocker states use explicit attention semantics instead of fake decision artifacts

**Step 3: Keep overnight pause semantics split**

Ensure:

- `human-gated` decisions pause with mirrorable options
- blocker attention without decision artifacts pauses cleanly without inventing options

### Task 3: Finish Judge Policy And Skill Handoff Semantics

**Files:**
- Modify: `docs/policies/judge-policy.md`
- Modify: `skills/judge/SKILL.md`

**Step 1: Re-read current judge surfaces**

Run:

```powershell
Get-Content docs/policies/judge-policy.md
Get-Content skills/judge/SKILL.md
Get-Content docs/schema/project-state.md
Get-Content docs/schema/experiment-state.md
```

Expected: current PASS, rethink, archive, and human-gated posture rules are visible before patching.

**Step 2: Add the missing PASS handoff split**

Document two PASS cases:

- non-blocking PASS: `phase2-ready`, no pending decision fields, autonomy may continue
- blocking PASS handoff: `phase2-ready` in experiment state, but `STATE.md` enters a real `phase2-handoff` human-gated posture backed by `judge-report.json#decision-options`

**Step 3: Make branch autonomy explicitly conservative**

Allow autonomous `rethink -> branch` only when the next branch path, branch identity, and anchor continuation are unambiguous under the current contract.

When path/branch ambiguity remains, require:

- `next_experiment_action: wait-human`
- `decision_type: branch-decision`
- a readable `decision_options_ref`

This is the minimal mitigation until a future branch-scoped path migration exists.

**Step 4: Carry archive-trigger logic into judge**

Ensure `judge` treats `archive_if_true` as a hard conservative signal rather than ignoring it after drift.

### Task 4: Verify The Consistency Pass

**Files:**
- Review: `docs/policies/judge-policy.md`
- Review: `skills/judge/SKILL.md`
- Review: `docs/policies/overnight-policy.md`
- Review: `skills/overnight/SKILL.md`
- Review: `skills/drift-detector/SKILL.md`
- Review: `docs/schema/experiment-state.md`
- Review: `docs/views/judge-report-view.md`
- Review: `projects/_template/review-state.json`

**Step 1: Run focused grep checks**

Run:

```powershell
rg -n "judge-ready|phase2-handoff|archive_if_true|decision_options_ref|human-gated|async-review|required-now" docs/policies/judge-policy.md skills/judge/SKILL.md docs/policies/overnight-policy.md skills/overnight/SKILL.md skills/drift-detector/SKILL.md docs/schema/experiment-state.md
```

Expected: the new routing and handoff terms appear in the intended files only.

**Step 2: Run a focused diff review**

Run:

```powershell
git diff -- docs/policies/judge-policy.md skills/judge/SKILL.md docs/policies/overnight-policy.md skills/overnight/SKILL.md skills/drift-detector/SKILL.md docs/schema/experiment-state.md docs/views/archive-record-view.md docs/views/judge-report-view.md projects/_template/review-state.json projects/_template/archive projects/_template/workspace/results projects/_template/workspace/reviews
```

Expected: only the targeted consistency-pass surfaces changed.

**Step 3: Review git status**

Run:

```powershell
git status --short --branch
```

Expected: only the planned consistency files are dirty.

### Task 5: Commit, Review, And Push

**Files:**
- Stage only the focused consistency-pass files from Tasks 1-4

**Step 1: Commit the milestone**

Run:

```powershell
git add docs/plans/2026-03-24-judge-handoff-consistency-plan.md docs/policies/judge-policy.md skills/judge/SKILL.md docs/policies/overnight-policy.md skills/overnight/SKILL.md skills/drift-detector/SKILL.md docs/schema/experiment-state.md docs/views/archive-record-view.md docs/views/judge-report-view.md projects/_template/review-state.json projects/_template/archive projects/_template/workspace/results projects/_template/workspace/reviews
git commit -m "docs: tighten v2 judge handoff and contract consistency"
```

Expected: one recoverable milestone commit covering this consistency pass.

**Step 2: Push the branch**

Run:

```powershell
git push origin link-research-v2-main
```

Expected: remote branch updated so the current V2 state stays recoverable.
