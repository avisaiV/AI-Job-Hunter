import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "private_path",
    [
        "candidate/profile.yaml",
        "templates/base_cv.docx",
        "data/jobs.sqlite3",
        "raw/job-alert.eml",
        "output/cover-letter.docx",
        "logs/application.log",
        "tmp/import.tmp",
        ".env",
    ],
)
def test_private_runtime_paths_are_git_ignored(private_path: str) -> None:
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", private_path],
        cwd=root,
        check=False,
    )

    assert result.returncode == 0, f"expected Git to ignore {private_path}"
