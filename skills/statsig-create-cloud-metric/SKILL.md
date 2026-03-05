---
name: statsig-create-cloud-metric
description: Create Statsig Cloud metrics via the Console API POST /console/v1/metrics. Use when drafting or executing Create Metric requests for Cloud projects, including required fields and metric type differences.
---

# Statsig Create Cloud Metric API

## Quick Start

1. Confirm the request is for a Cloud project.
2. Collect required inputs: metric name, requested metric kind, and whether to dry run.
3. Open shared contract guidance in references/create-metric-api.md.
4. Open references/cloud-metric-creation.md.
5. Map requested metric kind to API `type` enum using the Cloud reference.
6. Draft a curl request with STATSIG-API-KEY and JSON body.

## Required Inputs

- Metric name (4-200 chars).
- Requested metric kind and API `type` enum.
- Event definitions.
- Filters and optional rollup settings.
- unitTypes when required by the selected Cloud metric type.

## Build the Request

- Always send `POST /console/v1/metrics`.
- Always include `Content-Type: application/json` and `STATSIG-API-KEY`.
- Use `dryRun: true` for validation-first workflows.
- Prefer heredoc payloads (`--data-binary @- <<'JSON'`) instead of inline `-d '...'` JSON when SQL filters include single quotes.
- For Cloud metrics, set top-level fields such as `metricEvents`, `funnelEventList`, and `metricComponentMetrics`.
- For criteria-based filters, only use API-supported `condition` enum values (see references/create-metric-api.md). Do not use aliases like `eq`.
- Confirm enum mapping and required fields from the Cloud reference before finalizing.

## References

- Shared API contract and headers: `references/create-metric-api.md`
- Cloud metric creation details: `references/cloud-metric-creation.md`
