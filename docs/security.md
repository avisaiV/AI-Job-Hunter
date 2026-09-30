# Security, privacy, and trust boundaries

## Trust model

**Trusted control data:** reviewed application code, versioned configuration, candidate facts explicitly entered/approved by the user, document templates, and system/developer prompts.

**Untrusted data:** all emails, advertisements, webpages, employer copy, APIs, attachments, external documents, URLs, and model-produced output. Source reputation does not make its content an instruction.

External data may describe a vacancy. It may not change policies, invoke tools, select files, request secrets, edit candidate truth, modify score weights, approve documents, or transition an application to `applied`.

## Required controls

1. **Acquire:** allowlist adapter operations and protocols; enforce timeouts, byte limits, content types, rate limits, and redirects; prevent access to loopback, link-local, private-network, metadata-service, and `file:` targets (SSRF controls). Do not execute attachments, scripts, macros, or HTML.
2. **Quarantine and parse:** retain minimal raw content outside the served web root; parse email/HTML as data with safe libraries; strip active content for display; preserve hashes and lineage. Malformed content fails closed per item.
3. **Normalise:** validate lengths, URLs, enums, timestamps, and schema. Separate data fields from control/configuration. Never interpolate external content into executable templates, SQL, shell commands, paths, or trusted prompt sections.
4. **Analyse:** send only the minimum job text and non-sensitive candidate projection. Delimit and label job content as untrusted. Use fixed prompts, structured output schemas, no model tools, and least-privilege provider credentials. Treat model output as untrusted and validate types, evidence references, ranges, and allowed fact IDs.
5. **Generate:** construct a claim manifest from approved candidate facts before prose. Reject unsupported claims, provenance escalation, hidden text, instruction-like payloads, and external links not explicitly reviewed. Show document diffs and require human approval.
6. **Present:** escape/sanitise content in Streamlit; do not render arbitrary HTML. Protect local access if bound beyond localhost. Avoid sensitive logs and offer raw-payload retention/deletion controls.
7. **Act:** there is no application-submission capability. Status `applied` requires an explicit human gesture and audit event.

Prompt-injection phrases such as “ignore previous instructions”, requests to read environment variables, or requests to upload files remain ordinary quoted job text. Detection can flag a record for review but is not the primary defence; capability isolation is.

## Secrets and credentials

No credentials are required during architecture work. Potential later secrets/services are:

- an AI provider API key, unless a local model is chosen
- read-only IMAP/OAuth credentials or a dedicated mailbox for job alerts
- permitted job-board/public API credentials where offered
- optional document conversion tooling and, much later, optional notification credentials

Use environment variables backed by an OS keychain or a local ignored `.env` for development, provide only `.env.example` names, scope tokens minimally, and never commit/log/store them in prompts. Email access should be read-only and ideally restricted to a dedicated alert mailbox/folder.

## Privacy and retention

Candidate files, resumes, contact details, emails, the runtime database, raw payloads, model request/response bodies, and generated documents are private and ignored by Git. Redacted synthetic fixtures are the only test data committed. Define configurable retention for raw emails/pages and delete them once lineage/audit needs permit. Before using a hosted model, the user must decide which candidate fields may leave the device and review provider retention/training settings.

## Security validation

Maintain regression fixtures containing prompt injection, oversized input, malicious HTML, tracking/redirect URLs, unsupported schemes, traversal filenames, malformed model JSON, fabricated fact IDs, hidden-text attempts, and provenance escalation. Test that no case can read local files/secrets, change configuration/status, or create an approved document. Dependency scanning and secret scanning join the full-suite checks during hardening.
