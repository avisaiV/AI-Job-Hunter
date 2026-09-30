# Decisions, assumptions, and risks

## Initial decisions

| Decision | Rationale |
|---|---|
| Local-first modular Python monolith | Lowest operational burden and simplest privacy model for one user |
| SQLite with SQLAlchemy/Alembic | SQLite is sufficient locally; repository mappings and migrations preserve evolution options |
| YAML candidate truth plus validated snapshots | Human-reviewable facts with reproducible evaluations; operational database remains derived |
| Pydantic at external and AI boundaries | Reject malformed or over-privileged data before domain use |
| Streamlit only as a presentation adapter | Fast initial dashboard without coupling business rules to the UI |
| Compatibility score separate from freshness rank | Avoid representing recency as candidate/job fit while still prioritising new jobs |
| Candidate facts require atomic provenance | Prevent context inflation such as lab or end-user use becoming professional experience |
| Observations retained behind canonical jobs | Deduplication does not destroy source evidence or discovery history |
| AI is constrained analysis, never policy authority | Deterministic controls, schemas, evidence checks, and human review remain authoritative |
| No automatic submission | Product invariant and safety boundary, not a configurable convenience |
| Python 3.11 minimum with setuptools, `venv`, and `pip` | Supported across Windows and GitHub Actions without introducing a dependency manager |
| Pydantic Settings with `AJH_` environment variables | Provides typed validation, safe defaults, optional `.env` loading, and clear errors |
| Repository-local ignored private directories for the initial release | Simplifies a single-user setup while `.gitignore`, tests, and `doctor` reduce accidental commits |
| Standard-library `argparse` and JSON console logging | Meets M1 needs without adding CLI or observability frameworks |
| Ruff, strict mypy, pytest/coverage, and detect-secrets | A small, cross-platform quality and secret-scanning toolchain |

## Owner decisions recorded for future milestones

- Private candidate, template, runtime, raw, output, and log data initially live in
  repository-local ignored directories. Git may contain only explicitly synthetic or redacted
  examples.
- A hosted AI provider is the likely M6 direction, but no provider, API dependency, credential,
  or outbound-data policy is selected in M1.
- M10 email ingestion should begin with exported synthetic/sample `.eml` files before any live
  mailbox integration.
- DOCX is the intended authoritative editable format in M8. Optional local PDF rendering or
  visual comparison may be used for validation later.

## Assumptions to validate

- The application is single-user and normally runs on one trusted computer.
- Expected job volume fits SQLite and in-process matching comfortably.
- Job-alert emails contain enough metadata or permitted links to create useful observations without restricted scraping.
- The user's base DOCX has styles/structure that `python-docx` can preserve adequately.
- English-only job analysis and Australian English documents are sufficient initially.

## Major risks and mitigations

| Risk | Mitigation |
|---|---|
| Hallucinated or inflated candidate claims | Atomic fact IDs, provenance-aware wording, claim manifests, output validator, human review |
| Prompt injection/data exfiltration | Untrusted-data boundary, minimal projections, no model tools, schema/evidence validation, adversarial tests |
| Platform terms or page changes | Alert emails and permitted interfaces first, adapter isolation, compliance note per source, no prohibited scraping |
| False merges hide distinct vacancies | Conservative thresholds, source lineage, review band, overrides and reversible merge history |
| Duplicate roles evade matching | Layer exact IDs/URLs with explainable fuzzy features; calibrate against labelled pairs |
| Relative/missing dates distort freshness | Store precision/original text/retrieval time and rank uncertainty explicitly |
| AI scoring inconsistency or cost | Deterministic baseline, fixed rubric, versioned prompts/models, caching, budgets, calibration set |
| Private data leaks via Git/logs/provider | ignored private paths, redacted fixtures/logs, secret scanning, minimal provider payloads and retention review |
| DOCX formatting degradation | Separate edit plan from rendering, stable styles, structural/visual regression and immutable outputs |
| Local database loss or concurrent corruption | WAL/transactions where appropriate, run locks, versioned backups and restore drills |
| Over-filtering unconventional junior roles | Conservative hard rejects, reason codes, deprioritisation/review path and labelled-fixture tuning |

## Owner decisions needed before implementation reaches them

These are genuine product choices; none requires a secret now.

1. **Privacy boundary for AI (needed by M6):** hosted provider, fully local model, or hybrid; if hosted, which candidate fields and job text may leave the machine and what retention policy is acceptable?
2. **Mailbox access after file-based ingestion (needed by M10):** whether to add a dedicated
   alert mailbox/folder through read-only IMAP/OAuth after exported `.eml` ingestion is proven.
3. **Location policy (needed by M4):** acceptable commute areas/duration, minimum hybrid expectations, and treatment of fully remote roles based outside NSW/Australia.
4. **Hard requirement policy (needed by M5):** which requirements (for example citizenship, work rights, clearance, licence, shifts) are absolute exclusions versus surfaced dealbreakers for review?
5. **Longer-term profile/template privacy (revisit after M2/M7):** whether ignored local paths
   remain sufficient or should move to encrypted/external user-data storage.
6. **Visual validation tooling (needed by M8):** whether optional local LibreOffice/PDF preview
   is acceptable alongside authoritative DOCX templates.

Decisions that can safely wait include notification channel, scheduler choice, and additional source/API priority. Record resolved choices here with date, context, and consequences rather than burying them in code.
