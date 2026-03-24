# Link-Research V2 Target Operating Model Design

**Goal:** Define the schema-first operating model for a Claude-led research steering system that remains auditable, recoverable, and learnable over long-running research programs.

**Core Positioning**

- Claude is the primary operator and conversation surface.
- Automation is on by default.
- Human intervention is reserved for high-risk, irreversible, or ethics-sensitive decisions.
- Files are durable views over explicit state objects, not the state source itself.
- Scientific integrity is enforced through anchors, evidence ledgers, drift checks, and review gates.

## Design Principles

1. Schema-first over file-first.
2. Autonomy-first, human-vetoable, ethics-gated.
3. One file, one view responsibility.
4. Branches are governed scientific variants, not ad hoc code forks.
5. Failures must be re-used as future warning signals.
6. Dashboards consume state; they never define state.

## Two-Phase Research Model

### Phase 1: Validate

- Idea generation
- Novelty filtering
- Experiment design
- Anchor locking
- Experiment execution
- Analysis
- Drift detection
- Judge verdict

### Phase 2: Publish

- Paper planning
- Writing
- Citation verification
- Compilation
- Cross-model review
- Finalization

## State Objects

### Project State

Project-level steering context:

- current phase
- active idea and branch
- current run
- next action
- human attention mode
- blockers and risk

Primary view: `projects/<slug>/STATE.md`

### Experiment State

Validation lifecycle for one `idea x branch` line:

- anchor binding
- iteration count
- latest result and analysis refs
- latest drift state
- latest judge verdict
- next experiment action

Primary view: `projects/<slug>/experiment-memory.md`

### Run State

Recoverable execution control for one long-running process:

- run type
- progress steps
- pause/resume
- waiting-human state
- errors and warnings

Primary view: `projects/<slug>/review-state.json`

### Memory State

Cross-project long-term learning:

- lessons
- persistent patterns
- capability gaps
- failure classes

Primary view: `memory/lessons-learned.md`

## File Role Summary

- `projects/<slug>/STATE.md`: compact operator-facing project summary
- `projects/<slug>/experiment-memory.md`: current experiment view plus structured history
- `projects/<slug>/review-state.json`: machine-oriented run controller
- `projects/<slug>/results.tsv`: append-only experiment evidence ledger
- `projects/<slug>/plans/<idea>/anchor.md`: immutable hypothesis anchor
- `projects/<slug>/decision-tree.md`: branch governance record
- `projects/<slug>/archive/*.md`: project-local archive and evidence history
- `memory/lessons-learned.md`: cross-project learning view
- `memory/archive/*.md`: compacted global learning history
- `projects/<slug>/workspace/dashboard-data.json`: dashboard data projection

## Branch Governance Summary

- Default active branch limit per idea: 3
- Absolute cap per idea: 5
- Branch types:
  - `tactical`: same anchor, reversible, low-cost exploration
  - `strategic`: meaningful research divergence, may require anchor variant
- Each branch must end as one of:
  - `merged`
  - `promoted`
  - `abandoned`
  - `archived`

## Failure Learning Summary

Failure must pass through this loop:

1. failure event occurs
2. project archive captures details
3. lessons extract reusable insight
4. patterns and failure classes are promoted
5. future idea generation checks similar failure signals

## Dashboard Summary

Dashboard is a command surface, not a source of truth.

- stable frontend shell
- generated `dashboard-data.json`
- primary role: steering console
- secondary roles: project overview and governance health

## Immediate Design Deliverables

1. field naming conventions
2. state object schema documents
3. object-to-file mapping rules
4. template migration targets
5. skill contract migration plan

## Non-Goals For This First Cut

- no implementation of dashboard frontend yet
- no automation runner rewrite yet
- no Obsidian integration
- no remote execution redesign yet

