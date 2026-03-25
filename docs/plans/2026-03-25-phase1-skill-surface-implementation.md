# Phase 1 Skill Surface Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add the missing six V2 Phase 1 skills plus the bootstrap artifact contracts they depend on, and verify that `overnight` no longer delegates to undefined in-repo skills.

**Architecture:** Introduce three non-canonical bootstrap artifacts under `workspace/bootstrap/`, reuse the existing `experiment-plan.md`, `results.tsv`, `config-snapshot.json`, and `analysis-report.json` contracts for the execution side, and keep canonical state updates confined to `STATE.md`, `experiment-memory.md`, and `decision-tree.md` where appropriate.

**Tech Stack:** Markdown skill contracts, Markdown artifact view contracts, pytest, repo-local harness lint

---

### Task 1: Add Bootstrap Artifact View Contracts

**Files:**
- Create: `docs/views/literature-review-view.md`
- Create: `docs/views/idea-candidates-view.md`
- Create: `docs/views/novelty-check-view.md`
- Test: `tests/test_phase1_skill_surface.py`

**Step 1: Write the failing test**

Assert the three bootstrap artifact view docs exist and expose `## Purpose` plus `## Canonical Location`.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_phase1_skill_surface.py::test_bootstrap_view_docs_exist -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Define each artifact as a durable but non-canonical bootstrap contract under `projects/<slug>/workspace/bootstrap/`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_phase1_skill_surface.py::test_bootstrap_view_docs_exist -q`
Expected: PASS

**Step 5: Commit**

```bash
git add docs/views/literature-review-view.md docs/views/idea-candidates-view.md docs/views/novelty-check-view.md tests/test_phase1_skill_surface.py
git commit -m "docs: add v2 bootstrap artifact contracts"
```

### Task 2: Add Missing Bootstrap Skills

**Files:**
- Create: `skills/literature-review/SKILL.md`
- Create: `skills/idea-creator/SKILL.md`
- Create: `skills/novelty-check/SKILL.md`
- Test: `tests/test_phase1_skill_surface.py`

**Step 1: Write the failing test**

Assert the three skill files exist and include the standard contract sections.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_phase1_skill_surface.py::test_missing_phase1_skill_files_exist_with_standard_contract_sections -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Author the three bootstrap skill contracts with:

- explicit read/write ownership
- conservative STATE updates
- durable bootstrap artifact outputs

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_phase1_skill_surface.py::test_missing_phase1_skill_files_exist_with_standard_contract_sections -q`
Expected: PASS for the new skills, with remaining failures still coming from the other three missing skills

**Step 5: Commit**

```bash
git add skills/literature-review/SKILL.md skills/idea-creator/SKILL.md skills/novelty-check/SKILL.md tests/test_phase1_skill_surface.py
git commit -m "docs: add v2 bootstrap phase1 skills"
```

### Task 3: Add Missing Planning And Evidence Skills

**Files:**
- Create: `skills/experiment-plan/SKILL.md`
- Create: `skills/run-experiment/SKILL.md`
- Create: `skills/analyze-results/SKILL.md`
- Test: `tests/test_phase1_skill_surface.py`

**Step 1: Write the failing test**

Reuse the existing existence/section test so these files are still missing.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_phase1_skill_surface.py::test_missing_phase1_skill_files_exist_with_standard_contract_sections -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Author the three downstream skill contracts with:

- canonical `experiment-plan.md` authorship
- append-only evidence recording through `results.tsv`
- structured analysis output through `analysis-report.json`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_phase1_skill_surface.py::test_missing_phase1_skill_files_exist_with_standard_contract_sections -q`
Expected: PASS

**Step 5: Commit**

```bash
git add skills/experiment-plan/SKILL.md skills/run-experiment/SKILL.md skills/analyze-results/SKILL.md tests/test_phase1_skill_surface.py
git commit -m "docs: add v2 planning and evidence phase1 skills"
```

### Task 4: Clear The `overnight` Delegate Gap

**Files:**
- Review: `skills/overnight/SKILL.md`
- Review: `skills/*/SKILL.md`
- Test: `tests/test_phase1_skill_surface.py`

**Step 1: Run the failing lint expectation**

Run: `pytest tests/test_phase1_skill_surface.py::test_harness_lint_no_longer_reports_missing_delegate_skills -q`
Expected: FAIL before all six skills exist

**Step 2: Verify the implementation closes the gap**

Run: `pytest tests/test_phase1_skill_surface.py::test_harness_lint_no_longer_reports_missing_delegate_skills -q`
Expected: PASS

**Step 3: Commit**

```bash
git add skills tests
git commit -m "docs: close v2 overnight phase1 delegate gaps"
```

### Task 5: Full Verification And Self-Review

**Files:**
- Review: `docs/views/*.md`
- Review: `skills/*/SKILL.md`
- Review: `tests/*.py`

**Step 1: Run the focused test suite**

Run: `pytest tests/test_phase1_skill_surface.py -q`
Expected: PASS

**Step 2: Run the full test suite**

Run: `pytest -q`
Expected: PASS

**Step 3: Run harness lint**

Run: `python -m tools.link_research_cli harness-lint`
Expected: no `missing-delegate-skill` findings

**Step 4: Run patch verification**

Run: `git diff --check`
Expected: no output

**Step 5: Commit**

```bash
git add docs/views skills tests
git commit -m "docs: complete v2 phase1 skill surface"
```
