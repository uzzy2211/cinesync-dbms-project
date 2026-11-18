import argparse
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import requests


def check_health(url: str, timeout: float) -> tuple[bool, str]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        body: Any = response.json()
    except (requests.RequestException, ValueError) as error:
        return False, str(error)

    if not isinstance(body, dict) or body.get("status") != "ok":
        return False, "The health endpoint returned an unexpected response."
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send concurrent requests to the CineSync health endpoint."
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/health",
        help="Health endpoint URL.",
    )
    parser.add_argument("--requests", type=int, default=100, dest="request_count")
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    if args.request_count < 1:
        parser.error("--requests must be at least 1.")
    if args.workers < 1:
        parser.error("--workers must be at least 1.")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0.")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(
            executor.map(
                lambda _: check_health(args.url, args.timeout),
                range(args.request_count),
            )
        )

    passed = sum(success for success, _ in results)
    failures = [message for success, message in results if not success]
    print(f"Health checks passed: {passed}/{args.request_count}")
    for message in failures[:5]:
        print(f"Failure: {message}")
    return 0 if passed == args.request_count else 1


if __name__ == "__main__":
    raise SystemExit(main())