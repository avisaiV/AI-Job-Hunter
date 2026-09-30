"""Typed, environment-aware application configuration."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

from pydantic import BeforeValidator, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_SOURCE_DIRECTORIES = frozenset({"src", "tests", "docs", ".git", ".github"})


class Environment(StrEnum):
    """Supported runtime modes."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class LogLevel(StrEnum):
    """Supported console logging thresholds."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def _non_empty_path(path: object) -> object:
    if isinstance(path, str) and not path.strip():
        raise ValueError("path must not be empty")
    return path


ConfiguredPath = Annotated[Path, BeforeValidator(_non_empty_path)]


class Settings(BaseSettings):
    """Application settings loaded from defaults, ``.env``, and ``AJH_*`` variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AJH_",
        extra="forbid",
        case_sensitive=False,
    )

    environment: Environment = Environment.DEVELOPMENT
    log_level: LogLevel = LogLevel.INFO
    runtime_data_dir: ConfiguredPath = Field(default=Path("data"))
    candidate_data_dir: ConfiguredPath = Field(default=Path("candidate"))
    template_dir: ConfiguredPath = Field(default=Path("templates"))
    output_dir: ConfiguredPath = Field(default=Path("output"))
    log_dir: ConfiguredPath = Field(default=Path("logs"))

    @model_validator(mode="after")
    def validate_private_paths(self) -> Settings:
        resolved = self.resolved_paths()
        values = list(resolved.values())
        if len(set(values)) != len(values):
            raise ValueError("private/runtime paths must be distinct")
        for name, path in resolved.items():
            if any(parent.name in _SOURCE_DIRECTORIES for parent in (path, *path.parents)):
                raise ValueError(f"{name} must not be inside a tracked source directory")
        return self

    def resolved_paths(self, *, base_dir: Path | None = None) -> dict[str, Path]:
        """Return absolute private/runtime paths without creating them."""

        base = (base_dir or Path.cwd()).resolve()
        fields = {
            "runtime_data_dir": self.runtime_data_dir,
            "candidate_data_dir": self.candidate_data_dir,
            "template_dir": self.template_dir,
            "output_dir": self.output_dir,
            "log_dir": self.log_dir,
        }
        return {
            name: (path if path.is_absolute() else base / path).resolve()
            for name, path in fields.items()
        }

    def ensure_runtime_directories(self, *, base_dir: Path | None = None) -> dict[str, Path]:
        """Create configured private/runtime directories and return their absolute paths."""

        paths = self.resolved_paths(base_dir=base_dir)
        for path in paths.values():
            path.mkdir(parents=True, exist_ok=True)
        return paths


def load_settings() -> Settings:
    """Load and validate settings, allowing Pydantic errors to explain invalid input."""

    return Settings()
