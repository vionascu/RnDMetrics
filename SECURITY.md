# Security

- Source repository is never modified.
- GitLab API is used in read-only mode.
- Access token is read from `token_env` and never logged.
- No secrets are written to disk or exported JSON.
- CI variables must be masked and protected.

## CI guidance
- Use a masked variable named in `config.yml` (`GITLAB_TOKEN` by default).
- Avoid echoing environment variables or debug logs.
