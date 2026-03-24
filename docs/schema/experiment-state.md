# Experiment State Schema

## Purpose

Experiment State describes the validation lifecycle for one `idea x branch` line.

It answers:

- what is currently being validated
- which anchor is bound
- how many iterations have run
- what the latest evidence says
- what drift and judge currently think
- what should happen next

## Non-Goals

Experiment State does not store:

- project-wide steering state
- long-running orchestration progress
- cross-project lessons
- full raw result payloads

## Primary File Views

- `projects/<slug>/experiment-memory.md` - human-facing experiment view
- `projects/<slug>/results.tsv` - raw evidence ledger
- `projects/<slug>/plans/<idea>/anchor.md` - immutable hypothesis evidence
- `projects/<slug>/decision-tree.md` - branch comparison context

## Required Fields

| Field | Type | Description | Primary Consumer |
|------|------|-------------|------------------|
| `experiment_id` | id | stable experiment-line identity | all layers |
| `idea_id` | id | owning idea | Claude |
| `branch_id` | id | current branch identity | Claude |
| `status` | enum | lifecycle state for this experiment line | Claude, dashboard |
| `anchor_path` | path | bound anchor file | Claude, audit |
| `anchor_version` | string | anchor version or variant label | Claude |
| `iteration_count` | integer | completed iteration count | Claude, judge |
| `latest_result_ref` | ref/null | latest results ledger reference | Claude, dashboard |
| `latest_analysis_ref` | ref/null | latest analysis block reference | Claude |
| `latest_drift_score` | number/null | latest drift score | Claude, dashboard |
| `latest_drift_decision` | enum/null | latest drift decision | Claude |
| `latest_judge_verdict` | enum/null | latest judge verdict | Claude |
| `success_criteria_status` | enum | current success state | Claude |
| `human_review_required` | boolean | whether human review is required | operator |
| `archive_recommended` | boolean | whether archive is recommended | Claude |
| `next_experiment_action` | enum | next recommended experiment action | Claude |
| `last_updated` | timestamp | latest refresh time | all views |

## Optional Fields

| Field | Type | Description |
|------|------|-------------|
| `parent_branch_id` | id/null | parent branch when forked |
| `judge_confidence` | enum/null | confidence attached to latest judge verdict |
| `notes_ref` | ref/null | pointer to extra diagnostic notes |

## Enums

### `status`

- `planned`
- `anchored`
- `running`
- `analyzed`
- `drifted`
- `judged`
- `archived`
- `invalidated`

### `latest_drift_decision`

- `consistent`
- `drift-detected`
- `anchor-violation`
- `red-line`

### `latest_judge_verdict`

- `pass`
- `tweak`
- `rethink`
- `archive`

### `success_criteria_status`

- `met`
- `near-miss`
- `unmet`
- `invalidated`
- `unknown`

### `next_experiment_action`

- `run-first-experiment`
- `rerun`
- `tweak-mutable-vars`
- `branch`
- `rethink`
- `archive`
- `phase2-ready`
- `wait-human`

## Evidence Rule

No meaningful verdict should exist without a traceable evidence path:

- `anchor_path`
- `latest_result_ref`
- `latest_analysis_ref`

## View Design Rule

`experiment-memory.md` should combine:

- one current snapshot block
- structured history tables
- latest analysis detail block
- completed experiment-line summary table

It should not become the only storage location for raw experiment results.
