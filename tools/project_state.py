from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _coerce_value(raw: str) -> Any:
    value = raw.strip()
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("[") and value.endswith("]"):
        return json.loads(value)
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def parse_state_markdown(path: Path) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        key, raw_value = stripped[2:].split(":", 1)
        fields[key.strip()] = _coerce_value(raw_value)
    return fields


def parse_experiment_memory(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_snapshot = False
    rows: dict[str, Any] = {}
    for line in lines:
        stripped = line.strip()
        if stripped == "## Active Line Snapshot":
            in_snapshot = True
            continue
        if in_snapshot and stripped.startswith("## "):
            break
        if not in_snapshot or not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 2:
            continue
        field, value = cells
        if field in {"Field", "------"}:
            continue
        if value in {"Value", "-------"}:
            continue
        rows[field] = _coerce_value(value)
    return rows


def build_dashboard_projection(
    state: dict[str, Any],
    experiment: dict[str, Any],
    review_state: dict[str, Any],
) -> dict[str, Any]:
    run_is_active = state.get("current_run_id") and review_state.get("run_id") == state.get("current_run_id")
    run_block: dict[str, Any]
    if run_is_active:
        run_block = {
            "run_id": review_state.get("run_id"),
            "status": review_state.get("status"),
            "current_step_name": review_state.get("current_step_name"),
            "human_attention": review_state.get("human_attention"),
        }
    else:
        run_block = {
            "run_id": None,
            "status": None,
            "current_step_name": None,
            "human_attention": state.get("human_attention", "none"),
        }

    return {
        "meta": {
            "generated_at": state.get("last_updated"),
            "schema_version": "v2-draft",
            "is_derived": True,
        },
        "project": {
            "project_id": state.get("project_id"),
            "phase": state.get("phase"),
            "project_status": state.get("project_status"),
            "next_action": state.get("next_action"),
            "risk_level": state.get("risk_level"),
        },
        "experiment": {
            "experiment_id": experiment.get("experiment_id"),
            "status": experiment.get("status"),
            "latest_judge_verdict": experiment.get("latest_judge_verdict"),
            "latest_drift_score": experiment.get("latest_drift_score"),
            "next_experiment_action": experiment.get("next_experiment_action"),
        },
        "run": run_block,
        "memory": {
            "recent_warnings": [],
            "active_patterns": [],
            "open_capability_gaps": [],
        },
    }


def build_current_project_status(
    slug: str,
    state: dict[str, Any],
    experiment: dict[str, Any],
    review_state: dict[str, Any],
) -> dict[str, Any]:
    current_run_id = state.get("current_run_id")
    review_matches_state = bool(current_run_id) and review_state.get("run_id") == current_run_id

    return {
        "slug": slug,
        "project_title": state.get("project_title"),
        "phase": state.get("phase"),
        "project_status": state.get("project_status"),
        "active_idea_id": state.get("active_idea_id") or experiment.get("idea_id"),
        "active_branch_id": state.get("active_branch_id") or experiment.get("branch_id"),
        "current_run_id": current_run_id,
        "run_status": review_state.get("status") if review_matches_state else None,
        "current_step_name": review_state.get("current_step_name") if review_matches_state else None,
        "resume_safe": review_state.get("resume_safe") if review_matches_state else False,
        "human_attention": (
            review_state.get("human_attention")
            if review_matches_state
            else state.get("human_attention")
        ),
        "next_action": state.get("next_action"),
        "next_experiment_action": experiment.get("next_experiment_action"),
        "latest_judge_verdict": experiment.get("latest_judge_verdict"),
        "latest_drift_score": experiment.get("latest_drift_score"),
    }


def suggest_operator_prompt(status: dict[str, Any]) -> str:
    project_root = f"projects/{status['slug']}"
    current_run_id = status.get("current_run_id")
    run_status = status.get("run_status")

    if current_run_id and run_status in {"running", "paused", "blocked"}:
        step_name = status.get("current_step_name") or "the recorded step"
        return (
            f"Ask Claude to inspect {project_root}/review-state.json and resume run "
            f"{current_run_id} safely from {step_name} before starting any new branch."
        )

    if status.get("next_experiment_action") == "phase2-ready":
        return (
            f"Ask Claude to verify the evidence in {project_root}/experiment-memory.md and "
            f"start the approved Phase 2 workflow."
        )

    if status.get("phase") == "phase0" or not status.get("active_idea_id"):
        return (
            f"Ask Claude to read {project_root}/project-brief.md and begin the Phase 1 bootstrap "
            f"(intake mode selection, literature review, and first idea candidate generation)."
        )

    next_action = status.get("next_action") or "inspect canonical state and proceed conservatively"
    return (
        f"Ask Claude to open {project_root}/STATE.md and {project_root}/experiment-memory.md, "
        f"then continue from the recorded next action: {next_action}."
    )
