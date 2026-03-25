# Codex Review Integration Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Repair the local Codex sqlite warning without breaking working review calls, and expand advisory GPT review to the requested pipeline stages while documenting the real Claude/Codex setup for future users.

**Architecture:** Keep the runtime repair minimal and local by backing up the current sqlite files and deleting only the stale migration records that no longer exist in Codex 0.115.0. In the repo, extend existing skill contracts with the same advisory-only pattern already used by `judge` and `drift-detector`, then document the actual user-scope Claude MCP plus Codex custom-provider setup in the README and protect it with focused tests.

**Tech Stack:** Python sqlite3, PowerShell, Markdown skill contracts, pytest

---

### Task 1: Repair Local Codex Sqlite Metadata

**Files:**
- Modify: `C:\Users\SchultzDjango\.codex\state_5.sqlite`
- Modify: `C:\Users\SchultzDjango\.codex\logs_1.sqlite`
- Create: backup sqlite files under `C:\Users\SchultzDjango\.codex\`

**Step 1: Create consistent backups**

Use sqlite backup API to snapshot `state_5.sqlite` and `logs_1.sqlite` before any mutation.

**Step 2: Apply the minimal metadata repair**

Delete only:
- migration `20` from `state_5.sqlite._sqlx_migrations`
- migration `2` from `logs_1.sqlite._sqlx_migrations`

Do not rebuild tables or drop user data.

**Step 3: Verify**

Run:

```powershell
codex exec -m gpt-5.4 "Reply with exactly: GPT54_OK"
```

Expected:
- command succeeds
- migration warnings disappear
- provider remains `custom`

### Task 2: Extend Advisory GPT Review To Three More Skills

**Files:**
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\skills\novelty-check\SKILL.md`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\skills\experiment-plan\SKILL.md`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\skills\phase2-publish\SKILL.md`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\docs\views\novelty-check-view.md`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\docs\views\experiment-plan-view.md`

**Step 1: Add the advisory review contract**

Mirror the existing pattern used by `judge` and `drift-detector`:
- only when Codex MCP is available
- advisory only
- conservative posture wins on disagreement
- record the outcome in the owned artifact

**Step 2: Place each review at the right stage**

- `novelty-check`: critique idea quality, novelty overclaim risk, and why the selected line is best
- `experiment-plan`: critique falsifiability, baselines, metrics, confounders, and execution risk
- `phase2-publish`: critique claims-evidence traceability, framing accuracy, and publication-time integrity gaps

**Step 3: Align artifact docs**

Add optional cross-model review sections to the view docs where needed so skill behavior and artifact contracts stay aligned.

### Task 3: Document Real Claude/Codex/GPT Setup

**Files:**
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\README.md`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\docs\guides\phase1-quickstart.md`

**Step 1: Document user-scope setup**

Explain that:
- Claude remains the primary operator
- GPT review depends on user-scope Codex plus Claude MCP setup
- the repo alone does not ship secrets or machine-specific config

**Step 2: Add concrete setup and verification commands**

Include:
- `claude mcp add codex -s user -- codex mcp-server`
- `claude mcp list`
- `codex exec -m gpt-5.4 "Reply with exactly: GPT54_OK"`

**Step 3: Document current GPT review touchpoints**

List the actual pipeline stages where GPT advisory review is expected after this change.

### Task 4: Add Focused Regression Tests And Verify

**Files:**
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\tests\test_cli.py`
- Modify: `C:\Users\SchultzDjango\Desktop\Files\Projects\ClaudeCode\tests\test_phase1_skill_surface.py`

**Step 1: Add documentation assertions**

Check that README mentions:
- user-scope Codex MCP setup
- `claude mcp add codex -s user -- codex mcp-server`
- `codex exec -m gpt-5.4`

**Step 2: Add skill-surface assertions**

Check that:
- `novelty-check`
- `experiment-plan`
- `phase2-publish`

all contain the expected advisory cross-model review marker.

**Step 3: Run verification**

Run:

```powershell
pytest -q
python -m tools.link_research_cli harness-lint
```

Expected:
- tests pass
- harness lint reports `0 errors, 0 warnings`
