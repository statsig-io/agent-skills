# Statsig MCP capabilities and migration

For new-connection setup and API key guidance, see [the Statsig skill](../SKILL.md#connection-and-setup).

## Use the connected server's capabilities

The advertised tool list and input schemas are authoritative. Client prefixes may wrap the names below. Tool availability depends on permissions and the server's serving mode; a short tool list does not imply that the underlying capability is missing.

On v3, common directly advertised tools include:

| Task | Tools |
| --- | --- |
| Project, permission, and review context | `get_context` |
| Find a resource and retrieve the selected result | `search`, `fetch` |
| Gates, experiments, and dynamic configs | `gate_read`, `experiment_read`, `dynamic_config_read` |
| Metrics and metric sources | `metric_read` |
| Audit history and Logs Explorer | `log_read` |
| Authorized creation and updates | `gate_create`, `gate_update`, `experiment_create`, `experiment_update`, `dynamic_config_create`, `dynamic_config_update` |
| Discover and execute other operations | `discover_tools`, `api_read`, `api_write`, `api_destructive` |

Read each schema before calling: consolidated tools may require an explicit `action` and nested `arguments`. Do not translate a v1 tool name or reuse its argument shape by guesswork. Segments, parameter stores, layers, reviews, and other operations may require discovery even when related direct tools are absent.

## V3 operation discovery

1. Call `discover_tools` with `action: "resolve"` and a plain-language `query` describing the intended operation. Include `operationAction` or `category` only when known and supported by the advertised schema. Omit uncertain filters, especially `lane`: updates and review actions can require `api_destructive`.
2. If the result is ambiguous, select the appropriate returned operation (using `action: "list"` to refine the search when useful), then call `action: "get"` with its `operationId`. Do not execute an ambiguous match.
3. Read the selected operation's exact input schema and execution instructions. For a resolved result, use `executeWith.tool` and `executeWith.operationHandle`; for a `get` result, use `lane` as the execution tool and `handle` as its `operationHandle`. Call that tool (`api_read`, `api_write`, or `api_destructive`) with the signed `operationHandle` and schema-valid `arguments`. Do not invent handles, operation IDs, or argument fields, or substitute a different execution lane.
4. Handles are short-lived and credential-bound. If a handle is rejected as expired or invalid, rediscover the same intended operation. Before retrying a mutation whose outcome is unclear, inspect the current state to avoid duplicating a successful change.

Use `resolve_many` only when advertised and when resolving independent steps; dependent mutations still require the results of earlier steps. Discovery is read-only and does not authorize execution. If discovery cannot find an authorized operation, report the limitation rather than bypassing it through another credential or API.

## Changes, reviews, and results

- Read the current object before a full replacement and preserve fields outside the requested change. In particular, `dynamic_config_update` replaces the configuration; discover a partial-update operation for a targeted change such as adding a tag.
- Keep project, environment, resource IDs, and permissions explicit. Read-only access does not authorize writes.
- Supply destructive acknowledgement and reason only when the user's intent authorizes the specific change and the actual tool schema requires them. Some ordinary updates use the destructive lane; its name does not authorize deletion or additional actions.
- Honor review requirements. Discover the supported review workflow when needed, and distinguish creating a review from approving or committing it. Do not bypass an unsupported review workflow or claim the change was applied.
- For results, use the returned resource details and schemas to identify rule IDs, control/test groups, and date parameters. Paginate or narrow large responses as instructed by the tool.
- Inspect structured results and error indicators even when the transport succeeds. Report permission, review, validation, and upstream failures accurately.

## Existing connections and migration

An installed skill and an MCP server connection are separate. Updating this skill does not update an existing plugin's endpoint, a manual client configuration, credentials, or an open conversation's cached tools.

- If connected to v1, continue using its advertised legacy tools and schemas (for example, `Get_List_of_Experiments` if present). Do not call v3-only tools on it. Absence of `discover_tools` alone does not prove a server version; inspect the connection before recommending migration.
- When the user requests migration, update only the Statsig MCP URL from `https://api.statsig.com/v1/mcp` to `https://api.statsig.com/v3/mcp` using the client's supported plugin update or configuration flow. Preserve the existing server identity and unrelated settings. Do not add a second competing Statsig connection.
- Reconnect or restart the client to refresh its tool catalog. OAuth clients may require reauthorization for the new resource URL. Check the advertised tools and perform an appropriate read to confirm the connection; an endpoint edit alone does not confirm success.
- If a conversation retains obsolete tool names, refresh the connection or start a new conversation before retrying with the newly advertised schemas. Do not repeatedly replay stale writes. If authentication or access still fails, report the failure and use the client's supported recovery flow; do not silently switch endpoints or credentials.

The version change applies to the MCP endpoint only. Console API routes such as `/console/v1/metrics` and `/console/v1/dashboards`, used by the separate metric and dashboard skills, retain their API version. OAuth routes are also separate and should not be rewritten by a global version replacement.

## Example prompts

- "List my active experiments and show the results for the checkout experiment."
- "What gates are currently stale?"
- "Show recent audit log entries for this gate."
- "Update this gate without changing its other rules."
- "Add a tag to this dynamic config while preserving its configuration."
- "List segments and show the rules for the selected segment."
- "Find the metric definition for this KPI."

For more Statsig documentation, see [the documentation index](https://docs.statsig.com/llms.txt).
