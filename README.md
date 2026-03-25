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

Inspect the currently selected project and get a suggested next Claude prompt:

```bash
python -m tools.link_research_cli current-project
```

Refresh the derived dashboard files for the current project:

```bash
python -m tools.link_research_cli refresh-dashboard
```

Refresh all live project dashboards and regenerate the repo-local portfolio page:

```bash
python -m tools.link_research_cli refresh-dashboard --all
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

## Operator Flow

For the real day-1 path into Phase 1, use:

- `docs/guides/phase1-quickstart.md`
- `docs/guides/recovery-and-resume.md`
- `docs/guides/dashboard-usage.md`

The intended operator loop is:

1. Create a project.
2. Switch to it.
3. Fill `projects/<slug>/project-brief.md`.
4. Ask Claude to begin Phase 1 bootstrap.
5. Use `python -m tools.link_research_cli current-project` whenever you need a fast recovery summary.
6. Use `python -m tools.link_research_cli refresh-dashboard` whenever you want a fresh dashboard snapshot and HTML view.
7. Use `.link-research/dashboard/index.html` after `refresh-dashboard --all` when you want a repo-local portfolio overview.

## Notes

- `projects/_template/` remains the canonical scaffold and fixture for V2.
- `.link-research/runtime.json` is local operator convenience state, not canonical research state.
- `projects/<slug>/workspace/dashboard-data.json` is derived and should be regenerated from canonical files rather than edited as source of truth.
