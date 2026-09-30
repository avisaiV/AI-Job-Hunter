from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_job_hunter.config import Environment, LogLevel, Settings


def test_settings_have_safe_repository_local_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AJH_RUNTIME_DATA_DIR", raising=False)
    settings = Settings(_env_file=None)

    assert settings.environment is Environment.DEVELOPMENT
    assert settings.log_level is LogLevel.INFO
    assert settings.runtime_data_dir == Path("data")
    assert settings.candidate_data_dir == Path("candidate")
    assert settings.template_dir == Path("templates")
    assert settings.output_dir == Path("output")
    assert settings.log_dir == Path("logs")


def test_settings_accept_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AJH_ENVIRONMENT", "test")
    monkeypatch.setenv("AJH_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("AJH_RUNTIME_DATA_DIR", "private/runtime")

    settings = Settings(_env_file=None)

    assert settings.environment is Environment.TEST
    assert settings.log_level is LogLevel.DEBUG
    assert settings.runtime_data_dir == Path("private/runtime")


@pytest.mark.parametrize(
    ("field", "value"),
    [("log_level", "TRACE"), ("environment", "staging")],
)
def test_settings_reject_invalid_enum_values(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: value}, _env_file=None)  # type: ignore[arg-type]


def test_settings_reject_duplicate_private_paths() -> None:
    with pytest.raises(ValidationError, match="must be distinct"):
        Settings(runtime_data_dir="private", output_dir="private", _env_file=None)


def test_settings_reject_empty_paths() -> None:
    with pytest.raises(ValidationError, match="path must not be empty"):
        Settings(runtime_data_dir="", _env_file=None)


def test_settings_reject_paths_inside_source_tree() -> None:
    with pytest.raises(ValidationError, match="tracked source directory"):
        Settings(candidate_data_dir="src/private", _env_file=None)


def test_runtime_directories_resolve_and_are_created(tmp_path: Path) -> None:
    settings = Settings(_env_file=None)

    paths = settings.ensure_runtime_directories(base_dir=tmp_path)

    assert paths["runtime_data_dir"] == (tmp_path / "data").resolve()
    assert all(path.is_dir() for path in paths.values())
