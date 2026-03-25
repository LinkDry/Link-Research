# Link-Research V2 Project Tooling Design

**Goal:** Add the first executable operator tooling for V2 so Claude can instantiate, select, and lint real projects instead of depending on prose-only setup flows.

## Problem

The V2 repository now has a much cleaner schema-first contract, but it still lacks two practical abilities:

1. create a real `projects/<slug>/` instance from the canonical template without copying template noise into live state
2. detect contract drift before it spreads across skills, templates, and derived dashboard state

Without those two abilities, the system is still easy to understand on paper but hard to operate reliably over time.

## Design Constraints

- Keep canonical scientific state in the existing project files.
- Do not introduce a second hidden source of truth.
- Keep operator-local convenience state outside canonical project state.
- Prefer one lightweight repo-local toolchain over scattered ad hoc scripts.
- Make the first lint pass narrow, explicit, and high-signal.

## Approaches Considered

### Option 1: Continue Prose-Only Setup

Describe `new-project`, `switch-project`, and validation rules in docs and ask Claude to perform them manually.

Pros:

- no code to maintain
- fast in the short term

Cons:

- no repeatability
- setup remains fragile
- contract drift stays invisible until a later review

### Option 2: Several Small One-Off Scripts

Add separate scripts for project creation, listing, switching, and linting with no shared library.

Pros:

- simple to start
- each script stays small

Cons:

- duplicated parsing logic
- harder to test coherently
- encourages behavior drift between tools

### Option 3: Repo-Local Python CLI With Shared Contract Logic

Add a small Python CLI with subcommands for:

- `new-project`
- `list-projects`
- `switch-project`
- `harness-lint`

Back it with shared helpers for:

- template instantiation
- Markdown state parsing
- dashboard projection generation
- lint reporting

Recommended because it is the smallest option that still gives one coherent execution surface and one coherent place to encode repo rules.

## Chosen Design

Use Option 3.

### Tooling Surface

Create a repo-local Python package under `tools/` and invoke it with:

`python -m tools.link_research_cli <subcommand>`

This keeps the repo dependency-light, cross-platform enough for local Windows plus WSL use, and easy for Claude to call directly.

### Runtime Pointer

Store the currently selected project in a repo-local ignored file:

`.link-research/runtime.json`

This file is:

- operator convenience only
- not canonical scientific state
- safe to regenerate or clear

It should track:

- `current_project_slug`
- `current_project_path`
- `updated_at`

### `new-project`

`new-project` should not blindly copy `projects/_template/`.

Instead it should:

- create the live directory scaffold explicitly
- copy only canonical live-state files into the new project
- skip template-only example artifacts and `_template-*` reference files
- rewrite placeholder values such as:
  - `proj-template`
  - `Template Project`
  - `projects/<slug>/...`
  - initial timestamps
- regenerate the derived `workspace/dashboard-data.json` from the instantiated canonical state

This keeps live projects clean and avoids mixing fixture material with real state.

### `list-projects`

`list-projects` should enumerate live projects under `projects/`, skipping `_template`, and summarize each project from canonical state:

- slug
- project id
- project title
- phase
- status
- next action

If the runtime pointer is present, mark the current project clearly.

### `switch-project`

`switch-project` should only update the ignored runtime pointer after verifying that:

- the target slug exists
- the target project contains canonical state files

This gives Claude and the operator a stable “current project” handle without mutating project state itself.

### `harness-lint`

The first lint version should stay intentionally narrow and focus on high-value contract checks:

1. required repository scaffold exists
2. required template files exist
3. template-derived `dashboard-data.json` matches canonical template state
4. skill files expose usable read/write contract sections
5. no skill declares the same path in both write and must-not-write sections
6. delegated in-repo skill references resolve to existing repo skills
7. a selected current project, when present, resolves to a valid live project

Lint output should be structured and severity-based so it can become part of future automation.

## Non-Goals

- no full experiment execution runner in this batch
- no automatic project migration from legacy V1
- no dashboard frontend implementation here
- no branch/idea creation tool yet

## Expected Outcome

After this batch, V2 will have:

- a real project instantiation path
- a real current-project selection path
- a first executable contract guardrail
- a cleaner base for later branch tooling and dashboard refresh tooling
