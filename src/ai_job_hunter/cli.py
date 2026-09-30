"""Minimal command-line interface for foundation diagnostics."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from ai_job_hunter import __version__
from ai_job_hunter.config import Settings, load_settings
from ai_job_hunter.logging import configure_logging, new_correlation_id, set_correlation_id


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-job-hunter",
        description="Local project diagnostics for AI Job Hunter.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "doctor",
        help="validate configuration and prepare private runtime directories",
    )
    return parser


def _is_git_ignored(path: Path, *, project_root: Path) -> bool | None:
    try:
        relative = path.relative_to(project_root)
    except ValueError:
        return None
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(relative)],
        cwd=project_root,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def _doctor(settings: Settings, *, project_root: Path) -> int:
    paths = settings.ensure_runtime_directories(base_dir=project_root)
    checks = {
        name: {
            "path": str(path),
            "exists": path.is_dir(),
            "git_ignored": _is_git_ignored(path, project_root=project_root),
        }
        for name, path in paths.items()
    }
    failed = any(not check["exists"] or check["git_ignored"] is False for check in checks.values())
    report = {
        "status": "failed" if failed else "ok",
        "package_version": __version__,
        "python_version": sys.version.split()[0],
        "environment": settings.environment.value,
        "private_directories": checks,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failed else 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process status code."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        settings = load_settings()
    except ValidationError as error:
        parser.error(f"invalid configuration:\n{error}")
    configure_logging(settings.log_level)
    set_correlation_id(new_correlation_id())
    if args.command == "doctor":
        return _doctor(settings, project_root=Path.cwd().resolve())
    parser.error(f"unknown command: {args.command}")
