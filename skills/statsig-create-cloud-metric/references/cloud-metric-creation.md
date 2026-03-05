# Cloud Metric Creation

Use this file only for Statsig Cloud projects.

## Supported Cloud Metric Types

- Event count
- User count
- Aggregation (sum or average)
- Ratio
- Funnel


## Payload Shape

Cloud metrics are defined with top-level fields (not under `warehouseNative`):

- metricEvents
- funnelEventList
- funnelCountDistinct
- metricComponentMetrics

## Requested Metric Kind -> API `type`

- Event count -> `event_count_custom`
- User count -> `event_user`
- Aggregation sum -> `sum`
- Aggregation mean/avg -> `mean`
- Ratio -> `ratio`
- Funnel -> `funnel`
- Composite -> `composite`
- Composite sum -> `composite_sum`

## Runtime Required Inputs by Cloud Type

- `sum`, `mean`, `event_count_custom`:
  - `unitTypes` must be non-empty
  - `metricEvents` must be non-empty
- `ratio`:
  - `unitTypes` must be non-empty
  - `metricEvents` must be non-empty
- `event_user`:
  - every metric event must include `criteria`
- `funnel`:
  - `funnelCountDistinct` is required (`events` or `users`)
  - `funnelEventList` must include at least 2 events
  - event types must match `funnelCountDistinct`
- `composite`:
  - `unitTypes` must be non-empty
- `composite_sum`:
  - `unitTypes` must be non-empty
  - `metricComponentMetrics` must contain more than 1 metric

## Example (Event Count)

{
  "name": "Checkout Started",
  "type": "event_count_custom",
  "unitTypes": ["userID"],
  "metricEvents": [
    {
      "name": "checkout_started",
      "type": "value",
      "criteria": []
    }
  ]
}
