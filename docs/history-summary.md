# History Summary

This repository was tightened from an older, more centralized protocol style into the current
schema-first layout so Claude can operate from canonical project files instead of long freeform
plans.

## Current Source Of Truth

Treat these paths as the active surface:

- `docs/guides/`
- `docs/policies/`
- `docs/schema/`
- `docs/views/`
- root `skills/*/SKILL.md`
- `scaffold/project/` for new-project instantiation
- `projects/<slug>/...` for live canonical state

## Why The History Was Pruned

Older migration plans, red/green notes, and design scratchpads were useful while the system was
being rebuilt, but they created search noise for both humans and models. They are no longer part of
the live operating contract.

## GPT Advisory Review Touchpoints

Claude remains the primary operator. GPT-5.4 participates only as an advisory reviewer through
Codex MCP at these checkpoints:

- `novelty-check`
- `experiment-plan`
- `drift-detector`
- `judge`
- `phase2-publish`

Those reviews expand scrutiny and help catch overclaim risk, but canonical project state still
belongs to the owning Claude-side skill.
