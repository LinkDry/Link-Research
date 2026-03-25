from pathlib import Path

import pytest

from tools.link_research_cli import main
from tools.project_ops import create_project, load_runtime_pointer


@pytest.fixture()
def repo_fixture(tmp_path: Path) -> Path:
    source_root = Path(__file__).resolve().parents[1]
    import shutil

    shutil.copytree(source_root / "projects", tmp_path / "projects")
    shutil.copytree(source_root / "memory", tmp_path / "memory")
    shutil.copytree(source_root / "skills", tmp_path / "skills")
    return tmp_path


def test_cli_new_project_creates_project_and_reports_success(repo_fixture: Path, capsys: pytest.CaptureFixture[str]):
    exit_code = main(
        ["new-project", "--slug", "demo-project", "--title", "Demo Project", "--owner", "tester"],
        repo_root=repo_fixture,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Created project demo-project" in captured.out
    assert (repo_fixture / "projects" / "demo-project").exists()


def test_cli_list_projects_marks_current_project(repo_fixture: Path, capsys: pytest.CaptureFixture[str]):
    create_project(repo_fixture, "demo-project", "Demo Project")
    create_project(repo_fixture, "second-project", "Second Project")
    main(["switch-project", "--slug", "second-project"], repo_root=repo_fixture)

    exit_code = main(["list-projects"], repo_root=repo_fixture)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "demo-project" in captured.out
    assert "* second-project" in captured.out


def test_cli_switch_project_updates_runtime_pointer(repo_fixture: Path, capsys: pytest.CaptureFixture[str]):
    create_project(repo_fixture, "demo-project", "Demo Project")

    exit_code = main(["switch-project", "--slug", "demo-project"], repo_root=repo_fixture)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Current project set to demo-project" in captured.out
    assert load_runtime_pointer(repo_fixture)["current_project_slug"] == "demo-project"


def test_cli_returns_non_zero_for_missing_project(repo_fixture: Path, capsys: pytest.CaptureFixture[str]):
    exit_code = main(["switch-project", "--slug", "missing-project"], repo_root=repo_fixture)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Unknown project slug" in captured.err


def test_cli_harness_lint_runs_and_reports_summary(repo_fixture: Path, capsys: pytest.CaptureFixture[str]):
    exit_code = main(["harness-lint"], repo_root=repo_fixture)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Harness lint:" in captured.out
    assert "warning" in captured.out.lower()


def test_readme_documents_cli_quickstart():
    readme = Path(__file__).resolve().parents[1] / "README.md"

    assert readme.exists()
    content = readme.read_text(encoding="utf-8")
    assert "python -m tools.link_research_cli new-project" in content
    assert "python -m tools.link_research_cli harness-lint" in content
