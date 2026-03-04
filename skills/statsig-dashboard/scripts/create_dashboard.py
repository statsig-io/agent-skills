#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_ENDPOINT = "https://api.statsig.com/console/v1/dashboards"
DEFAULT_API_VERSION = "20240601"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Statsig dashboard via /console/v1/dashboards",
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="Path to a JSON file containing the dashboard create body",
    )
    parser.add_argument(
        "--body",
        default=None,
        help="Inline JSON string containing the dashboard create body",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Endpoint URL (default: {DEFAULT_ENDPOINT})",
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
        raise ValueError("Dashboard create body must be a JSON object")

    if "id" in payload:
        raise ValueError("Create body must not include `id`")

    return payload


def format_dry_run(
    endpoint: str,
    has_api_key: bool,
    api_version: str,
    payload: dict,
) -> str:
    request_preview = {
        "method": "POST",
        "endpoint": endpoint,
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

    if args.dry_run:
        print(
            format_dry_run(
                args.endpoint,
                api_key is not None,
                api_version,
                payload,
            )
        )
        return 0

    if not api_key:
        print(
            "Missing STATSIG_CONSOLE_API_KEY (or pass --api-key)",
            file=sys.stderr,
        )
        return 2

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        args.endpoint,
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
        print(f"HTTP {exc.code} from {args.endpoint}: {body}", file=sys.stderr)
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
