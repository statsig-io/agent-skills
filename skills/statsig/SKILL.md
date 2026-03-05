---
name: statsig
description: Use the Statsig MCP to inspect and manage Statsig entities such as gates, experiments, dynamic configs, segments, metrics, audit logs, and results.
---

# Statsig MCP

## Overview

Use the Statsig MCP server to inspect and manage Statsig entities, review rollout state, check experiment or gate results, inspect audit history, and answer configuration questions.

## Setup Statsig MCP
Important: you must check to see if the Statsig MCP server is running. If not, tell the user how to configure Statsig:

Add this to `~/.codex/config.toml` and replace the API key:

```toml
[mcp_servers.statsig]
command = "npx"
args = ["--yes", "mcp-remote", "https://api.statsig.com/v1/mcp", "--header", "statsig-api-key: console-YOUR-CONSOLE-API-KEY"]
trust_level = "trusted"
```

Use a Statsig Console API key with the permissions you need (read-only for viewing, write for changes). Statsig API keys can be created under Settings -> Keys & Environments. Restart Codex after editing the config.

## Workflow

1. Analyze the user's query and determine the task type: discovery, inspection, results analysis, audit/history review, or config changes.
2. Identify the relevant Statsig entity types and names when possible. Common entities include gates, experiments, dynamic configs, segments, metrics, metric sources, and param stores.
3. Use list or search-style MCP tools first when the user does not provide an exact identifier. Use detail tools once you know the target object.
4. For performance or rollout questions, use the appropriate results endpoints or audit logs to understand behavior over time.
5. For create or update requests, confirm the intended object, preserve required fields, and apply the matching write tool carefully.
6. Summarize the key findings or changes clearly, including the object name, current state, important rules or metrics, and any follow-up actions.

## MCP usage

Use the MCP to fetch, inspect, create, and update Statsig objects. For the current capability list and example prompts, read `references/statsig-mcp.md`.

## Resources

- `references/statsig-mcp.md`: setup notes, MCP capabilities, and example prompts for Statsig MCP.
