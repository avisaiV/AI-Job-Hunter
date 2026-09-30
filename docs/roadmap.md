# Milestone roadmap

Each milestone is a reviewable vertical slice. Do not begin source automation or document generation until the truth and audit foundations pass their criteria.

## M0 — Architecture approval (current)

**Scope:** product, architecture, data, security, decisions, and roadmap documentation only.

**Acceptance and validation:** requirements are traceable in the documents; prohibited automation, human approval, provenance, source modularity, component scoring, freshness, deduplication, credentials, risks, and open decisions are explicit. Review manually with the owner; run documentation/link/format checks available in the repository.

## M1 — Project foundation

**Scope:** Python package/CLI skeleton, dependency and tool configuration, privacy-safe ignores, configuration loading, typed domain primitives, logging/redaction, CI, and test fixtures.

**Acceptance:** a fresh documented setup runs CLI help and tests; runtime/private paths cannot be committed accidentally; configuration fails clearly; no application feature is implied. **Validation:** unit tests, lint/type checks, secret scan, clean-install smoke test.

## M2 — Candidate truth store

**Scope:** versioned YAML schemas/examples, loader, atomic facts, provenance/use/sensitivity policy, story bank, profile snapshotting, and validation CLI.

**Acceptance:** all six provenance types are representable; invalid dates/categories/references fail; a lab/end-user fact cannot be rendered as professional; scoring projections omit contact data. **Validation:** schema/property tests, golden fixtures, provenance-escalation and privacy tests, owner review of private profile.

## M3 — Job database and manual ingestion

**Scope:** SQLite schema/migrations/repositories, manual JSON/YAML sample adapter, normalisation, observations/lineage, freshness precision, basic duplicate resolution, and audit records.

**Acceptance:** required job fields and multiple observations persist idempotently; migrations work from empty; exact duplicates merge without losing lineage; uncertain duplicates await review; UTC/relative/unknown dates behave as designed. **Validation:** repository integration and migration tests, adapter contract tests, duplicate/freshness fixture matrix, backup/restore smoke test.

## M4 — Deterministic filtering and ranking

**Scope:** configurable title, seniority, experience, location, salary, and age policies with reason codes; ranked review queue.

**Acceptance:** clear senior/5+ year roles and out-of-scope on-site roles are handled predictably; missing/ambiguous data does not hard-reject; Sydney variants and 1–3 year roles follow policy; freshness tie-breaking is visible. **Validation:** table-driven boundary tests and owner-reviewed labelled job fixture set.

## M5 — Transparent scoring engine

**Scope:** rubric and seven component scores, evidence links, dealbreaker/cap policy, snapshot/version storage, 8.0 review threshold, calibration report.

**Acceptance:** totals are bounded and reproducible; components sum to 10.0 maximum; every awarded point/gap has job and candidate evidence; freshness is not hidden in compatibility. **Validation:** unit/invariant tests, hand-scored golden jobs, sensitivity/regression comparison after policy changes.

## M6 — AI analysis layer

**Scope:** provider-neutral interface, structured prompts/results, minimal candidate projection, injection-resistant boundary, output validation, cache/budget controls, and deterministic/AI reconciliation.

**Acceptance:** AI can explain but cannot invent facts, alter weights/status, access tools/files, or bypass caps; invalid output fails safely; provider/version/cost metadata is recorded; repeat outputs stay within an agreed tolerance. **Validation:** mocked provider contract tests, adversarial injection suite, malformed-output tests, blinded owner comparison with manual judgements.

## M7 — Resume tailoring and cover-letter planning

**Scope:** base-template analysis, supported claim selection, resume edit plan, story selection, company-specific cover-letter plan, claim manifest, human-readable diff.

**Acceptance:** every factual statement maps to permitted fact IDs; formatting/identity preservation rules are explicit; repeated story use is controllable; Australian English/no-em-dash/style checks pass; gaps are not disguised. **Validation:** provenance adversarial tests, golden text snapshots, unsupported-claim blocker, manual truth/style review.

## M8 — DOCX generation and package review

**Scope:** `python-docx` rendering, immutable versions, template/content hashes, output naming, validation report, approval metadata.

**Acceptance:** source template structure is preserved within agreed limits; generated documents open correctly; no hidden text; drafts cannot be mistaken for approved output; regeneration does not overwrite prior versions. **Validation:** DOCX structural tests, unzip/XML inspection, visual comparison/manual review, round-trip/open smoke tests.

## M9 — Review dashboard and tracking

**Scope:** Streamlit job queue, evidence/score views, duplicate review, document preview/download, notes, status history, and explicit human controls.

**Acceptance:** all canonical statuses are usable and audited; only the human can confirm `applied`; untrusted content is safely displayed; there is no submit control; core services remain UI-independent. **Validation:** service tests, UI smoke tests, status-transition matrix, XSS/unsafe-render regression tests, owner walkthrough.

## M10 — Compliant source integrations

**Scope:** job-alert email adapters first, then individually approved public feeds/APIs/employer pages; cursoring, idempotency, source health, compliance record.

**Acceptance:** each adapter passes the shared contract, records lineage and errors, honours rate/access rules, and has a documented permission basis; email access is least privilege; no restricted-site scraping is introduced. **Validation:** saved-message fixtures, mocked HTTP tests, replay/idempotency tests, source-specific compliance checklist and manual live smoke test.

## M11 — Scheduling and operations

**Scope:** single-host scheduled runs, locking, retries/backoff, summaries, retention, database backups, and recovery instructions.

**Acceptance:** repeated/concurrent runs do not duplicate/corrupt data; partial failures are resumable and visible; no job is applied for; backup restoration is demonstrated. **Validation:** concurrency/failure simulations, scheduled-run dry run, restore drill, redacted-log inspection.

## M12 — Hardening and release readiness

**Scope:** end-to-end regression, scoring calibration, threat-model review, privacy/deletion, performance, dependency/secret scans, user/runbook documentation.

**Acceptance:** labelled end-to-end fixtures pass; high-risk security cases fail closed; known limitations are documented; the owner signs off truth, privacy, ranking usefulness, and manual-control guarantees. **Validation:** full automated suite, security corpus, dependency and secret scans, fresh-machine rehearsal, final manual acceptance test.
