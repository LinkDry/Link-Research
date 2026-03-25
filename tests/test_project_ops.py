import json
import shutil
from pathlib import Path

import pytest

from tools.project_ops import (
    create_project,
    load_runtime_pointer,
    validate_project_slug,
    write_runtime_pointer,
)
from tools.project_state import (
    build_dashboard_projection,
    load_json_file,
    parse_experiment_memory,
    parse_state_markdown,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def repo_fixture(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "projects", tmp_path / "projects")
    return tmp_path


def test_validate_project_slug_accepts_safe_slug():
    assert validate_project_slug("demo-project") == "demo-project"


@pytest.mark.parametrize("slug", ["Demo", "bad_slug", "bad slug", "-leading"])
def test_validate_project_slug_rejects_invalid_slug(slug: str):
    with pytest.raises(ValueError):
        validate_project_slug(slug)


def test_create_project_instantiates_live_project_without_template_noise(repo_fixture: Path):
    project_dir = create_project(
        repo_root=repo_fixture,
        slug="demo-project",
        title="Demo Project",
        owner="tester",
    )

    assert project_dir == repo_fixture / "projects" / "demo-project"
    assert (project_dir / "STATE.md").exists()
    assert (project_dir / "experiment-memory.md").exists()
    assert (project_dir / "review-state.json").exists()
    assert (project_dir / "workspace" / "dashboard-data.json").exists()
    assert (project_dir / "workspace" / "reviews").exists()
    assert (project_dir / "papers" / "drafts").exists()
    assert not (project_dir / "plans" / "_template-anchor.md").exists()
    assert not (project_dir / "plans" / "_template-experiment-plan.md").exists()
    assert not (project_dir / "workspace" / "reviews" / "exp-template").exists()
    assert not (project_dir / "workspace" / "results" / "rg-template").exists()

    state = parse_state_markdown(project_dir / "STATE.md")
    experiment = parse_experiment_memory(project_dir / "experiment-memory.md")
    review_state = load_json_file(project_dir / "review-state.json")
    dashboard = load_json_file(project_dir / "workspace" / "dashboard-data.json")
    brief = (project_dir / "project-brief.md").read_text(encoding="utf-8")

    assert state["project_id"] == "proj-demo-project"
    assert state["project_title"] == "Demo Project"
    assert state["experiment_memory_path"] == "projects/demo-project/experiment-memory.md"
    assert review_state["project_id"] == "proj-demo-project"
    assert "project_title: Demo Project" in brief
    assert "project_slug: demo-project" in brief
    assert "owner: tester" in brief
    assert dashboard == build_dashboard_projection(state, experiment, review_state)


def test_runtime_pointer_round_trip(repo_fixture: Path):
    create_project(repo_root=repo_fixture, slug="demo-project", title="Demo Project")

    runtime_state = write_runtime_pointer(repo_root=repo_fixture, slug="demo-project")

    assert runtime_state["current_project_slug"] == "demo-project"
    assert runtime_state["current_project_path"] == "projects/demo-project"
    assert load_runtime_pointer(repo_root=repo_fixture) == runtime_state
