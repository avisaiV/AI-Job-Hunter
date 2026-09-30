import json
from enum import StrEnum

import pytest

from ai_job_hunter.domain import (
    ApplicationStatus,
    DocumentState,
    DocumentType,
    FilterOutcome,
    JobFreshnessPrecision,
    ProvenanceType,
    SourceTrustClassification,
    WorkArrangement,
)


@pytest.mark.parametrize(
    ("enum_type", "expected"),
    [
        (
            ProvenanceType,
            [
                "professional",
                "freelance_casual",
                "academic",
                "certification_lab",
                "conceptual",
                "end_user",
            ],
        ),
        (
            ApplicationStatus,
            [
                "discovered",
                "shortlisted",
                "preparing",
                "ready_to_apply",
                "applied",
                "interview",
                "rejected",
                "offer",
                "withdrawn",
            ],
        ),
        (DocumentType, ["resume", "cover_letter"]),
        (DocumentState, ["draft", "validated", "approved", "superseded"]),
        (JobFreshnessPrecision, ["exact", "date_only", "relative", "unknown"]),
        (WorkArrangement, ["on_site", "hybrid", "remote", "unknown"]),
        (FilterOutcome, ["eligible", "deprioritised", "excluded"]),
        (SourceTrustClassification, ["untrusted", "validated_untrusted"]),
    ],
)
def test_domain_enum_values_are_stable_and_json_serialisable(
    enum_type: type[StrEnum], expected: list[str]
) -> None:
    values = list(enum_type)

    assert [item.value for item in values] == expected
    assert json.loads(json.dumps(values)) == expected
