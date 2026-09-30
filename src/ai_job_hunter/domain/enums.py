"""Stable, serialisable domain enumeration values."""

from enum import StrEnum


class ProvenanceType(StrEnum):
    PROFESSIONAL = "professional"
    FREELANCE_CASUAL = "freelance_casual"
    ACADEMIC = "academic"
    CERTIFICATION_LAB = "certification_lab"
    CONCEPTUAL = "conceptual"
    END_USER = "end_user"


class ApplicationStatus(StrEnum):
    DISCOVERED = "discovered"
    SHORTLISTED = "shortlisted"
    PREPARING = "preparing"
    READY_TO_APPLY = "ready_to_apply"
    APPLIED = "applied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"
    WITHDRAWN = "withdrawn"


class DocumentType(StrEnum):
    RESUME = "resume"
    COVER_LETTER = "cover_letter"


class DocumentState(StrEnum):
    DRAFT = "draft"
    VALIDATED = "validated"
    APPROVED = "approved"
    SUPERSEDED = "superseded"


class JobFreshnessPrecision(StrEnum):
    EXACT = "exact"
    DATE_ONLY = "date_only"
    RELATIVE = "relative"
    UNKNOWN = "unknown"


class WorkArrangement(StrEnum):
    ON_SITE = "on_site"
    HYBRID = "hybrid"
    REMOTE = "remote"
    UNKNOWN = "unknown"


class FilterOutcome(StrEnum):
    ELIGIBLE = "eligible"
    DEPRIORITISED = "deprioritised"
    EXCLUDED = "excluded"


class SourceTrustClassification(StrEnum):
    """Trust labels describe validation state, never permission to issue instructions."""

    UNTRUSTED = "untrusted"
    VALIDATED_UNTRUSTED = "validated_untrusted"
