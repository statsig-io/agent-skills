# Statsig MCP setup and capabilities

## Setup (Codex CLI / IDE extension)

See `statsig-mcp/SKILL.md` for the Codex MCP config snippet and API key notes.

## Current MCP capabilities

The Statsig MCP currently supports both read and write workflows across the main Statsig object types, along with audit and results lookups.

### Experiments (A/B tests)

- Get_List_of_Experiments: list experiments with optional status filtering
- Get_Experiment_Details_by_ID: experiment details including groups and parameters
- Get_Experiment_Results: fetch experiment metric results for a control/test comparison
- Create_Experiment: create a new experiment
- Update_Experiment_Entirely: replace an experiment configuration

### Gates (feature flags)

- Get_List_of_Gates: list gates/flags with optional type filtering (STALE, PERMANENT, etc.)
- Get_Gate_Details_by_ID: full gate configuration details
- Get_Gate_Results: fetch gate metric results for a specific rule
- Create_Gate: create a new gate/flag
- Update_Gate_Entirely: replace a gate configuration

### Dynamic configs

- Get_List_of_Dynamic_Configs: list dynamic config objects
- Get_Dynamic_Config_Details_by_ID: retrieve config details
- Create_Dynamic_Config: create a new config
- Update_Dynamic_Config_Entirely: replace a config configuration

### Segments

- Get_List_of_Segments: list segments
- Get_Segment_by_ID: inspect a segment definition
- Create_Segment: create a segment
- Update_Segment: update a segment or append data for supported segment types

### Metrics and related objects

- Get_List_of_Metrics: list metrics
- Get_Metric_Definition_by_ID: inspect a metric definition
- Get_List_of_Metric_Sources: list available metric sources
- Get_List_of_Param_Stores: list param stores
- Get_Param_Store_Details_by_Id: inspect a param store

### Audit and search tools

- Get_Audit_Logs: inspect recent changes, filtered by id, tags, and date range
- Search / Fetch: search Statsig MCP data and retrieve full matching documents

## Example prompts

- "List all my active experiments"
- "What gates are currently stale?"
- "Show me the configuration for the dynamic config 'dynamic-config'"
- "Show me details about the experiment called 'new-checkout-flow'"
- "Show recent audit log entries for this gate"
- "Compare the latest results for the control and treatment groups in this experiment"
- "List segments and show me the rules for one of them"
- "Create a dynamic config for this JSON payload"
- "Update this gate without changing its other rules"
- "Find the metric definition for this KPI"

## Notes

- The MCP supports GET and POST requests.
- For updates, gather the current object first when the endpoint expects a full replacement.
- Pay attention to required IDs, rule IDs, control/test group names, and date parameters on results endpoints.
- For more docs, see https://docs.statsig.com/llms.txt
