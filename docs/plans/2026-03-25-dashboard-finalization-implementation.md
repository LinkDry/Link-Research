# Dashboard Finalization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Finalize the V2 dashboard product surface by adding a repo-local portfolio overview and lint coverage for stale live project dashboards.

**Architecture:** Keep per-project dashboards in `projects/<slug>/workspace/` as refreshable derived views, and add a repo-local portfolio overview under `.link-research/dashboard/` so multi-project operators have a clean landing page without polluting canonical project state. Extend harness lint to detect stale live dashboard projections while preserving stricter error semantics for the template dashboard fixture.

**Tech Stack:** Python 3.12 CLI, pytest, static HTML/CSS, JSON projections, Markdown docs

---

### Task 1: Add RED Tests For Portfolio Dashboard And Live Dashboard Lint

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `tests/test_harness_lint.py`
- Modify: `tests/test_project_ops.py`
- Modify: `tests/test_dashboard_renderer.py`

**Step 1: Write the failing tests**

Cover:

- `refresh-dashboard --all` writes a repo-local portfolio HTML
- portfolio render includes current-project marker and summary cards
- harness lint warns when a live project dashboard-data.json drifts from canonical state

**Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_cli.py tests/test_harness_lint.py tests/test_project_ops.py tests/test_dashboard_renderer.py -q
```

Expected: FAIL due to missing portfolio renderer and missing live-dashboard lint rule.

**Step 3: Write minimal implementation**

Add only the smallest pieces required to satisfy the new portfolio and lint behavior.

**Step 4: Run tests to verify they pass**

Run:

```powershell
pytest tests/test_cli.py tests/test_harness_lint.py tests/test_project_ops.py tests/test_dashboard_renderer.py -q
```

Expected: PASS

**Step 5: Commit**

```powershell
git add tests tools
git commit -m "feat: add portfolio dashboard and live dashboard lint"
```

### Task 2: Document The Final Dashboard Surface

**Files:**
- Modify: `README.md`
- Modify: `docs/guides/dashboard-usage.md`

**Step 1: Write the failing doc expectations**

Use existing CLI/doc tests or add small assertions so the docs mention:

- repo-local portfolio output
- why it lives under `.link-research/dashboard/`
- how `refresh-dashboard --all` differs from per-project refresh

**Step 2: Run tests to verify they fail**

Run:

```powershell
pytest tests/test_cli.py -q
```

Expected: FAIL

**Step 3: Write minimal implementation**

Document the portfolio workflow without adding unrelated commands.

**Step 4: Run tests to verify they pass**

Run:

```powershell
pytest tests/test_cli.py -q
```

Expected: PASS

**Step 5: Commit**

```powershell
git add README.md docs/guides/dashboard-usage.md tests/test_cli.py
git commit -m "docs: finalize dashboard workflow docs"
```

### Task 3: Verify And Ship The Finalization Batch

**Files:**
- Review: `tools/*.py`
- Review: `tests/*.py`
- Review: `README.md`
- Review: `docs/guides/dashboard-usage.md`

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

**Step 3: Verify patch cleanliness**

Run:

```powershell
git diff --check
git status --short --branch
```

Expected: only intended files are modified before final commit.

**Step 4: Commit and push**

Run:

```powershell
git add README.md docs/guides/dashboard-usage.md docs/plans/2026-03-25-dashboard-finalization-implementation.md tools tests
git commit -m "feat: finalize dashboard operator surface"
git push origin link-research-v2-main
```

Expected: the final dashboard/operator surface is recoverable on GitHub.
