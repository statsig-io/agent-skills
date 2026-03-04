# Experimental

This repository is experimental.

It contains public agent skills and supporting scripts for working with Statsig.

## Install

Install this repo with the Vercel `skills` CLI:

```bash
npx skills add statsig-io/agent-skills --skill statsig-dashboard
```

Useful variants:

- List installable skills: `npx skills add statsig-io/agent-skills --list`
- Install globally for your user: `npx skills add -g statsig-io/agent-skills --skill statsig-dashboard`
- Install every skill in this repo: `npx skills add statsig-io/agent-skills --all`

After installation, compatible agents can discover the skill from its metadata.

## Requirements

- `STATSIG_CONSOLE_API_KEY` for Statsig Console API access
- Python 3 if you want to run the bundled helper scripts directly

## Included Skill

- `statsig-dashboard`: create dashboards, read dashboards into reusable create payloads, and add or replace dashboard widgets through the Statsig Console API

## Structure

- `*/SKILL.md`: skill-specific instructions
- `*/scripts/`: helper scripts used by a skill
- `*/references/`: supporting reference material

## Notes

- Review skills before installing them, especially when they include executable scripts.
- This repo currently targets the Statsig Console dashboards API.

## License

See `LICENSE`.
