# Operator Workflow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve first-time usability and minimal recovery by adding an operator workflow guide, a recovery guide, and a `current-project` CLI command backed by canonical state.

**Architecture:** Keep canonical state in existing project files. Add human-facing guidance under `docs/guides/` and a lightweight `current-project` command that summarizes the selected project from runtime pointer plus canonical state files.

**Tech Stack:** Markdown docs, Python 3.12 CLI, pytest

---

### Task 1: Add Operator Workflow Docs

**Files:**
- Create: `docs/guides/phase1-quickstart.md`
- Create: `docs/guides/recovery-and-resume.md`
- Modify: `README.md`
- Test: `tests/test_cli.py`

**Step 1: Write the failing tests**

Assert:

- README links to the workflow guides
- README mentions the new `current-project` command
- the guide files exist

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Add concise but real operator guidance for:

- first-time project setup
- Phase 1 bootstrap launch
- interruption and resume checks

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -q`
Expected: PASS for the new documentation expectations, with any remaining failures coming from the missing CLI command.

**Step 5: Commit**

```bash
git add README.md docs/guides tests/test_cli.py
git commit -m "docs: add operator workflow guides"
```

### Task 2: Add Current Project Status Helpers

**Files:**
- Modify: `tools/project_state.py`
- Modify: `tools/project_ops.py`
- Test: `tests/test_project_state.py`
- Test: `tests/test_project_ops.py`

**Step 1: Write the failing tests**

Cover:

- loading the current project from runtime pointer
- building a compact current-project summary from canonical files
- generating a suggested next action hint or prompt

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_project_state.py tests/test_project_ops.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Add helpers to:

- resolve the selected current project
- load canonical summary state
- compute a compact operator-facing status payload

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_project_state.py tests/test_project_ops.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/project_state.py tools/project_ops.py tests/test_project_state.py tests/test_project_ops.py
git commit -m "feat: add current project status helpers"
```

### Task 3: Add `current-project` CLI Command

**Files:**
- Modify: `tools/link_research_cli.py`
- Test: `tests/test_cli.py`

**Step 1: Write the failing tests**

Cover:

- `current-project` with a selected project
- `current-project` with no project selected
- output includes phase, status, next action, and a suggested prompt

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -q`
Expected: FAIL

**Step 3: Write minimal implementation**

Add a `current-project` subcommand that prints:

- selected project slug
- project title
- phase and status
- active idea and branch
- current run status when present
- next action
- suggested next Claude prompt

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/link_research_cli.py tests/test_cli.py
git commit -m "feat: add current-project operator command"
```

### Task 4: Full Verification

**Files:**
- Review: `README.md`
- Review: `docs/guides/*.md`
- Review: `tools/*.py`
- Review: `tests/*.py`

**Step 1: Run the full test suite**

Run: `pytest -q`
Expected: PASS

**Step 2: Run harness lint**

Run: `python -m tools.link_research_cli harness-lint`
Expected: `0 errors, 0 warnings`

**Step 3: Run patch verification**

Run: `git diff --check`
Expected: no output

**Step 4: Confirm git status**

Run: `git status --short --branch`
Expected: only intentional changes before final commit, then clean after commit

**Step 5: Commit**

```bash
git add README.md docs/guides tools tests
git commit -m "feat: add operator workflow and recovery surface"
```
