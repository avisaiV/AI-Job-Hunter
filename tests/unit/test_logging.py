import json
import logging

from ai_job_hunter.config import LogLevel
from ai_job_hunter.logging import (
    REDACTED,
    configure_logging,
    reset_correlation_id,
    set_correlation_id,
)


def test_structured_logging_redacts_common_and_explicit_sensitive_values(capsys: object) -> None:
    configure_logging(LogLevel.INFO)
    token = set_correlation_id("test-run")
    logger = logging.getLogger("test")

    try:
        logger.info(
            "password=hunter2 Authorization: Bearer synthetic-token candidate_note=%s",
            "Synthetic private note",
            extra={"sensitive_values": ("Synthetic private note",)},
        )
    finally:
        reset_correlation_id(token)

    captured = capsys.readouterr()  # type: ignore[attr-defined]
    event = json.loads(captured.err)
    assert event["correlation_id"] == "test-run"
    assert event["message"] == (
        f"password={REDACTED} Authorization: {REDACTED} candidate_note={REDACTED}"
    )
    assert "hunter2" not in captured.err
    assert "synthetic-token" not in captured.err
    assert "Synthetic private note" not in captured.err
