# Critical Skill Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate the first six critical research-governance skills to Link-Research V2 without reintroducing the contract drift, hidden state, and governance conflicts that accumulated in V1.

**Architecture:** Treat each skill as a schema-aligned state transformer over the new V2 templates. Before authoring any skill, define its allowed reads and writes, identify legacy failure modes, and create pressure scenarios so the new skill is written test-first instead of prose-first.

**Tech Stack:** Markdown skill contracts, schema-driven state files, JSON run state, TSV result ledger, test-first skill authoring workflow

---

### Task 1: Create the Skill Migration Matrix

**Files:**
- Create: `docs/skills/critical-skill-migration-matrix.md`

**Step 1: Define the six-skill migration scope**

Cover these skills in order:

- `anchor-wrapper`
- `drift-detector`
- `judge`
- `archive`
- `reflect`
- `overnight`

**Step 2: Record per-skill contract data**

For each skill, document:

- owner objects touched
- canonical reads
- canonical writes
- forbidden writes
- required outputs
- unresolved policy questions

**Step 3: Verify the matrix against V2 views**

Confirm every listed read or write maps to files that now exist in `projects/_template/` or `memory/`.

**Step 4: Commit**

Commit target: `docs: add critical skill migration matrix`

### Task 2: Create Baseline Pressure Scenarios

**Files:**
- Create: `docs/skills/critical-skill-baseline-scenarios.md`

**Step 1: Define RED-phase scenarios**

For each of the six skills, define:

- one happy-path scenario
- one contract-violation scenario
- one governance-pressure scenario

**Step 2: Define pass/fail expectations**

For each scenario, specify:

- expected legacy failure mode
- expected V2 compliant behavior
- state files that should change
- state files that must remain untouched

**Step 3: Verify scenarios are concrete**

Each scenario must mention exact files and the decision that would reveal whether the skill is compliant.

**Step 4: Commit**

Commit target: `docs: add critical skill baseline scenarios`

### Task 3: Migrate `anchor-wrapper`

**Files:**
- Create: `skills/anchor-wrapper/SKILL.md`
- Review: `docs/skills/critical-skill-migration-matrix.md`
- Review: `docs/skills/critical-skill-baseline-scenarios.md`

**Step 1: Run RED baseline for `anchor-wrapper`**

Demonstrate the legacy behavior or expected failure mode before writing the V2 skill.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- create a write-once anchor record
- update only the allowed canonical files
- avoid hidden writes to indexes or derived projections

**Step 3: Run GREEN verification**

Confirm the new skill follows the V2 contract under the baseline scenarios.

**Step 4: Commit**

Commit target: `docs: migrate v2 anchor-wrapper skill`

### Task 4: Migrate `drift-detector`

**Files:**
- Create: `skills/drift-detector/SKILL.md`

**Step 1: Run RED baseline for `drift-detector`**

Focus on immutable-variable violations, score-to-decision consistency, and allowed writes.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- read the anchor and latest evidence
- update only the experiment and project steering views
- avoid turning workspace inspection into hidden state ownership

**Step 3: Run GREEN verification**

Confirm decision outputs and file updates match the baseline scenarios.

**Step 4: Commit**

Commit target: `docs: migrate v2 drift-detector skill`

### Task 5: Migrate `judge`

**Files:**
- Create: `skills/judge/SKILL.md`

**Step 1: Run RED baseline for `judge`**

Test verdict conservatism, forced-archive logic, and Phase 2 gating.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- depend on a completed drift check
- derive verdicts from anchor plus evidence
- write only canonical verdict state and branch governance state
- keep any cross-model verification as advisory rather than hidden state

**Step 3: Run GREEN verification**

Confirm `PASS`, `TWEAK`, `RETHINK`, and `ARCHIVE` each produce the expected state transitions.

**Step 4: Commit**

Commit target: `docs: migrate v2 judge skill`

### Task 6: Migrate `archive`

**Files:**
- Create: `skills/archive/SKILL.md`

**Step 1: Run RED baseline for `archive`**

Test archive behavior under evidence-rich and early-abandonment cases.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- preserve append-only evidence ledgers
- move or snapshot substantive artifacts
- avoid destructive cleanup that conflicts with the safety model
- extract reusable lessons into global memory

**Step 3: Run GREEN verification**

Confirm active state clears correctly and archive records remain traceable.

**Step 4: Commit**

Commit target: `docs: migrate v2 archive skill`

### Task 7: Migrate `reflect`

**Files:**
- Create: `skills/reflect/SKILL.md`

**Step 1: Run RED baseline for `reflect`**

Test that session synthesis does not silently become a catch-all writer for unrelated files.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- summarize session changes from canonical views
- write lessons and capability gaps only where appropriate
- avoid writing run-controller state or judge-owned logs

**Step 3: Run GREEN verification**

Confirm lessons, gaps, and project summary updates are correctly scoped.

**Step 4: Commit**

Commit target: `docs: migrate v2 reflect skill`

### Task 8: Migrate `overnight`

**Files:**
- Create: `skills/overnight/SKILL.md`

**Step 1: Run RED baseline for `overnight`**

Test pause/resume, human-gated decisions, and Phase 2 orchestration consistency.

**Step 2: Write the minimal V2 skill**

The V2 version must:

- use `review-state.json` as the only run controller
- call only the approved Phase 1 and Phase 2 sequences
- pause cleanly when a human-gated decision is required
- keep dashboard refreshes derived, not canonical

**Step 3: Run GREEN verification**

Confirm resume semantics and end-of-run summaries match the plan.

**Step 4: Commit**

Commit target: `docs: migrate v2 overnight skill`

### Task 9: Verify Skill-System Consistency

**Files:**
- Review: `docs/schema/*.md`
- Review: `docs/views/*.md`
- Review: `docs/skills/*.md`
- Review: `skills/*/SKILL.md`

**Step 1: Check read/write scope**

Verify every migrated skill only references canonical or explicitly allowed projection files.

**Step 2: Check policy consistency**

Verify branch governance, archive policy, and human-gating rules are not rewritten differently across skills.

**Step 3: Check testing coverage**

Verify each migrated skill has a corresponding RED/GREEN scenario in the baseline scenario doc.

**Step 4: Commit**

Commit target: `docs: verify v2 critical skill migration consistency`
