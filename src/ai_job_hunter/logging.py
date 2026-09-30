"""Structured console logging with defensive redaction."""

from __future__ import annotations

import json
import logging
import re
from contextvars import ContextVar, Token
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from ai_job_hunter.config import LogLevel

REDACTED = "[REDACTED]"
_correlation_id: ContextVar[str] = ContextVar("correlation_id", default="-")
_AUTHORIZATION_PATTERN = re.compile(
    r"(?i)(?P<prefix>authorization\s*[:=]\s*)(?:bearer|basic)\s+[^\s,;]+"
)
_SENSITIVE_PATTERN = re.compile(
    r"(?i)(?P<key>password|passwd|secret|api[_-]?key|access[_-]?token|auth(?:orization)?)"
    r"(?P<separator>\s*[:=]\s*|\s+)"
    r"(?P<value>[^\s,;]+)"
)


def redact(value: object, *, sensitive_values: tuple[str, ...] = ()) -> str:
    """Redact common key/value secrets and explicitly supplied sensitive values."""

    text = str(value)
    text = _AUTHORIZATION_PATTERN.sub(
        lambda match: f"{match.group('prefix')}{REDACTED}", text
    )
    text = _SENSITIVE_PATTERN.sub(
        lambda match: f"{match.group('key')}{match.group('separator')}{REDACTED}", text
    )
    for sensitive in sensitive_values:
        if sensitive:
            text = text.replace(sensitive, REDACTED)
    return text


class RedactingFilter(logging.Filter):
    """Sanitise the rendered log message before it reaches any handler."""

    def filter(self, record: logging.LogRecord) -> bool:
        supplied = getattr(record, "sensitive_values", ())
        sensitive_values = tuple(str(value) for value in supplied)
        record.msg = redact(record.getMessage(), sensitive_values=sensitive_values)
        record.args = ()
        record.correlation_id = _correlation_id.get()
        return True


class JsonFormatter(logging.Formatter):
    """Emit one JSON object per console log event."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", "-"),
        }
        if record.exc_info:
            sensitive_values = tuple(
                str(value) for value in getattr(record, "sensitive_values", ())
            )
            payload["exception"] = redact(
                self.formatException(record.exc_info), sensitive_values=sensitive_values
            )
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(level: LogLevel | str = LogLevel.INFO) -> None:
    """Configure safe structured console logging for the application."""

    handler = logging.StreamHandler()
    handler.addFilter(RedactingFilter())
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(str(level))


def new_correlation_id() -> str:
    """Create a non-sensitive run identifier."""

    return uuid4().hex


def set_correlation_id(value: str) -> Token[str]:
    """Set the correlation ID and return a token that can restore the prior value."""

    return _correlation_id.set(value)


def reset_correlation_id(token: Token[str]) -> None:
    """Restore the correlation ID context represented by ``token``."""

    _correlation_id.reset(token)
