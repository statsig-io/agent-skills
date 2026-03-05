# Create Metric API (Shared Contract)

## Endpoint

POST https://statsigapi.net/console/v1/metrics

## Required Headers

- Content-Type: application/json
- STATSIG-API-KEY: <console api key>

## Base Required Body Fields (DTO)

- name (string, 4-200)
- type (enum)

## Common Optional Body Fields

- unitTypes (array of strings)
- description (string)
- tags (string[] or string)
- directionality (`increase` | `decrease`)
- isPermanent (bool)
- isReadOnly (bool)
- isVerified (bool)
- team (string | null)
- teamID (string | null)
- dryRun (bool)

## Allowed `type` Enum for Create

`ratio`, `mean`, `event_count_custom`, `event_user`, `funnel`, `composite`, `composite_sum`, `sum`, `undefined`, `percentile`

## Criteria Contract (`metricEvents[].criteria`)

Criteria object shape:

- `type`: `value` | `metadata` | `user` | `user_custom`
- `condition`: `in` | `not_in` | `=` | `>` | `<` | `>=` | `<=` | `is_null` | `non_null` | `contains` | `not_contains` | `sql_filter` | `starts_with` | `ends_with` | `after_exposure` | `before_exposure`
- `column`: string (optional for conditions like `sql_filter`)
- `values`: string[] (optional for null checks and some operators)
- `nullVacuousOverride`: boolean (optional)

Important:

- Use exact enum literals for `condition` (for example `=` not `eq`).

## Contract Notes

- Cloud projects use non-warehouse types such as `event_count_custom`, `sum`, `mean`, `ratio`, `funnel`, `composite`, and `composite_sum`.
- DTO-level optional fields can still be runtime-required by mutation validation based on metric type and aggregation.

## Shell Quoting (Important)

If your payload includes SQL with single quotes (for example `JSON_VALUE(company_metadata, '$.route') = '/onboarding'`), do not use inline single-quoted JSON (`-d '...'`).

Use heredoc payloads:

```bash
curl -X POST "https://statsigapi.net/console/v1/metrics" \
  -H "Content-Type: application/json" \
  -H "STATSIG-API-KEY: $STATSIG_API_KEY" \
  --data-binary @- <<'JSON'
{
  "name": "example_metric",
  "type": "event_count_custom",
  "unitTypes": ["userID"],
  "metricEvents": [
    {
      "name": "checkout_started",
      "type": "value",
      "criteria": [
        {
          "type": "metadata",
          "condition": "sql_filter",
          "values": ["JSON_VALUE(company_metadata, '$.route') = '/onboarding'"]
        }
      ]
    }
  ]
}
JSON
```
