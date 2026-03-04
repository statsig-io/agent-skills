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
        description="Add widgets via /console/v1/dashboards/{id}/widgets",
    )
    parser.add_argument(
        "--dashboard-id",
        required=True,
        help="Dashboard ID to update",
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="Path to a JSON file containing the add-widgets body",
    )
    parser.add_argument(
        "--body",
        default=None,
        help="Inline JSON string containing the add-widgets body",
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
    args = parser.parse_args()

    if args.body_file and args.body:
        parser.error("Provide only one of --body-file or --body")

    return args


def build_url(endpoint: str, dashboard_id: str) -> str:
    encoded_dashboard_id = urllib.parse.quote(dashboard_id, safe="")
    return f"{endpoint.rstrip('/')}/{encoded_dashboard_id}/widgets"


def read_payload_text(args: argparse.Namespace) -> str:
    if args.body is not None:
        return args.body

    if args.body_file is not None:
        with open(args.body_file, encoding="utf-8") as handle:
            return handle.read()

    if sys.stdin.isatty():
        raise ValueError("Provide --body-file, --body, or pipe JSON on stdin")

    return sys.stdin.read()


def parse_payload(payload_text: str) -> dict:
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON body: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("Add-widgets body must be a JSON object")

    widgets = payload.get("widgets")
    if not isinstance(widgets, list) or len(widgets) == 0:
        raise ValueError("Add-widgets body must include non-empty `widgets`")

    return payload


def format_dry_run(
    url: str,
    has_api_key: bool,
    api_version: str,
    payload: dict,
) -> str:
    request_preview = {
        "method": "POST",
        "endpoint": url,
        "headers": {
            "Content-Type": "application/json",
            "statsig-api-key": "***redacted***" if has_api_key else "<missing>",
            "statsig-api-version": api_version,
        },
        "body": payload,
    }
    return json.dumps(request_preview, indent=2, sort_keys=True)


def main() -> int:
    args = parse_args()

    try:
        payload_text = read_payload_text(args)
        payload = parse_payload(payload_text)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    api_key = args.api_key or os.environ.get("STATSIG_CONSOLE_API_KEY")
    api_version = args.api_version or os.environ.get(
        "STATSIG_API_VERSION",
        DEFAULT_API_VERSION,
    )
    url = build_url(args.endpoint, args.dashboard_id)

    if args.dry_run:
        print(format_dry_run(url, api_key is not None, api_version, payload))
        return 0

    if not api_key:
        print("Missing STATSIG_CONSOLE_API_KEY (or pass --api-key)", file=sys.stderr)
        return 2

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
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
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print(raw)
        return 0

    print(json.dumps(parsed, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
