# Template Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create the first clean V2 repository scaffold and template files so future skill migration targets concrete, schema-aligned state views instead of loose protocol text.

**Architecture:** Build a minimal but complete template layer around the schema-first contracts already defined in `docs/schema/` and `docs/views/`. Keep canonical state in a small number of files, keep dashboard data derived, and keep archives and memory separate from active project state.

**Tech Stack:** Markdown templates, JSON run state, TSV evidence ledger, git worktree isolation

---

### Task 1: Create Repository Skeleton

**Files:**
- Create: `projects/_template/.gitkeep`
- Create: `projects/_template/archive/.gitkeep`
- Create: `projects/_template/papers/assets/.gitkeep`
- Create: `projects/_template/papers/drafts/.gitkeep`
- Create: `projects/_template/papers/reviews/.gitkeep`
- Create: `projects/_template/plans/.gitkeep`
- Create: `projects/_template/workspace/code/.gitkeep`
- Create: `projects/_template/workspace/data/.gitkeep`
- Create: `projects/_template/workspace/results/.gitkeep`
- Create: `memory/archive/.gitkeep`

**Step 1: Create the directory scaffold**

Create the folders listed above so the V2 repository already matches the target operating model.

**Step 2: Verify the scaffold**

Run: `Get-ChildItem -Recurse 'projects/_template','memory'`
Expected: the key folders above exist.

**Step 3: Commit**

Commit target: `chore: add v2 repository scaffold`

### Task 2: Create Core Project State Templates

**Files:**
- Create: `projects/_template/STATE.md`
- Create: `projects/_template/review-state.json`

**Step 1: Create `STATE.md` from the V2 view contract**

Include only the compact Project State summary sections defined in `docs/views/state-view.md`.

**Step 2: Create `review-state.json` from the V2 view contract**

Use a valid JSON object with placeholder values and one example step entry.

**Step 3: Verify the files**

Run: `Get-Content projects/_template/review-state.json | ConvertFrom-Json | Out-Null`
Expected: no JSON parse error.

**Step 4: Commit**

Commit target: `docs: add v2 project state templates`

### Task 3: Create Core Experiment Templates

**Files:**
- Create: `projects/_template/experiment-memory.md`
- Create: `projects/_template/results.tsv`
- Create: `projects/_template/decision-tree.md`

**Step 1: Create `experiment-memory.md`**

Follow `docs/views/experiment-memory-view.md` with the active snapshot, history tables, and analysis sections.

**Step 2: Create `results.tsv`**

Use the header defined in `docs/views/results-ledger-view.md`.

**Step 3: Create `decision-tree.md`**

Provide a compact branch-governance template aligned with the V2 branch model.

**Step 4: Verify the files**

Run: `Get-Content projects/_template/results.tsv`
Expected: a single header row with the agreed columns.

**Step 5: Commit**

Commit target: `docs: add v2 experiment templates`

### Task 4: Create Supporting Template Files

**Files:**
- Create: `projects/_template/project-brief.md`
- Create: `projects/_template/plans/_template-anchor.md`
- Create: `projects/_template/workspace/dashboard-data.json`
- Create: `memory/lessons-learned.md`
- Create: `memory/failure-library.md`

**Step 1: Create `project-brief.md`**

Keep it human-facing and focused on input constraints, venue goals, resources, and operator preferences.

**Step 2: Create `_template-anchor.md`**

Make anchor immutability explicit and keep the file strongly evidence-oriented.

**Step 3: Create `dashboard-data.json`**

Use a valid placeholder projection structure and make it clear the file is derived, not canonical.

**Step 4: Create global memory templates**

Add one human-readable lessons template and one structured failure-library template.

**Step 5: Verify the JSON file**

Run: `Get-Content projects/_template/workspace/dashboard-data.json | ConvertFrom-Json | Out-Null`
Expected: no JSON parse error.

**Step 6: Commit**

Commit target: `docs: add v2 support templates`

### Task 5: Verify and Publish Template Baseline

**Files:**
- Review: `docs/schema/*.md`
- Review: `docs/views/*.md`
- Review: `projects/_template/*`
- Review: `memory/*`

**Step 1: Run formatting and consistency checks**

Run: `git diff --check`
Expected: no whitespace or patch formatting errors.

**Step 2: Confirm no old schema names remain**

Run: `rg "active_branch\\b|phase-invalidated|consistency_score" .`
Expected: only intentional legacy mentions or no matches in new template files.

**Step 3: Confirm worktree is clean after commit**

Run: `git status -sb`
Expected: clean branch state after commit.

**Step 4: Push the new baseline branch**

Push `link-research-v2-main` so the new template layer is recoverable from GitHub.

**Step 5: Commit**

Commit target: `docs: publish v2 template baseline`
