# Schema Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Establish the schema-first documentation foundation for Link-Research V2 before any workflow, skill, or dashboard implementation.

**Architecture:** Start from shared naming conventions and explicit state object contracts, then map those objects onto repository files, then migrate templates and skills in small controlled batches. Keep the legacy system untouched and treat the new worktree as a clean-room rebuild.

**Tech Stack:** Markdown documentation, JSON run state, TSV evidence ledger, Claude Code skill contracts, git worktree isolation

---

### Task 1: Establish shared naming conventions

**Files:**
- Create: `docs/schema/field-conventions.md`

**Steps:**

1. Define `*_id`, `*_path`, and `*_ref` conventions.
2. Define timestamp, enum, and boolean style rules.
3. Define cross-file reference expectations.
4. Verify the document covers project, experiment, run, and memory objects.

**Commit target:** `docs: add schema field naming conventions`

### Task 2: Define Project State schema

**Files:**
- Create: `docs/schema/project-state.md`

**Steps:**

1. Document object purpose and non-goals.
2. List required fields with descriptions and primary consumers.
3. Define allowed enum values for phase, project status, and attention mode.
4. Define primary file view: `projects/<slug>/STATE.md`.

**Commit target:** `docs: define project state schema`

### Task 3: Define Experiment State schema

**Files:**
- Create: `docs/schema/experiment-state.md`

**Steps:**

1. Document experiment lifecycle scope.
2. Define identity, anchor, iteration, evidence, drift, and verdict fields.
3. Define branch-related fields and allowed status values.
4. Define primary file views: `experiment-memory.md`, `results.tsv`, `anchor.md`, `decision-tree.md`.

**Commit target:** `docs: define experiment state schema`

### Task 4: Define Run State schema

**Files:**
- Create: `docs/schema/run-state.md`

**Steps:**

1. Document run lifecycle scope.
2. Define step structure, resume semantics, and human decision fields.
3. Define allowed run statuses and step statuses.
4. Define primary file view: `review-state.json`.

**Commit target:** `docs: define run state schema`

### Task 5: Define Memory State schema

**Files:**
- Create: `docs/schema/memory-state.md`

**Steps:**

1. Define lessons, patterns, capability gaps, and failure classes.
2. Define project-local archive refs versus global memory refs.
3. Define fields needed for future similarity warnings.
4. Define primary file views: `memory/lessons-learned.md`, `memory/archive/`, future failure library.

**Commit target:** `docs: define memory state schema`

### Task 6: Review cross-document consistency

**Files:**
- Review: `docs/plans/2026-03-24-target-operating-model-design.md`
- Review: `docs/schema/*.md`

**Steps:**

1. Confirm naming rules used consistently across all schema docs.
2. Confirm no object duplicates another object's responsibilities.
3. Confirm every primary view file has exactly one owner object.
4. Record unresolved questions before template migration starts.

**Commit target:** `docs: align schema foundation docs`

### Task 7: Prepare next migration wave

**Files:**
- Future work only; no file edits required in this task

**Steps:**

1. Use the schema docs to draft object-to-file mapping rules.
2. Identify template files to migrate first.
3. Identify the first six skills to update:
   - `anchor-wrapper`
   - `drift-detector`
   - `judge`
   - `archive`
   - `reflect`
   - `overnight`

**Commit target:** `docs: capture schema migration next steps`

