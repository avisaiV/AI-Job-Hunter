# Data model and contracts

This document describes the domain model. Exact SQL and Pydantic representations are deferred until the foundation milestone.

## Jobs and source lineage

### `Job`

The canonical vacancy:

- `id` (UUID), `company_id`/normalised company name, `title`, normalised `location`
- `salary_min`, `salary_max`, `salary_currency`, `salary_period`, and original salary text
- `employment_type`, `work_arrangement` (on-site/hybrid/remote/unknown)
- `posted_at`, timezone, posting precision, original posted text
- `first_discovered_at`, `last_seen_at`, `description_text`, structured requirements
- canonical `application_url` and `original_url`
- lifecycle/availability state, created/updated timestamps

### `JobObservation`

One source sighting: `id`, `job_id`, `source_name`, optional `source_job_id`, canonical/original/application URLs, `retrieved_at`, source-posted fields, payload hash, parser version, trust classification, and optional pointer to a retained raw payload. A uniqueness key such as `(source_name, source_job_id)` is used when IDs exist; otherwise an adapter-generated idempotency fingerprint is used.

### Requirements

`JobRequirement` records text, normalised skill/category, mandatory/preferred/unknown importance, minimum years where stated, evidence span/observation ID, and extraction confidence. Extracted requirements never become candidate facts.

### Duplicate decisions

`DuplicateCandidate` stores the job pair, feature values, algorithm version, confidence, state (`auto_merged`, `needs_review`, `not_duplicate`), and reviewer override. `JobAlias`/merge history preserves old IDs and supports reversal/audit. Useful features include exact source ID, canonical URL, company-domain/name similarity, title tokens, location, description fingerprint, salary, and posted-time window.

## Candidate truth store

YAML is the human-editable source of truth and is validated into domain objects. Suggested private files are `candidate/profile.yaml`, `experience.yaml`, `skills.yaml`, `education.yaml`, `certifications.yaml`, `story_bank.yaml`, and `writing_style.md`. Redacted examples define schemas without exposing personal data. Database projections are derived caches and never silently overwrite YAML.

### `CandidateProfile`

Contains identity/contact references, location and work preferences, target roles, salary preferences, education IDs, certification IDs, experience IDs, skill assertions, story IDs, and explicit constraints. Sensitive contact fields should be separable so scoring never receives them.

### `ExperienceRecord`

Contains `id`, organisation/context, role/title, dates with precision, summary, and a required provenance category. Its child `CandidateFact` records an atomic claim:

- stable `fact_id` and factual text
- `provenance_type`
- parent evidence record and optional evidence note/artifact reference
- skill/topic tags and capability level
- start/end dates or `unknown`, verification state, and last-reviewed date
- allowed uses (`scoring`, `resume`, `cover_letter`) and sensitivity classification

Allowed `provenance_type` values and claim limits:

| Type | Meaning | Permitted wording |
|---|---|---|
| `professional` | Paid employment performing the stated responsibility | May say professional/workplace experience within the recorded scope |
| `freelance_casual` | Casual, freelance, volunteer, or informal work | Name the context; never imply enterprise employment |
| `academic` | Coursework or assessed project | Say studied/built in an academic project |
| `certification_lab` | Guided or independent certification lab | Say practised/demonstrated in a lab, not administered professionally |
| `conceptual` | Theory understood without asserted hands-on use | Say knowledge/familiarity only |
| `end_user` | Used a product as a user | Say used as an end user; never infer support/administration |

Provenance is attached to each atomic fact, not merely a role or skill. Derived summaries retain the contributing fact IDs and may never use a stronger experience verb/category than their strongest directly relevant evidence. Conflicting or unverified facts are withheld from documents and surfaced for review.

### `Story`

A verified STAR-like story containing situation, actions, result, fact IDs, themes, context/provenance, allowed uses, and sensitivity. Generators select stories for relevance and diversity; they cannot invent missing outcomes.

## Source-adapter contract

Conceptual asynchronous interface (exact syntax is deferred):

```python
class JobSourceAdapter(Protocol):
    name: str
    capabilities: SourceCapabilities

    async def discover(self, cursor: SourceCursor | None) -> DiscoveryBatch: ...
    def normalise(self, item: RawJobObservation) -> NormalisedJobDraft: ...
```

`DiscoveryBatch` contains observations, the next cursor, retrieval metadata, and per-item errors so one malformed item does not lose the batch. `SourceCapabilities` declares access method, terms/compliance notes, rate limits, supported fields, and whether detail fetching is permitted. Adapters have no scoring, persistence, AI, or document responsibilities. They must be idempotent and preserve source lineage. A separate orchestrator validates output and commits it through repository interfaces.

## Filtering and scoring

### Filter result

`FilterAssessment` stores outcome, reason codes, evidence spans, rule-set version, and evaluation time. Example reason codes include `SENIOR_TITLE`, `EXPERIENCE_5_PLUS`, `LOCATION_OUT_OF_SCOPE`, and softer `SALARY_BELOW_PREFERENCE`. Missing salary, ambiguous seniority, or unknown posted date is never by itself a hard rejection.

### Score assessment

Each `ScoreAssessment` is immutable and includes job/profile snapshot IDs, component results, raw total, bounded total, recommendation, strong/partial matches, gaps, potential dealbreakers, career value, uncertainty, evidence links, deterministic rule-set version, prompt/model version where applicable, and timestamp.

Initial weights:

| Component | Maximum |
|---|---:|
| Technical match | 3.0 |
| Experience-level match | 2.0 |
| Education/certification match | 1.5 |
| Customer service/communication | 1.0 |
| Location/working arrangement | 1.0 |
| Career-development value | 1.0 |
| Other requirements | 0.5 |
| **Total** | **10.0** |

Each component stores awarded points, maximum, deterministic signals, AI-supported rubric judgement, candidate fact IDs, job evidence, confidence, and explanation. Mandatory unsupported requirements are recorded as gaps/dealbreakers and may cap the recommendation under a versioned policy. Scores round for display only. Freshness and source confidence affect ranking alongside compatibility rather than silently changing the factual match score. The 8.0 threshold creates a review candidate, never an application.

## Applications, statuses, and documents

### `Application`

One record per canonical job with current status, shortlist decision, notes, timestamps, and optimistic version. `ApplicationStatusEvent` appends from/to status, actor (`human` or approved system action), timestamp, and reason. The transition policy allows ordinary forward movement and explicit human withdrawal/reopening; only a human confirmation can create `applied`.

### `GeneratedDocument`

- `id`, `application_id`, `type` (`resume`, `cover_letter`, later supporting material)
- document version, state (`draft`, `validated`, `approved`, `superseded`)
- template ID/hash and output path (not document bytes in the database)
- generator/rule/prompt/model versions and generation timestamp
- input job/profile/score snapshot IDs
- ordered candidate fact IDs and story IDs used (claim manifest)
- content hash, validation results, human approval actor/time

Documents are immutable artefacts: edits create a new version. `DocumentClaim` maps each generated claim or paragraph to candidate fact IDs and records transformations. Export is blocked if a factual claim lacks permitted, verified provenance. Approval means approved for manual use, not submitted.

## Storage and privacy

SQLite holds canonical operational data; YAML holds candidate truth; raw payloads and DOCX files live in ignored directories referenced by opaque paths. Enforce foreign keys, UTC timestamps, uniqueness/idempotency constraints, migrations, and indexes for status, posted/discovered time, source IDs, and duplicate features. Do not store secrets in SQLite or YAML; use environment/keychain configuration later.
