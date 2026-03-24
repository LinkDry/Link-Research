# Archive Record

## Identity
- archive_id: archive-exp-template
- project_id: proj-template
- experiment_id: exp-template
- idea_id: idea-template
- branch_id: branch-main
- parent_branch_id: null
- archived_at: 2026-03-24T00:00:00+08:00
- archive_reason: judge-archive
- archive_trigger_ref: projects/<slug>/workspace/reviews/<experiment_id>/judge-report-<iteration>.json

## Final Outcome
- final_status: archived
- final_judge_verdict: archive
- final_drift_decision: consistent
- final_drift_score: 8.0
- total_iterations: 3
- success_criteria_status: unmet

## Locked Claim Context
- anchor_path: projects/<slug>/archive/artifacts/<experiment_id>/anchor.md
- anchor_version: v1
- claim_summary: Summarize the failed or abandoned line in 1-2 sentences.
- plan_ref: projects/<slug>/archive/artifacts/<experiment_id>/experiment-plan.md

## Evidence Summary
- result_refs: ["results.tsv#rg-template"]
- analysis_refs: ["projects/<slug>/workspace/results/rg-template/analysis-report.json"]
- judge_report_ref: projects/<slug>/workspace/reviews/<experiment_id>/judge-report-<iteration>.json
- artifact_bundle_path: projects/<slug>/archive/artifacts/<experiment_id>/
- evidence_limitations: ["Document any reasons the evidence is incomplete or ambiguous."]

## Failure Analysis
- failure_class: inconclusive
- why_it_failed: Explain the concrete failure mechanism.
- what_would_need_to_change: State what would have to change for this line to become viable.
- key_takeaway: One reusable lesson for future idea generation or validation.
- when_to_warn_again: Describe the future trigger pattern that should raise caution.

## Workspace Preservation
| item_path | handling | archive_path | notes |
|-----------|----------|--------------|-------|
| projects/<slug>/plans/<idea>/anchor.md | snapshotted | projects/<slug>/archive/artifacts/<experiment_id>/anchor.md | Stable archived copy because the live idea-scoped slot may later be reused. |
| projects/<slug>/plans/<idea>/experiment-plan.md | snapshotted | projects/<slug>/archive/artifacts/<experiment_id>/experiment-plan.md | Preserve the editable pre-anchor plan that led to this archived line. |
| projects/<slug>/workspace/results/rg-template/ | moved | projects/<slug>/archive/artifacts/<experiment_id>/rg-template/ | Example preserved artifact bundle. |

## Memory Promotion
- lesson_ref: Fill with the concrete inserted lesson row ref in `memory/lessons-learned.md`.
- failure_library_ref: Fill with the concrete inserted failure row ref in `memory/failure-library.md`.
- similarity_tags: ["example-tag"]
