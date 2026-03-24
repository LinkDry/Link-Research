# Run State Schema

## Purpose

Run State tracks one recoverable execution instance.

Examples:

- `overnight phase1`
- `overnight phase2`
- long review loops
- resumed execution after interruption

It answers:

- what run is active
- what step is currently executing
- what already completed
- why the run paused or failed
- whether the run can safely resume

## Non-Goals

Run State does not store:

- project-wide research history
- experiment scientific interpretation
- cross-project lessons
- full raw result ledgers

## Primary File View

- `projects/<slug>/review-state.json`

## Required Fields

| Field | Type | Description | Primary Consumer |
|------|------|-------------|------------------|
| `run_id` | id | stable run identity | all layers |
| `run_type` | enum | execution mode | Claude, dashboard |
| `project_id` | id | owning project | all layers |
| `phase` | enum | phase covered by this run | Claude |
| `target_id` | id/null | main target idea, paper, or experiment | Claude |
| `status` | enum | current run lifecycle status | all layers |
| `started_at` | timestamp | run start time | dashboard |
| `updated_at` | timestamp | latest status update | dashboard |
| `current_step_index` | integer | active step index | Claude |
| `current_step_name` | string | active step name | operator |
| `steps` | array | structured list of run steps | Claude, dashboard |
| `resume_safe` | boolean | whether resuming is allowed | Claude |
| `decision_mode` | enum | current decision handling mode | Claude |
| `human_attention` | enum | whether operator attention is needed | dashboard |
| `errors` | array | recorded run errors | Claude |
| `warnings` | array | recorded run warnings | Claude |

## Optional Fields

| Field | Type | Description |
|------|------|-------------|
| `finished_at` | timestamp/null | finish time when closed |
| `blocking_reason` | string/null | current blocking reason |
| `decision_type` | enum/null | current decision type |
| `decision_options` | array | structured options for operator review |
| `artifacts` | array | run-generated artifact refs |
| `summary` | string/null | compact run summary |

## Enums

### `run_type`

- `phase1-overnight`
- `phase2-overnight`
- `review-loop`
- `manual-resume`
- `support`

### `status`

- `pending`
- `running`
- `paused`
- `waiting-human`
- `failed`
- `cancelled`
- `completed`

### `step.status`

- `pending`
- `in-progress`
- `completed`
- `skipped`
- `failed`
- `cancelled`
- `budget-skipped`

### `decision_mode`

- `auto`
- `auto-report`
- `human-gated`

### `human_attention`

- `none`
- `async-review`
- `required-now`

## Step Structure

Each `steps[]` entry should contain:

- `index`
- `name`
- `status`
- `started_at`
- `finished_at`
- `input_ref`
- `output_ref`
- `notes`

## Resume Rule

A run is resumable only if:

- state file is internally consistent
- current step is known
- completed steps are clearly marked
- any in-progress step can be safely re-run

## View Design Rule

`review-state.json` should remain machine-oriented and compactly parseable.

Do not replace structured fields with long freeform text.

