# Phase 1 Quickstart

This guide is the shortest reliable path from a fresh repo checkout to a live Phase 1 project.

## 1. Create and select a project

```bash
python -m tools.link_research_cli new-project --slug demo-project --title "Demo Project"
python -m tools.link_research_cli switch-project --slug demo-project
python -m tools.link_research_cli current-project
```

The last command confirms which project Claude should operate on and shows the next suggested prompt.

## 2. Fill the project brief

Open `projects/<slug>/project-brief.md` and fill the intake fields before asking Claude to start work.

Use one of the two supported intake modes:

- `direction-search`: give Claude a research direction and let it search literature for promising novelty.
- `seed-papers`: provide one or more seed papers so Claude can propose tighter idea branches from a bounded context.

Keep the brief concrete. A good brief defines the target domain, constraints, evaluation preferences, and any hard exclusions.

## 3. Start Phase 1 bootstrap

Once the brief is filled, ask Claude to:

- read `projects/<slug>/project-brief.md`
- inspect `projects/<slug>/STATE.md`
- begin Phase 1 bootstrap

Recommended operator prompt:

```text
Read projects/<slug>/project-brief.md and the canonical Phase 1 state files, then begin Phase 1 bootstrap. Choose the correct intake mode, produce the first literature review pass, and propose the first idea candidates without drifting away from the brief.
```

## 4. Watch the canonical files

During Phase 1, treat these files as the main truth surface:

- `projects/<slug>/STATE.md`
- `projects/<slug>/experiment-memory.md`
- `projects/<slug>/review-state.json`

Use `python -m tools.link_research_cli current-project` whenever you want a compact summary instead of manually opening all three.

## 5. When to intervene

Most iterations should stay automated. Step in when:

- Claude reports a major branch or archive decision
- evidence no longer supports the original idea
- a run is blocked and asks for a human choice
- you want to redirect the research objective itself

When you do intervene, prefer explicit instructions tied to the canonical files rather than conversational guesses.
