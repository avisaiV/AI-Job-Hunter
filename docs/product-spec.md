# Product specification

## Purpose and success criteria

AI Job Hunter is a personal system that finds recently posted Sydney IT roles, removes clearly unsuitable roles cheaply, evaluates plausible roles against the candidate's real background, and prepares truthful application drafts for the best opportunities. Success means fewer, better-supported applications, not maximum throughput.

The system is advisory. It must never submit an application. The candidate reviews every score, explanation, resume, cover letter, and submission decision.

## Target roles and constraints

Primary targets are IT support officer/analyst, service or help desk analyst, desktop/technical/ICT support, junior systems or IT support, and graduate IT/technology roles. Junior cybersecurity and SOC analyst level 1 roles are secondary targets.

- **Geography:** Sydney CBD, Western Sydney, South West Sydney, and reasonable Sydney hybrid roles.
- **Seniority:** graduate, junior, entry-level, and generally 0–2 years. A 1–3 year request is not an automatic rejection when other evidence is strong.
- **Negative signals:** senior, lead, manager, architect, clear 5+ year requirements, or mandatory requirements substantially beyond the candidate profile.
- **Freshness:** prefer roles posted in the last 48 hours; consider roles up to seven days old. Unknown posted dates remain eligible but carry uncertainty.
- **Salary:** approximately AUD 65,000 or above when disclosed. Missing salary is neutral, not a rejection.
- **Opportunity threshold:** a validated compatibility score of 8.0 or higher is a serious application opportunity, not automatic approval.

## Functional flow

1. Ingest job-alert emails, approved APIs/public feeds, user-supplied jobs, and permitted employer career pages through source adapters. Do not directly scrape or automate SEEK, LinkedIn, or Indeed contrary to their terms.
2. Retain source lineage and a minimally necessary raw snapshot, then normalise and validate a common job record.
3. Resolve exact and probable duplicates while retaining all source sightings.
4. Apply explainable deterministic eligibility and deprioritisation rules before paid AI calls.
5. Produce a 0.0–10.0 component score plus evidence, gaps, dealbreakers, career value, uncertainty, and an apply recommendation.
6. For user-approved strong opportunities, tailor the existing resume and create a company-specific cover-letter draft using only supported candidate facts.
7. Export versioned drafts for human review and track the application through its lifecycle.
8. Present jobs, source history, scores, reasoning, documents, and status in a simple dashboard.

## Candidate truth policy

Candidate data is the exclusive authority for claims about the candidate. Every usable claim must identify its provenance category and supporting record. The system must distinguish professional employment, freelance/casual work, academic projects, certification labs, conceptual knowledge, and end-user use. A missing fact is a gap, not permission to infer one.

Resume tailoring may reorder supported skills, adjust the career profile, rephrase existing experience without changing meaning, emphasise relevant projects, and use truthful equivalent terminology. It must preserve the base document's identity and structure where practical. It must not add hidden keywords, fabricate dates or duties, claim administration from ordinary product use, or turn lab/informal/POS use into enterprise support experience.

Cover letters use Australian English and a relaxed, concise, professional early-career voice. They must be meaningfully specific to the role or company, draw selectively from verified stories, avoid generic AI introductions and corporate fluff, not repeat the resume, and use no em dashes.

## Application lifecycle

Canonical statuses are `discovered`, `shortlisted`, `preparing`, `ready_to_apply`, `applied`, `interview`, `rejected`, `offer`, and `withdrawn`. All changes are recorded in an append-only history with actor, timestamp, and optional note. `applied` must only result from explicit human confirmation. Terminal statuses may be reopened only through an explicit human action.

## Out of scope for the first release

- automatic form completion or application submission
- prohibited scraping or bypassing access controls
- multi-user accounts, distributed services, and cloud orchestration
- autonomous candidate-profile edits based on generated text
- fabricated, hidden, or deceptive ATS optimisation
