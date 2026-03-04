---
name: statsig-dashboard
description: Create or read Statsig dashboards through the Console API. Use when building a valid `POST /console/v1/dashboards` body, reading `GET /console/v1/dashboards/{id}` into a create-compatible shape, or appending or replacing dashboard widgets through the related widget endpoints.
---

# Create Statsig Dashboard

Build valid dashboard API requests for the console v1 dashboards API and execute them with the bundled scripts.

Read `references/dashboard-api.md` for the exact field-level schema, supported values, and ready-to-edit examples.

The command examples below assume you are running from this skill directory.

## Quick Start

1. Export the API key:
   `export STATSIG_CONSOLE_API_KEY="..."`
2. Save the request body to a JSON file.
3. Run the matching script:

```bash
python3 scripts/create_dashboard.py \
  --body-file /tmp/dashboard.json
```

## Companion Scripts

- `scripts/create_dashboard.py`: create a new dashboard with `POST /console/v1/dashboards`
- `scripts/read_dashboard.py`: fetch a dashboard and print a create-compatible shape by default using `GET /console/v1/dashboards/{id}`
- `scripts/add_dashboard_widgets.py`: append widgets with `POST /console/v1/dashboards/{id}/widgets`
- `scripts/replace_dashboard_widgets.py`: replace all widgets with `PUT /console/v1/dashboards/{id}/widgets`

## Workflow

1. Choose the correct endpoint:
   - create a dashboard: `create_dashboard.py`
   - read a dashboard in create-compatible shape: `read_dashboard.py`
   - append widgets: `add_dashboard_widgets.py`
   - replace all widgets: `replace_dashboard_widgets.py`
2. Build the matching request body for the chosen endpoint.
3. Include only supported fields:
   - `name`
   - `description`
   - `defaults`
   - `widgets`
4. Map each requested widget to one of the supported widget types:
   - `header`
   - `text`
   - `timeseries`
   - each widget may include optional `width` and `height`
5. For `timeseries`, enforce the query contract exactly:
   - include exactly one of `source` or `sources`
   - use `type: "event"` for each source
   - include `aggregation`
   - only use supported filter operators and chart types
   - if the user wants to group by or filter by event value, use `!statsig_value` rather than `value`
6. Execute the matching script.
7. Return the API response, or summarize the created dashboard ID or widget IDs if that is all the user needs.

## Service Filters

When a widget needs to scope to a Statsig service, prefer filtering on:

```json
{
  "property": {
    "key": "custom.service",
    "column": "user_object"
  },
  "operator": "EQ",
  "values": ["service-name"]
}
```

Do not default to bare `service` when building dashboard widgets. In Statsig event payloads this is commonly nested under `user_object.custom`, so `custom.service` is the safer default.

## OTEL Aggregations

When a widget targets a metric that may come from OTEL, sample the metric first and inspect `company_metadata.__metric_type`.

- If `__metric_type` is present, treat the metric as OTEL-backed and prefer the matching OTEL aggregation family instead of the plain aggregation.
- If `__metric_type` is absent on a representative sample, treat it as a non-OTEL metric and use the normal aggregation types.

Preferred mapping:

- `__metric_type = "gauge"`: use `OTEL_GAUGE__AVG`, `OTEL_GAUGE__MAX`, `OTEL_GAUGE__MIN`, or `OTEL_GAUGE__SUM`
- `__metric_type = "counter"`: use `OTEL_COUNTER__SUM`, `OTEL_COUNTER__AVG`, `OTEL_COUNTER__MIN`, or `OTEL_COUNTER__MAX`
- `__metric_type = "histogram"`: use the OTEL histogram aggregations documented in `references/dashboard-api.md`

Keep the aggregation intent the same when converting:

- average-style widgets should become `OTEL_GAUGE__AVG` instead of `AVG`
- max-style widgets should become `OTEL_GAUGE__MAX` instead of `MAX`

## Guardrails

- Do not invent unsupported widget types such as tables.
- Do not include layout fields when creating a dashboard. The create endpoint does not accept widget positions.
- Do not include `row` or `column`. The API currently supports widget sizing via `width` and `height`, not explicit placement.
- Do not include `id` in the create request body.
- If the user gives you a dashboard from `GET /console/v1/dashboards/{id}`, reuse that create-compatible shape but remove `id`.
- Do not use the create endpoint when the user wants to mutate an existing dashboard.
- Prefer markdown formatting in text widgets so the content is readable and structured.

## Examples

Minimal dashboard:

```bash
cat > /tmp/dashboard.json <<'JSON'
{
  "name": "Checkout Overview"
}
JSON

python3 scripts/create_dashboard.py \
  --body-file /tmp/dashboard.json
```

Read an existing dashboard into a reusable create payload:

```bash
python3 scripts/read_dashboard.py \
  --dashboard-id dash_123
```

Append widgets to an existing dashboard:

```bash
python3 scripts/add_dashboard_widgets.py \
  --dashboard-id dash_123 \
  --body-file /tmp/add-widgets.json
```

Replace all widgets on an existing dashboard:

```bash
python3 scripts/replace_dashboard_widgets.py \
  --dashboard-id dash_123 \
  --body-file /tmp/replace-widgets.json
```

## Script Notes

- All scripts read `STATSIG_CONSOLE_API_KEY` from the environment.
- All scripts default `STATSIG_API_VERSION` to `20240601`.
- Pass `--api-version` or set `STATSIG_API_VERSION` to override that default.
- All scripts default to `https://api.statsig.com/console/v1/dashboards`.
- All scripts send the Console API key in the `statsig-api-key` header.
- All scripts send the configured `statsig-api-version` header.
- `create_dashboard.py`, `add_dashboard_widgets.py`, and `replace_dashboard_widgets.py` accept:
  - `--body-file`
  - `--body`
  - stdin
- `read_dashboard.py`, `add_dashboard_widgets.py`, and `replace_dashboard_widgets.py` require `--dashboard-id`.
- All scripts support `--dry-run`.
- All scripts support `--raw`.
- `read_dashboard.py` prints the raw GET response only when `--raw` is set. Otherwise it unwraps `data` and removes `id`.
