# Object-to-File Mapping Rules

This document defines how Link-Research V2 state objects map onto repository files.

## Core Rule

In V2, each state object has one canonical primary view file for persistence.

Other files may exist as:

- secondary evidence views
- derived projections
- historical archives

Those files must not become the hidden source of truth.

## File Categories

### Primary View

The main persisted representation of one owner object.

Rules:

- exactly one owner object
- may be read and updated directly by skills
- must be sufficient to recover the current high-level state for that object

### Secondary Evidence View

A file owned by the same object, but optimized for evidence, immutability, or history.

Rules:

- still tied to one owner object
- may be append-only or write-once
- must not contradict the primary view

### Derived Projection

A generated file that aggregates data from more than one object.

Rules:

- not a source of truth
- may be regenerated at any time
- must not be manually edited as if it were canonical state

### Historical Archive

A durable record of prior states or completed lines.

Rules:

- may summarize multiple objects
- must point back to canonical IDs, paths, and evidence refs
- must not replace the active primary view

## Mapping Matrix

| File | Category | Primary Owner | Purpose | Update Policy |
|------|----------|---------------|---------|---------------|
| `projects/<slug>/STATE.md` | primary view | Project State | operator-facing steering summary | overwrite in place |
| `projects/<slug>/experiment-memory.md` | primary view | Experiment State | current validation snapshot plus structured history | overwrite snapshot sections, append history rows |
| `projects/<slug>/review-state.json` | primary view | Run State | machine-readable controller for resumable execution | atomic structured overwrite |
| `memory/lessons-learned.md` | primary view | Memory State | human-readable long-term learning summary | append, compact, promote |
| `projects/<slug>/results.tsv` | secondary evidence view | Experiment State | append-only results ledger | append only |
| `projects/<slug>/plans/<idea>/anchor.md` | secondary evidence view | Experiment State | immutable anchor evidence | write once per anchor version |
| `projects/<slug>/decision-tree.md` | secondary evidence view | Experiment State | branch governance history | append and summarize |
| `memory/archive/*.md` | historical archive | Memory State | compacted global lesson history | append and rotate |
| `projects/<slug>/archive/*.md` | historical archive | Experiment State | completed branch or experiment case record | append new archive record |
| `projects/<slug>/workspace/dashboard-data.json` | derived projection | derived from Project, Experiment, Run, Memory | dashboard payload for UI shell | regenerate only |

## Source-of-Truth Rules

1. Primary views are canonical for current active state.
2. Secondary evidence views hold details that primary views should reference, not duplicate.
3. Derived projections may summarize multiple objects but cannot introduce new facts.
4. Historical archives may explain past decisions but cannot silently overwrite current active state.

## Cross-File Responsibility Rules

### `STATE.md`

- owns only current project steering summary
- may point to experiment, run, or decision files
- must not contain detailed experiment history

### `experiment-memory.md`

- owns current experiment-line snapshot and structured experiment history
- may summarize latest evidence and verdict
- must not replace `results.tsv` as the raw evidence ledger

### `review-state.json`

- owns execution control and resume semantics
- may point to artifacts and decisions
- must not contain scientific interpretation as its primary content

### `results.tsv`

- owns ledger-style result rows only
- must not become a freeform notes dump
- corrections should create new rows, not rewrite history

### `anchor.md`

- owns the locked research claim and validation intent for one branch line
- must never be rewritten to match later results
- new scientific framing requires a new anchor version or branch

### `lessons-learned.md`

- owns reusable abstractions
- must reference project archives rather than duplicate their full detail
- global lesson compaction belongs in `memory/archive/`, not project archives

## Projection Rules

`projects/<slug>/workspace/dashboard-data.json` is allowed to aggregate:

- current project steering summary from Project State
- active experiment snapshot from Experiment State
- live run progress from Run State
- recent lessons or warnings from Memory State

But it must remain:

- read-only from the perspective of workflow skills
- fully regenerable from canonical files

## Update and Conflict Rules

When two files appear to disagree:

1. trust the relevant primary view first
2. then inspect secondary evidence files
3. treat derived projections as stale until regenerated
4. treat archives as historical context, not current truth

## Future Lint Targets

Harness lint should later verify:

- every primary view has exactly one owner object
- every derived projection is marked non-canonical
- no skill writes a derived projection as if it were a primary view
- no primary field exists only in a derived file
- every archive record points back to canonical IDs and evidence refs
