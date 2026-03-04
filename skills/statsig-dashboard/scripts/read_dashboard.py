#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_ENDPOINT = "https://api.statsig.com/console/v1/dashboards"
DEFAULT_API_VERSION = "20240601"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read a Statsig dashboard via /console/v1/dashboards/{id}",
    )
    parser.add_argument(
        "--dashboard-id",
        required=True,
        help="Dashboard ID to read",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Endpoint base URL (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Override STATSIG_CONSOLE_API_KEY",
    )
    parser.add_argument(
        "--api-version",
        default=None,
        help=f"Override STATSIG_API_VERSION (default: {DEFAULT_API_VERSION})",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw response text instead of pretty JSON",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request that would be sent without making the API call",
    )
    return parser.parse_args()


def build_url(endpoint: str, dashboard_id: str) -> str:
    encoded_dashboard_id = urllib.parse.quote(dashboard_id, safe="")
    return f"{endpoint.rstrip('/')}/{encoded_dashboard_id}"


def format_dry_run(url: str, has_api_key: bool, api_version: str) -> str:
    request_preview = {
        "method": "GET",
        "endpoint": url,
        "headers": {
            "statsig-api-key": "***redacted***" if has_api_key else "<missing>",
            "statsig-api-version": api_version,
        },
    }
    return json.dumps(request_preview, indent=2, sort_keys=True)


def normalize_create_payload(raw: str) -> str:
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Dashboard response must be a JSON object")

    payload = parsed.get("data", parsed)
    if not isinstance(payload, dict):
        raise ValueError("Dashboard response data must be a JSON object")

    normalized = dict(payload)
    normalized.pop("id", None)
    return json.dumps(normalized, indent=2, sort_keys=True)


def main() -> int:
    args = parse_args()
    api_key = args.api_key or os.environ.get("STATSIG_CONSOLE_API_KEY")
    api_version = args.api_version or os.environ.get(
        "STATSIG_API_VERSION",
        DEFAULT_API_VERSION,
    )
    url = build_url(args.endpoint, args.dashboard_id)

    if args.dry_run:
        print(format_dry_run(url, api_key is not None, api_version))
        return 0

    if not api_key:
        print("Missing STATSIG_CONSOLE_API_KEY (or pass --api-key)", file=sys.stderr)
        return 2

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "statsig-api-key": api_key,
            "statsig-api-version": api_version,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8") if exc.fp else ""
        print(f"HTTP {exc.code} from {url}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    if args.raw:
        print(raw)
        return 0

    try:
        print(normalize_create_payload(raw))
    except (json.JSONDecodeError, ValueError):
        print(raw)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
