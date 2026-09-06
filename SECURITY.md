# Security Policy

## Supported scope

This repository is an actively developed portfolio of Python automation projects. Security fixes are handled on the default branch for the current codebase.

## Reporting a vulnerability

Please do not include passwords, API keys, tokens, private files, or other secrets in public issues.

If you identify a security concern, contact the repository owner privately with:

- the affected project and file or component;
- a clear description of the issue;
- safe reproduction steps; and
- any suggested mitigation.

## Secret handling

Never commit credentials to the repository. Use environment variables and `.env` files locally, and commit only safe examples such as `.env.example` files where applicable.
