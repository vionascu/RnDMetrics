# Troubleshooting

## No data in charts
- Ensure `metrics collect` ran successfully and `data/metrics.db` exists.
- Check `output/latest.json` and `output/history.json` are created.

## GitLab API errors
- Confirm the token has `read_api` access.
- Ensure `project_id` is correct (numeric ID preferred).

## Repo metrics missing
- Ensure `collection.repo_path` is writable and reachable.
- If cloning is disabled, only API-based metrics will be available.
