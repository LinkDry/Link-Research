import json
from pathlib import Path

from tools.project_state import (
    build_dashboard_projection,
    build_current_project_status,
    load_json_file,
    parse_experiment_memory,
    parse_state_markdown,
    suggest_operator_prompt,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "projects" / "_template"


def test_parse_state_markdown_reads_scalar_and_list_fields():
    state = parse_state_markdown(TEMPLATE_DIR / "STATE.md")

    assert state["project_id"] == "proj-template"
    assert state["project_title"] == "Template Project"
    assert state["phase"] == "phase0"
    assert state["current_run_id"] is None
    assert state["blockers"] == []


def test_parse_experiment_memory_reads_active_line_snapshot():
    experiment = parse_experiment_memory(TEMPLATE_DIR / "experiment-memory.md")

    assert experiment["experiment_id"] is None
    assert experiment["status"] == "planned"
    assert experiment["iteration_count"] == 0
    assert experiment["archive_recommended"] is False
    assert experiment["human_review_required"] is False


def test_build_dashboard_projection_matches_template_fixture():
    state = parse_state_markdown(TEMPLATE_DIR / "STATE.md")
    experiment = parse_experiment_memory(TEMPLATE_DIR / "experiment-memory.md")
    review_state = load_json_file(TEMPLATE_DIR / "review-state.json")

    actual = build_dashboard_projection(state, experiment, review_state)
    expected = json.loads((TEMPLATE_DIR / "workspace" / "dashboard-data.json").read_text(encoding="utf-8"))

    assert actual == expected


def test_build_current_project_status_uses_canonical_state():
    state = parse_state_markdown(TEMPLATE_DIR / "STATE.md")
    experiment = parse_experiment_memory(TEMPLATE_DIR / "experiment-memory.md")
    review_state = load_json_file(TEMPLATE_DIR / "review-state.json")

    status = build_current_project_status("demo-project", state, experiment, review_state)

    assert status["slug"] == "demo-project"
    assert status["project_title"] == "Template Project"
    assert status["phase"] == "phase0"
    assert status["project_status"] == "idle"
    assert status["current_run_id"] is None
    assert status["run_status"] is None


def test_suggest_operator_prompt_for_bootstrap_state():
    state = parse_state_markdown(TEMPLATE_DIR / "STATE.md")
    experiment = parse_experiment_memory(TEMPLATE_DIR / "experiment-memory.md")
    review_state = load_json_file(TEMPLATE_DIR / "review-state.json")
    status = build_current_project_status("demo-project", state, experiment, review_state)

    prompt = suggest_operator_prompt(status)

    assert "project-brief.md" in prompt
    assert "Phase 1 bootstrap" in prompt
