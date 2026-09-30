# Architecture

## Technology recommendation

Use a **modular Python monolith** with a `src/` layout, SQLite, SQLAlchemy plus Alembic migrations, Pydantic validation, YAML authoring for candidate data, pytest, `python-docx`, and Streamlit. The proposed stack fits a single-user local application. SQLAlchemy avoids coupling domain logic to SQLite and Alembic makes schema evolution explicit; Pydantic validates YAML, adapter, and AI boundaries. Streamlit is appropriate for a review-first initial UI, but domain services must not import it so a later UI can replace it.

Do not add queues, containers, a vector database, or microservices initially. Use a CLI and in-process services first. Scheduling can later use the host scheduler or a small application runner with a lock.

## Logical layers

```text
alert emails / manual files / permitted APIs and pages
                         |
                  source adapters
                         v
 raw observation -> validate/normalise -> identity resolution
                                            |
                                     deterministic filter
                                            |
 candidate truth store ------------> scoring + AI analysis
                                            |
                                  review / application record
                                            |
                         document planning -> DOCX export
                                            |
                                  Streamlit dashboard
```

Suggested eventual layout (create directories only when their milestone begins):

```text
candidate/                 private YAML truth store (ignored; redacted examples tracked)
templates/                 user-provided base DOCX templates (private by default)
src/ai_job_hunter/
  domain/                  entities, value objects, enums, policies
  adapters/sources/        source-specific acquisition and mapping
  ingestion/               orchestration, validation, normalisation
  matching/                filters, scoring, analysis contracts
  documents/               claim selection, rendering and validation
  persistence/             repositories, ORM mappings and migrations
  application/             use cases and status-transition service
  dashboard/               Streamlit composition only
data/                      ignored runtime database and quarantined payloads
output/                    ignored generated application packages
tests/                     unit, integration, contract, security, fixtures
```

Dependencies point inward: adapters, persistence, dashboard, and AI implementations depend on application/domain interfaces. Domain code does not depend on Streamlit, SQLAlchemy, email clients, or a model vendor.

## Pipeline boundaries

### Acquisition and normalisation

Each adapter returns source observations, never database objects. The ingestion service assigns discovery metadata, size/content-type limits inputs, quarantines malformed payloads, sanitises rendered content, and maps fields into a validated normalised job. Original content is retained only when needed for audit and with retention controls.

Initial adapter priority is manual/sample import, then job-alert email parsing for SEEK, LinkedIn, and Indeed. Alert parsing uses emails the user is authorised to access; links remain links and do not authorise scraping the destination. Public APIs/feeds and employer pages require a source-specific compliance review, rate limit, identification policy, and tests.

### Identity resolution

Exact source IDs and canonical URLs resolve first. Probabilistic duplicate candidates are then found with normalised company, title, location, and posting-time similarity. High-confidence matches merge into one canonical job while retaining every observation; medium-confidence matches enter a review queue; weak matches remain separate. No raw source is discarded during a merge, and user decisions become durable overrides.

### Filtering and analysis

Deterministic rules classify a job as `eligible`, `deprioritised`, or `excluded`, with reason codes. Hard exclusion is limited to confident facts such as an out-of-area on-site location or clearly senior role; ambiguity is not exclusion. Only eligible/deprioritised jobs proceed according to configured budgets.

Scoring has deterministic inputs and a constrained AI assessment. The model receives a purpose-built, minimal candidate projection and delimited job data, not filesystem access or secrets. It returns a versioned schema with evidence references. Application code validates, bounds, and reconciles output; a model cannot alter weights, statuses, candidate facts, or tool permissions.

### Documents and review

Document generation is a claim-selection pipeline, not free-form biography generation: select candidate fact IDs, produce proposed transformations, validate every claim against provenance, show a diff/claim manifest, then render a versioned DOCX from the user's template. A failed or untraceable claim blocks export. Generated files are drafts. The dashboard provides no automatic-submit capability.

## Freshness and ranking

Store source-provided posting time with timezone and precision (`exact`, `date_only`, `relative`, `unknown`) plus immutable `first_discovered_at` and mutable `last_seen_at`, all normalised to UTC. Preserve the original posted text. Relative dates are resolved using source retrieval time and flagged as inferred.

Freshness is a ranking modifier, not part of compatibility truth: band A is at most 48 hours, band B is over 48 hours through seven days, band C is older, and unknown is explicitly marked. Within otherwise similar scores, rank A above B, B above unknown, and unknown above known-stale C by default. Never repeatedly reset freshness when a duplicate is rediscovered; use the earliest credible posted time and first discovery.

## Operations and observability

- structured local logs with correlation IDs; redact candidate text, email bodies, tokens, and model prompts by default
- idempotency keys per source observation and scheduled run
- persisted rule, prompt, model, schema, and score-policy versions for reproducibility
- transactional writes around ingestion, merges, status changes, and document metadata
- backups for the SQLite database and candidate files, with restore tests before automation
