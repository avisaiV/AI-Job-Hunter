# AI Job Hunter

A planned personal, local-first assistant for discovering suitable early-career IT jobs in Sydney, evaluating them honestly against a structured candidate profile, and preparing application drafts for human review.

This repository currently contains **architecture and planning only**. No job ingestion, AI analysis, document generation, scraping, or application automation has been implemented.

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

Future implementation should begin with Milestone 1 in the roadmap only after this architecture is approved.
