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
