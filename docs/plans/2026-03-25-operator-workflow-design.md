# Link-Research V2 Operator Workflow Design

**Goal:** Make V2 meaningfully easier to use by documenting the real operator path from project creation into Phase 1 bootstrap while also adding a minimal recovery surface for interrupted runs.

## Problem

V2 now has:

- canonical state files
- executable project tooling
- a complete Phase 1 skill surface
- a harness-level lint guardrail

But the actual usage story is still underspecified.

Right now a new operator can create a project, yet the repo still does not clearly answer:

- what to do immediately after `new-project`
- how to fill `project-brief.md` for the two intake modes
- how Claude should be prompted to begin Phase 1 bootstrap
- how to quickly recover after interruption and identify the current project posture

This makes the system structurally strong but still harder to adopt than it should be.

## Scope Choice

This batch follows the agreed “1.5” strategy:

- fully document the first-time path from zero to Phase 1 start
- also add the smallest useful recovery surface for existing projects

It does **not** try to fully solve every long-horizon operations problem in one step.

## Approaches Considered

### Option 1: Docs Only

Write a stronger README and one operator playbook, but do not add any new CLI surface.

Pros:

- low code cost
- fast to ship

Cons:

- recovery still depends on manually opening files
- CLI remains blind to the operator’s current project posture

### Option 2: CLI Only

Add a `current-project` or `status` command without improving the written operator workflow.

Pros:

- immediately useful for interrupted sessions
- strong support for Claude and human operators

Cons:

- first-time users still lack a coherent documented path
- commands alone do not explain the intended Phase 1 sequence

### Option 3: Hybrid Docs + Minimal Recovery CLI

Add:

- a real operator workflow guide
- a recovery guide
- a `current-project` CLI command that summarizes the current canonical posture and suggests the next Claude-facing move

Recommended because it gives a concrete operator experience without expanding the tooling surface too aggressively.

## Chosen Design

Use Option 3.

## User-Facing Additions

### 1. README Upgrade

The README should move from “tooling smoke test” to “real entrypoint.”

It should cover:

- what Link-Research V2 is for
- the first 5 minutes of setup
- links to the more detailed workflow guides
- the most important commands

### 2. Phase 1 Quickstart Guide

Add a focused operator guide that explains:

- create a project
- switch to it
- fill `project-brief.md`
- choose between `direction-search` and `seed-papers`
- ask Claude to begin Phase 1 bootstrap
- inspect the right canonical files while work proceeds

### 3. Recovery Guide

Add a short guide that explains:

- how to identify the current project
- how to inspect current phase, active line, and current run
- how to know whether the next step is bootstrap, resume, drift, judge, archive, or Phase 2

### 4. `current-project` CLI Command

Add:

`python -m tools.link_research_cli current-project`

It should read:

- `.link-research/runtime.json`
- `projects/<slug>/STATE.md`
- `projects/<slug>/experiment-memory.md`
- `projects/<slug>/review-state.json`

And print a compact operator-facing summary:

- current slug and title
- phase and project status
- active idea and branch
- current run id plus run status when relevant
- next action
- a suggested next Claude prompt or recovery action

## Prompt Guidance Model

The CLI should not try to automate Claude itself.

Instead it should produce a suggested prompt or action hint based on canonical state, for example:

- if no current project is selected:
  - tell the operator to run `switch-project`
- if `phase0` or early bootstrap:
  - suggest asking Claude to read `project-brief.md` and begin Phase 1 bootstrap
- if a paused or running run exists:
  - suggest asking Claude to inspect `review-state.json` and resume safely
- if `next_experiment_action: phase2-ready`:
  - suggest starting the approved Phase 2 workflow

This keeps the CLI small while making recovery materially easier.

## Non-Goals

- no new orchestration engine in this batch
- no auto-prompt execution
- no dashboard frontend implementation yet
- no full multi-project scheduling layer

## Expected Outcome

After this batch:

- a new operator can realistically get from repo clone to Phase 1 start
- an interrupted operator can quickly recover the current project posture
- the repo has a clearer human-facing usage story, not just an internal schema story
