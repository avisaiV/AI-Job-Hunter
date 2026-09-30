# AI Job Hunter

A planned personal, local-first assistant for discovering suitable early-career IT jobs in Sydney, evaluating them honestly against a structured candidate profile, and preparing application drafts for human review.

This repository currently implements **Milestone M1 infrastructure only**: an installable
Python package, configuration, shared vocabulary, safe logging, a diagnostic CLI, tests, and
CI. No candidate profile, job ingestion, database, matching, AI analysis, document generation,
scraping, dashboard, scheduling, or application automation has been implemented.

## Design goals

- truthful matching backed by candidate-fact provenance
- transparent, reproducible scoring
- modular and terms-compliant job sources
- strict separation of untrusted external content from trusted instructions
- manual review and submission of every application
- a maintainable single-user system without unnecessary cloud infrastructure

## Documentation map

- [Product specification](docs/product-spec.md)
- [Architecture](docs/architecture.md)
- [Data model and interfaces](docs/data-model.md)
- [Security and privacy](docs/security.md)
- [Implementation roadmap](docs/roadmap.md)
- [Decision log and open decisions](docs/decisions.md)

## Requirements

- Python 3.11 or newer
- Git

The project uses standard `venv` and `pip`; no separate dependency manager is required.

## Local setup

```bash
git clone <repository-url>
cd AI-Job-Hunter
python -m venv .venv
```

Activate the environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the package and development tools:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Configuration and CLI

Defaults place private/runtime content in ignored repository-local directories. Copy
`.env.example` to `.env` only when overrides are needed; never commit `.env` or private data.

```bash
ai-job-hunter --help
ai-job-hunter doctor
```

`doctor` validates configuration, creates the configured private directories, reports Python
and package versions, and checks repository-local private paths with `git check-ignore`. It does
not read or display candidate files.

Supported variables are `AJH_ENVIRONMENT`, `AJH_LOG_LEVEL`, `AJH_RUNTIME_DATA_DIR`,
`AJH_CANDIDATE_DATA_DIR`, `AJH_TEMPLATE_DIR`, `AJH_OUTPUT_DIR`, and `AJH_LOG_DIR`.

## Development checks

```bash
ruff check .
mypy src tests
python -m pytest
detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
git diff --check
```

On PowerShell, pass the tracked paths to `detect-secrets-hook` using:

```powershell
detect-secrets-hook --baseline .secrets.baseline (git ls-files)
```

GitHub Actions runs linting, strict type checking, tests with coverage, and the secret scan on
pull requests and pushes to `main`.

## Private directories

The following defaults are intentionally ignored by Git and are created by `doctor`:

- `candidate/` for future private candidate data
- `templates/` for private source CV and letter templates
- `data/` for runtime state and future databases
- `output/` for generated documents
- `logs/` for runtime logs

`raw/` and `tmp/` are also ignored for future imported payloads and temporary files. Only
explicitly synthetic or redacted examples may ever be tracked.

After M1 review, development should stop until the owner approves beginning M2.
