# Project State Schema

## Purpose

Project State defines the current steering context for one research project.

It answers:

- which phase the project is in
- which idea and branch are currently primary
- what should happen next
- whether human attention is required
- what risks or blockers currently exist

## Non-Goals

Project State does not store:

- detailed experiment history
- raw results
- full branch comparison data
- long-running step details
- cross-project memory content

## Primary File Views

- `projects/<slug>/STATE.md` - primary human-facing view
- dashboard top summary - visual projection

## Required Fields

| Field | Type | Description | Primary Consumer |
|------|------|-------------|------------------|
| `project_id` | id | stable project identity | all layers |
| `phase` | enum | current top-level research phase | Claude, dashboard |
| `project_status` | enum | current project condition | Claude, dashboard |
| `active_idea_id` | id/null | currently primary idea, or `null` when none is selected | Claude |
| `active_branch_id` | id/null | currently primary branch, or `null` when none is selected | Claude |
| `current_run_id` | id/null | current active run if any | Claude, dashboard |
| `next_action` | string | next recommended action | Claude, operator |
| `decision_mode` | enum | how the next decision should be handled | Claude |
| `human_attention` | enum | whether the human should look now | dashboard |
| `risk_level` | enum | current overall steering risk | dashboard |
| `last_completed_skill` | string | latest completed skill | Claude |
| `last_updated` | timestamp | latest refresh time | all views |
| `blockers` | list | active blockers or empty list | Claude, operator |

## Optional Fields

| Field | Type | Description |
|------|------|-------------|
| `project_title` | string | human-readable project title |
| `active_paper_id` | id/null | current paper object in phase 2 |
| `decision_type` | enum/null | current decision category |
| `decision_options_ref` | ref/null | pointer to the canonical decision artifact that holds detailed options |

## Enums

### `phase`

- `phase0`
- `phase1`
- `phase2`
- `paused`
- `archived`

## Phase Transition Rule

Project State remains in `phase1` after a Phase 1 PASS until a Phase 2 workflow actually starts.

Use `next_action` plus Experiment State `next_experiment_action: phase2-ready` to express readiness before the transition happens.

### `project_status`

- `idle`
- `running`
- `waiting-human`
- `blocked`
- `invalidated`
- `completed`

### `decision_mode`

- `auto`
- `auto-report`
- `human-gated`

### `human_attention`

- `none`
- `async-review`
- `required-now`

### `risk_level`

- `low`
- `medium`
- `high`
- `critical`

### `decision_type`

- `branch-decision`
- `phase2-handoff`
- `archive-review`
- `integrity-review`
- `resource-review`

## Update Triggers

Project State should be updated when:

- phase changes
- primary idea changes
- primary branch changes
- a run starts or stops
- a human-gated decision is entered or cleared
- a critical blocker appears or clears

## View Design Rule

`STATE.md` should stay compact and operator-oriented.

Target:

- 10-15 lines
- no long explanations
- no duplicated experiment history
