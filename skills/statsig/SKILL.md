---
name: statsig
description: Use the Statsig MCP to inspect and manage Statsig entities such as gates, experiments, dynamic configs, segments, metrics, audit logs, and results.
---

# Statsig MCP

Use the Statsig MCP server to inspect and manage Statsig entities, review rollout state, check experiment or gate results, inspect audit history, and answer configuration questions.

## Connection and setup

First check for an available Statsig MCP connection and inspect its advertised tools. Use an existing connection, including v1, according to its actual schemas; installing this skill does not migrate the server or refresh the client's tool catalog.

For a new connection, use `https://api.statsig.com/v3/mcp`. For example, add this server to `~/.codex/config.toml`, replacing the placeholder locally with a Console API key:

```toml
[mcp_servers.statsig]
command = "npx"
args = ["--yes", "mcp-remote", "https://api.statsig.com/v3/mcp", "--header", "statsig-api-key: console-YOUR-CONSOLE-API-KEY"]
```

Use a Statsig Console API key with the permissions needed for the task (read-only for viewing, write for changes), created under Settings -> Keys & Environments. Do not ask the user to paste credentials into chat. Restart Codex after editing its configuration. Other clients should use their supported remote MCP setup with the same v3 URL.

For existing connections and reconnect guidance, read [the MCP reference](references/statsig-mcp.md#existing-connections-and-migration).

## Workflow

1. Identify the task and target resource. If the target is ambiguous, clarify before searching broadly or making changes.
2. Inspect the connected server's advertised tools and schemas. On v3, use `get_context` when project, permissions, or review requirements need clarification. Use list/search tools to resolve names to identifiers, then read the target's details.
3. Use the matching advertised tool. If v3 does not directly expose the needed operation, use `discover_tools` before declaring it unavailable. Follow the discovery and execution workflow in [the MCP reference](references/statsig-mcp.md#v3-operation-discovery).
4. For results or rollout questions, inspect the relevant results and audit history; supply the required rule, group, and date identifiers from the actual schemas.
5. For changes, stay within the user's requested scope and the connection's permissions. Read before replacing an object and preserve unrelated fields. Honor required reviews and destructive acknowledgements; do not infer destructive intent from a request to inspect or analyze.
6. Check the tool result for success or errors, then summarize the findings or changes and any unresolved limitations. A created review is a proposed change, not an applied update.

## Reference

Read [Statsig MCP capabilities and migration](references/statsig-mcp.md) for tool selection, discovery, write safeguards, and existing-client compatibility.
