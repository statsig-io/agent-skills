# Experimental

This repository is experimental.

It contains public agent skills and supporting scripts for working with Statsig.

## Install

Install this repo with the Vercel `skills` CLI:

```bash
npx skills add statsig-io/agent-skills
```

Useful variants:

- List installable skills: `npx skills add statsig-io/agent-skills --list`
- Install globally for your user: `npx skills add -g statsig-io/agent-skills --skill statsig-dashboard`
- Install every skill in this repo: `npx skills add statsig-io/agent-skills --all`

After installation, compatible agents can discover the skill from its metadata.

## Requirements

- `STATSIG_CONSOLE_API_KEY` for Statsig Console API access
- Python 3 if you want to run the bundled helper scripts directly

## Included Skills

- `statsig`: query Statsig experiments, gates, and dynamic configs through the Statsig MCP
- `statsig-dashboard`: create dashboards, read dashboards into reusable create payloads, and add or replace dashboard widgets through the Statsig Console API
- `statsig-create-cloud-metric`: draft or execute Statsig Cloud metric creation requests through the Statsig Console API

## Structure

- `skills/*/SKILL.md`: skill-specific instructions
- `skills/*/scripts/`: helper scripts used by a skill
- `skills/*/references/`: supporting reference material

## Notes

- Review skills before installing them, especially when they include executable scripts.
- The `statsig` skill defaults new MCP connections to `https://api.statsig.com/v3/mcp` and follows the advertised tools for existing connections, including v1. Installing or updating a skill does not migrate an MCP connection; see [connection and migration guidance](skills/statsig/references/statsig-mcp.md#existing-connections-and-migration).
- The dashboard and Cloud metric skills use the Console API; their `/console/v1` endpoints are unchanged.

## License

See `LICENSE`.
