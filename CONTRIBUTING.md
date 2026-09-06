# Contributing

Thanks for your interest in this automation portfolio.

## Scope

This repository contains independent Python automation projects. Each project should remain modular, testable, and runnable from its own project directory.

## Before opening a change

1. Keep changes focused on a single project or repository-level concern.
2. Follow the existing project structure and naming conventions.
3. Add or update tests when behavior changes.
4. Run the relevant test suite locally with `python -m pytest -q`.
5. Do not commit secrets, virtual environments, logs, caches, or generated output.
6. Update the relevant README when setup, behavior, architecture, or usage changes.

## Commit guidance

Use concise commit messages that describe the change clearly, for example:

```text
Add monthly revenue export to ReportFlow
Fix validation for duplicate order IDs
Improve KnowledgeBase-AI retrieval documentation
```

## Security

If you discover a security issue involving credentials or sensitive data, do not publish the secret in an issue. Remove exposed credentials immediately and use a secure communication channel with the repository owner.
