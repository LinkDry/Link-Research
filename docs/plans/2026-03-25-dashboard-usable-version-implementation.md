# Dashboard Usable Version Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver the first practical V2 dashboard surface by deriving richer dashboard data from canonical state, adding repo-local refresh/render commands, and documenting the operator workflow for using the dashboard safely.

**Architecture:** Keep canonical truth in `STATE.md`, `experiment-memory.md`, `review-state.json`, and Memory files. Expand the derived dashboard payload to include memory and decision posture, then render a static but refreshable HTML shell per project. The CLI remains the operator entrypoint and owns regeneration; the dashboard remains read-only and non-canonical.

**Tech Stack:** Python 3.12 CLI, pytest, JSON projections, static HTML/CSS/JS, Markdown docs

---

### Task 1: Expand Dashboard Projection And Memory Parsing

**Files:**
- Modify: `tools/project_state.py`
- Modify: `tests/test_project_state.py`
- Modify: `tests/test_project_ops.py`
- Modify: `tests/test_harness_lint.py`

**Step 1: Write the failing tests**

Cover:

- parsing recent lessons, persistent patterns, capability gaps, and failure cases from Memory files
- deriving dashboard payloads that expose decision posture and non-empty memory summaries
- keeping template dashboard data aligned with canonical template files

**Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_project_state.py tests/test_project_ops.py tests/test_harness_lint.py -q
```

Expected: FAIL due to missing memory parsing helpers and richer dashboard projection fields.

**Step 3: Write minimal implementation**

Add helpers to:

- parse the Markdown table sections used by `memory/lessons-learned.md`
- parse `memory/failure-library.md`
- project a richer dashboard payload with:
  - project steering posture
  - active experiment snapshot
  - live run posture
  - recent lessons, active patterns, open capability gaps, and recent failure warnings

**Step 4: Run tests to verify they pass**

Run:

```powershell
pytest tests/test_project_state.py tests/test_project_ops.py tests/test_harness_lint.py -q
```

Expected: PASS

**Step 5: Commit**

```powershell
git add tools/project_state.py tests/test_project_state.py tests/test_project_ops.py tests/test_harness_lint.py
git commit -m "feat: enrich dashboard projection with memory state"
```

### Task 2: Add Dashboard Refresh And Render Tooling

**Files:**
- Modify: `tools/project_ops.py`
- Modify: `tools/link_research_cli.py`
- Create: `tools/dashboard_renderer.py`
- Modify: `tests/test_cli.py`
- Create: `tests/test_dashboard_renderer.py`

**Step 1: Write the failing tests**

Cover:

- refreshing a selected project dashboard from canonical files
- rendering `projects/<slug>/workspace/dashboard.html`
- CLI surface for `refresh-dashboard`
- optional `--slug`, `--current`, and `--all` routing

**Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_cli.py tests/test_dashboard_renderer.py -q
```

Expected: FAIL due to missing command and renderer.

**Step 3: Write minimal implementation**

Add:

- a small HTML renderer with embedded JSON payload
- a project helper that regenerates `dashboard-data.json` and `dashboard.html`
- a CLI command:
  - `python -m tools.link_research_cli refresh-dashboard --current`

**Step 4: Run tests to verify they pass**

Run:

```powershell
pytest tests/test_cli.py tests/test_dashboard_renderer.py -q
```

Expected: PASS

**Step 5: Commit**

```powershell
git add tools/project_ops.py tools/link_research_cli.py tools/dashboard_renderer.py tests/test_cli.py tests/test_dashboard_renderer.py
git commit -m "feat: add dashboard refresh and render tooling"
```

### Task 3: Document The Dashboard Operator Path

**Files:**
- Modify: `README.md`
- Create: `docs/guides/dashboard-usage.md`
- Modify: `tests/test_cli.py`

**Step 1: Write the failing tests**

Assert:

- README links the dashboard guide
- README mentions `refresh-dashboard`
- the guide exists and explains canonical-vs-derived usage

**Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_cli.py -q
```

Expected: FAIL

**Step 3: Write minimal implementation**

Document:

- how to refresh the dashboard
- where the HTML file is written
- why the dashboard is derived and read-only
- how this fits into the current-project and recovery workflow

**Step 4: Run tests to verify they pass**

Run:

```powershell
pytest tests/test_cli.py -q
```

Expected: PASS

**Step 5: Commit**

```powershell
git add README.md docs/guides/dashboard-usage.md tests/test_cli.py
git commit -m "docs: add dashboard usage guide"
```

### Task 4: Verify And Ship The Usable-Version Batch

**Files:**
- Review: `README.md`
- Review: `docs/guides/dashboard-usage.md`
- Review: `tools/*.py`
- Review: `tests/*.py`
- Review: `projects/_template/workspace/dashboard-data.json`

**Step 1: Run the full test suite**

Run:

```powershell
pytest -q
```

Expected: PASS

**Step 2: Run harness lint**

Run:

```powershell
python -m tools.link_research_cli harness-lint
```

Expected: `0 errors, 0 warnings`

**Step 3: Refresh the template dashboard and verify the patch**

Run:

```powershell
python -m tools.link_research_cli refresh-dashboard --slug _template
git diff --check
git status --short --branch
```

Expected:

- the template dashboard projection matches canonical template state
- no patch-formatting issues
- only intended files are modified before final commit

**Step 4: Commit and push**

Run:

```powershell
git add README.md docs/guides/dashboard-usage.md docs/plans/2026-03-25-dashboard-usable-version-implementation.md tools tests projects/_template/workspace/dashboard-data.json
git commit -m "feat: add usable dashboard workflow"
git push origin link-research-v2-main
```

Expected: the usable-version batch is recoverable on GitHub.
