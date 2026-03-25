from pathlib import Path

from tools.harness_lint import run_harness_lint


REPO_ROOT = Path(__file__).resolve().parents[1]

PHASE1_SKILLS = [
    "literature-review",
    "idea-creator",
    "novelty-check",
    "experiment-plan",
    "run-experiment",
    "analyze-results",
]

BOOTSTRAP_VIEW_DOCS = [
    "docs/views/literature-review-view.md",
    "docs/views/idea-candidates-view.md",
    "docs/views/novelty-check-view.md",
]


def test_missing_phase1_skill_files_exist_with_standard_contract_sections():
    required_markers = [
        "## Read / Write Contract",
        "### Read",
        "### Write",
        "### Must Not Write",
        "## Protocol",
        "## Self-Check",
    ]

    for skill_name in PHASE1_SKILLS:
        skill_path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
        assert skill_path.exists(), f"Missing skill file: {skill_path}"
        content = skill_path.read_text(encoding="utf-8")
        for marker in required_markers:
            assert marker in content, f"{skill_name} missing section: {marker}"


def test_bootstrap_view_docs_exist():
    for relative_path in BOOTSTRAP_VIEW_DOCS:
        path = REPO_ROOT / relative_path
        assert path.exists(), f"Missing bootstrap artifact view doc: {relative_path}"
        content = path.read_text(encoding="utf-8")
        assert "## Purpose" in content
        assert "## Canonical Location" in content


def test_harness_lint_no_longer_reports_missing_delegate_skills():
    report = run_harness_lint(REPO_ROOT)
    missing_delegate_findings = [
        finding for finding in report["findings"] if finding["code"] == "missing-delegate-skill"
    ]

    assert missing_delegate_findings == []
