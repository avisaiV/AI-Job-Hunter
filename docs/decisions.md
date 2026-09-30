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
2. **Mailbox access (needed by M10):** dedicated alert mailbox/folder via read-only IMAP/OAuth, or user-exported `.eml` files first? Exported files are the safer initial choice.
3. **Location policy (needed by M4):** acceptable commute areas/duration, minimum hybrid expectations, and treatment of fully remote roles based outside NSW/Australia.
4. **Hard requirement policy (needed by M5):** which requirements (for example citizenship, work rights, clearance, licence, shifts) are absolute exclusions versus surfaced dealbreakers for review?
5. **Profile/template privacy (needed by M2/M7):** should encrypted/private source files live inside ignored repository folders, or in an external user-data directory referenced by configuration?
6. **Base document fidelity (needed by M8):** is DOCX the authoritative template and is optional local LibreOffice/PDF preview acceptable for visual validation?

Decisions that can safely wait include notification channel, scheduler choice, and additional source/API priority. Record resolved choices here with date, context, and consequences rather than burying them in code.
