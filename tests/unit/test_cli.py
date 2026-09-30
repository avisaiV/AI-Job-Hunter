import json
from pathlib import Path

import pytest

from ai_job_hunter.cli import main


def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])

    assert exit_info.value.code == 0
    assert "doctor" in capsys.readouterr().out


def test_doctor_creates_private_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("AJH_ENVIRONMENT", "test")

    assert main(["doctor"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ok"
    assert report["environment"] == "test"
    assert all(item["exists"] for item in report["private_directories"].values())
    assert all(item["git_ignored"] is None for item in report["private_directories"].values())
