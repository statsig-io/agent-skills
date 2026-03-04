# Dashboard API Reference

This file is the self-contained request and response contract for the dashboard create, read, append-widgets, and replace-widgets console v1 endpoints.

The contract in this reference is aligned to the Statsig Console API OpenAPI docs for `20240601` and the corresponding controller, DTO, and tests in the Statsig repo.

## Create Endpoint

- Method: `POST`
- Path: `/console/v1/dashboards`
- Header: `statsig-api-key: <console_api_key>`
- Header: `statsig-api-version: 20240601` by default, or an explicitly configured override
- Success response:

```json
{
  "message": "Dashboard Created Successfully",
  "data": {
    "id": "dashboard_id"
  }
}
```

## Read Endpoint

- Method: `GET`
- Path: `/console/v1/dashboards/{id}`
- Header: `statsig-api-key: <console_api_key>`
- Header: `statsig-api-version: 20240601` by default, or an explicitly configured override
- Success response:

```json
{
  "message": "Dashboard Read Successfully",
  "data": {
    "id": "dashboard_id",
    "name": "My Dashboard",
    "description": "Optional description",
    "defaults": {
      "date": {
        "value": 14,
        "unit": "day"
      },
      "granularity": "daily"
    },
    "widgets": []
  }
}
```

The bundled `read_dashboard.py` script unwraps `data` and removes `id` by default so its output is directly reusable as a create-compatible template.

## Create Request Body

```json
{
  "name": "My Dashboard",
  "description": "Optional description",
  "defaults": {
    "date": {
      "value": 14,
      "unit": "day"
    },
    "granularity": "daily"
  },
  "widgets": [
    {
      "type": "header",
      "title": "Section header",
      "color": "#1d4ed8",
      "width": 12,
      "height": 1
    },
    {
      "type": "text",
      "title": "Overview",
      "content": "## Summary\n\n- Key finding one\n- Key finding two",
      "width": 6,
      "height": 3
    },
    {
      "type": "timeseries",
      "title": "Checkout Started",
      "description": "Optional description",
      "color": "#0f766e",
      "width": 8,
      "height": 5,
      "query": {
        "source": {
          "type": "event",
          "event_name": "checkout_started",
          "filters": [
            {
              "property": {
                "key": "custom.service",
                "column": "user_object"
              },
              "operator": "EQ",
              "values": ["checkout"]
            }
          ]
        },
        "aggregation": {
          "type": "COUNT"
        },
        "group_bys": [
          {
            "key": "platform",
            "column": "company_metadata"
          }
        ],
        "viz": {
          "chart_type": "line"
        }
      }
    }
  ]
}
```

## Field Rules

### Top level

- `name`: required, string, length `1..200`
- `description`: optional, string, max length `10000`
- `defaults`: optional
- `widgets`: optional array

### Defaults

- `defaults.date.value`: positive integer
- `defaults.date.unit`: one of `day`, `week`, `month`
- `defaults.granularity`: one of `auto`, `daily`, `weekly`, `monthly`

### Widget types

All widget types support these optional sizing fields:

- `width`: positive integer, maximum `12`
- `height`: positive integer

#### Header

```json
{
  "type": "header",
  "title": "Section header",
  "color": "#1d4ed8",
  "width": 12,
  "height": 1
}
```

#### Text

```json
{
  "type": "text",
  "title": "Overview",
  "content": "## Summary\n\n- Key finding one\n- Key finding two",
  "width": 6,
  "height": 3
}
```

Guidance:

- Author `content` as markdown so the text widget is readable and structured.
- Prefer headings, bullets, emphasis, and short sections over plain paragraphs.

#### Timeseries

```json
{
  "type": "timeseries",
  "title": "Metric title",
  "description": "Optional description",
  "color": "#0f766e",
  "width": 8,
  "height": 5,
  "query": {
    "source": {
      "type": "event",
      "event_name": "event_name"
    },
    "aggregation": {
      "type": "COUNT"
    }
  }
}
```

Rules:

- include exactly one of `query.source` or `query.sources`
- `width` is optional and must be `1..12` when provided
- `height` is optional and must be a positive integer when provided
- when filtering to a service, prefer `property.key = "custom.service"` with `column = "user_object"` rather than bare `service`
- when filtering by or grouping by event value, use `property.key = "!statsig_value"` or `group_bys[].key = "!statsig_value"` rather than `value`
- when a sampled event shows `company_metadata.__metric_type`, prefer the matching OTEL aggregation family over plain `AVG`, `MAX`, `MIN`, or `SUM`
- every source must be:

```json
{
  "type": "event",
  "event_name": "event_name",
  "filters": []
}
```

- `query.aggregation.type` is required
- `query.aggregation.property` is optional
- `query.unit_type` is optional
- `query.group_bys` is optional
- `query.viz.chart_type` is optional

Supported chart types:

- `line`
- `timeseries-bar`
- `grouped-bar`
- `horizontal-bar`

Supported filter operators:

- `ANY_OF`
- `CONTAINS`
- `EQ`
- `GT`
- `LT`
- `GTE`
- `LTE`
- `IS_NOT_NULL`
- `IS_NULL`
- `NONE_OF`
- `NOT_CONTAINS`
- `SQL_FILTER`
- `STARTS_WITH`
- `ENDS_WITH`
- `AFTER_EXPOSURE`
- `BEFORE_EXPOSURE`
- `IS_TRUE`
- `IS_FALSE`
- `INCLUDED`
- `NOT_INCLUDED`

Supported aggregation types:

- `COUNT`
- `COUNT_DISTINCT`
- `COUNT_DISTINCT_VALUE`
- `COUNT_DISTINCT_VALUE_PER_USER`
- `AVG_COUNT_PER_USER`
- `MAX_COUNT_PER_USER`
- `MIN_COUNT_PER_USER`
- `P50_COUNT_PER_USER`
- `P75_COUNT_PER_USER`
- `P90_COUNT_PER_USER`
- `P95_COUNT_PER_USER`
- `P99_COUNT_PER_USER`
- `SUM`
- `AVG`
- `CONVERSION_RATE`
- `FUNNEL`
- `P50`
- `P75`
- `P90`
- `P95`
- `P99`
- `MAX`
- `MIN`
- `OTEL_COUNTER__SUM`
- `OTEL_COUNTER__AVG`
- `OTEL_COUNTER__MIN`
- `OTEL_COUNTER__MAX`
- `OTEL_HISTOGRAM__COUNT`
- `OTEL_HISTOGRAM__SUM`
- `OTEL_HISTOGRAM__AVG`
- `OTEL_HISTOGRAM__P50`
- `OTEL_HISTOGRAM__P75`
- `OTEL_HISTOGRAM__P90`
- `OTEL_HISTOGRAM__P95`
- `OTEL_HISTOGRAM__P99`
- `OTEL_GAUGE__AVG`
- `OTEL_GAUGE__SUM`
- `OTEL_GAUGE__MIN`
- `OTEL_GAUGE__MAX`

## Related Endpoints

- Read dashboard and transform it into a create-compatible shape: `GET /console/v1/dashboards/{id}`
- Append widgets to existing dashboard: `POST /console/v1/dashboards/{id}/widgets`
- Replace all widgets on existing dashboard: `PUT /console/v1/dashboards/{id}/widgets`

## Add Widgets Endpoint

- Method: `POST`
- Path: `/console/v1/dashboards/{id}/widgets`
- Header: `statsig-api-key: <console_api_key>`
- Header: `statsig-api-version: 20240601` by default, or an explicitly configured override
- Request body:

```json
{
  "widgets": [
    {
      "type": "header",
      "title": "Section header",
      "width": 12,
      "height": 1
    }
  ],
  "defaults": {
    "date": {
      "value": 14,
      "unit": "day"
    },
    "granularity": "daily"
  },
  "max_cols": 12
}
```

Rules:

- `widgets` is required
- `widgets` must contain at least one item
- each widget may include optional `width` and `height`
- `defaults` is optional
- `max_cols` is optional and must be a positive integer when provided

Success response:

```json
{
  "message": "Dashboard Widgets Added Successfully",
  "data": {
    "ids": ["widget_id"]
  }
}
```

## Replace Widgets Endpoint

- Method: `PUT`
- Path: `/console/v1/dashboards/{id}/widgets`
- Header: `statsig-api-key: <console_api_key>`
- Header: `statsig-api-version: 20240601` by default, or an explicitly configured override
- Request body:

```json
{
  "widgets": [
    {
      "type": "header",
      "title": "Replacement header",
      "width": 12,
      "height": 1
    }
  ],
  "defaults": {
    "date": {
      "value": 14,
      "unit": "day"
    },
    "granularity": "daily"
  },
  "max_cols": 12
}
```

Rules:

- `widgets` is required
- `widgets` may be empty to clear the dashboard
- each widget may include optional `width` and `height`
- `defaults` is optional
- `max_cols` is optional and must be a positive integer when provided

Success response:

```json
{
  "message": "Dashboard Widgets Replaced Successfully",
  "data": {
    "ids": ["widget_id"]
  }
}
```
