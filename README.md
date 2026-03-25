# Link-Research V2

Schema-first research steering for a Claude-led paper workflow.

This branch is the V2 rebuild: canonical project state lives in project files, dashboard data is derived, and operator tooling is beginning to move from prose into executable repo-local commands.

## Quickstart

Create a live project from the canonical scaffold:

```bash
python -m tools.link_research_cli new-project --slug demo-project --title "Demo Project"
```

Set the current project pointer used by local operator tooling:

```bash
python -m tools.link_research_cli switch-project --slug demo-project
```

List live projects:

```bash
python -m tools.link_research_cli list-projects
```

Run the current harness contract checks:

```bash
python -m tools.link_research_cli harness-lint
```

Run the tooling test suite:

```bash
pytest -q
```

## Notes

- `projects/_template/` remains the canonical scaffold and fixture for V2.
- `.link-research/runtime.json` is local operator convenience state, not canonical research state.
- `projects/<slug>/workspace/dashboard-data.json` is derived and should be regenerated from canonical files rather than edited as source of truth.
