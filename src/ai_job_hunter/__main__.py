"""Allow ``python -m ai_job_hunter`` to run the CLI."""

from ai_job_hunter.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
