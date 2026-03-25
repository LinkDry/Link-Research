# Project Tooling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the first executable V2 project tooling: live project creation, current-project selection, project listing, and a narrow but high-signal harness lint.

**Architecture:** Add a small Python CLI under `tools/` with shared helpers for Markdown state parsing, template instantiation, dashboard projection generation, runtime pointer handling, and lint reporting. Keep canonical state in project files and keep the runtime pointer local and ignored.

**Tech Stack:** Python 3.12, argparse, pathlib, json, pytest

---

### Task 1: Add Tooling Skeleton And Ignore Rules

**Files:**
- Create: `.gitignore`
- Create: `tools/__init__.py`
- Create: `tests/__init__.py`

**Step 1: Write the failing tests**

Create tests that expect:

- `.link-research/runtime.json` to be ignored by git
- Python modules under `tools/` to be importable

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli_smoke.py -q`
Expected: FAIL because the files do not exist yet.

**Step 3: Write minimal implementation**

- add ignore rules for `.link-research/` and Python cache files
- create minimal package markers under `tools/` and `tests/`

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli_smoke.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add .gitignore tools/__init__.py tests/__init__.py tests/test_cli_smoke.py
git commit -m "chore: add v2 tooling skeleton"
```

### Task 2: Implement Shared Project Parsing And Dashboard Projection Helpers

**Files:**
- Create: `tools/project_state.py`
- Test: `tests/test_project_state.py`

**Step 1: Write the failing tests**

Cover:

- parsing key-value fields from `STATE.md`
- parsing the active snapshot table from `experiment-memory.md`
- building the derived dashboard payload from canonical template files

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_project_state.py -q`
Expected: FAIL because the module does not exist yet.

**Step 3: Write minimal implementation**

Add helpers to:

- parse bullet-list field blocks
- parse the `Active Line Snapshot` table
- load `review-state.json`
- build the derived `dashboard-data.json` structure

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_project_state.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/project_state.py tests/test_project_state.py
git commit -m "feat: add v2 project state helpers"
```

### Task 3: Implement Project Runtime And Instantiation Helpers

**Files:**
- Create: `tools/project_ops.py`
- Test: `tests/test_project_ops.py`

**Step 1: Write the failing tests**

Cover:

- slug validation
- creating a new project without copying template-only example artifacts
- rewriting project id, title, slug paths, and timestamps
- writing an aligned derived dashboard payload
- storing and loading the runtime current-project pointer

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_project_ops.py -q`
Expected: FAIL because the module does not exist yet.

**Step 3: Write minimal implementation**

Implement helpers to:

- validate slugs
- create live project directories
- instantiate core live files from `projects/_template/`
- skip `_template-*` reference files and sample artifact fixtures
- write `.link-research/runtime.json`

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_project_ops.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/project_ops.py tests/test_project_ops.py
git commit -m "feat: add v2 project instantiation helpers"
```

### Task 4: Implement CLI Subcommands

**Files:**
- Create: `tools/link_research_cli.py`
- Test: `tests/test_cli.py`

**Step 1: Write the failing tests**

Cover:

- `new-project`
- `list-projects`
- `switch-project`
- human-readable output
- non-zero exit on invalid usage

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -q`
Expected: FAIL because the CLI module does not exist yet.

**Step 3: Write minimal implementation**

Implement argparse subcommands that call the shared helpers and print compact operator-friendly output.

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/link_research_cli.py tests/test_cli.py
git commit -m "feat: add v2 operator cli"
```

### Task 5: Implement Harness Lint Core

**Files:**
- Create: `tools/harness_lint.py`
- Test: `tests/test_harness_lint.py`

**Step 1: Write the failing tests**

Cover:

- missing required repo files
- mismatched dashboard projection
- write vs must-not-write overlap in a skill contract
- unresolved delegated skill reference
- invalid runtime current-project pointer

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_harness_lint.py -q`
Expected: FAIL because the lint module does not exist yet.

**Step 3: Write minimal implementation**

Implement a lint runner that emits structured findings with severities and returns non-zero when errors are present.

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_harness_lint.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/harness_lint.py tests/test_harness_lint.py
git commit -m "feat: add v2 harness lint"
```

### Task 6: Wire CLI To Harness Lint And Document Usage

**Files:**
- Modify: `tools/link_research_cli.py`
- Create: `README.md`
- Test: `tests/test_cli.py`

**Step 1: Write the failing tests**

Add coverage for:

- `harness-lint`
- usage examples exposed in README-friendly command form

**Step 2: Run tests to verify they fail**

Run: `pytest tests/test_cli.py -q`
Expected: FAIL on the new lint command expectations.

**Step 3: Write minimal implementation**

- add the lint subcommand
- document quick-start usage for Claude or a human operator

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_cli.py -q`
Expected: PASS

**Step 5: Commit**

```bash
git add tools/link_research_cli.py README.md tests/test_cli.py
git commit -m "docs: add v2 tooling quickstart"
```

### Task 7: Full Verification

**Files:**
- Review: `tools/*.py`
- Review: `tests/*.py`
- Review: `README.md`

**Step 1: Run the full test suite**

Run: `pytest -q`
Expected: PASS

**Step 2: Run the harness lint on the repository**

Run: `python -m tools.link_research_cli harness-lint`
Expected: command completes with structured findings. If it reports repo errors, fix or explicitly document them before claiming completion.

**Step 3: Run patch-format verification**

Run: `git diff --check`
Expected: no output

**Step 4: Confirm git status**

Run: `git status --short --branch`
Expected: only intentional tracked changes before final commit, then clean after commit

**Step 5: Commit**

```bash
git add README.md tools tests .gitignore
git commit -m "feat: add v2 project tooling and harness lint"
```
