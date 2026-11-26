#!/usr/bin/env python3
"""envcheck - Zero-dependency CLI to validate .env files against .env.example."""

import argparse
import sys
from pathlib import Path


def parse_env_keys(filepath: Path) -> dict[str, str]:
    """Parse KEY=VALUE pairs from an env file, ignoring comments and blank lines."""
    entries: dict[str, str] = {}
    for line_num, raw_line in enumerate(
        filepath.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            print(
                f"Warning: {filepath}:{line_num} skipped (missing '=')",
                file=sys.stderr,
            )
            continue
        key, value = line.split("=", 1)
        entries[key.strip()] = value.strip().strip("\"'")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that a .env file defines all keys required by .env.example."
        )
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to target .env file (default: .env)",
    )
    parser.add_argument(
        "--example",
        default=".env.example",
        help="Path to template file (default: .env.example)",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow keys to exist with empty values",
    )
    args = parser.parse_args()

    example_path = Path(args.example)
    env_path = Path(args.env)

    if not example_path.exists():
        print(f"Error: Template file '{example_path}' not found.", file=sys.stderr)
        return 2
    if not env_path.exists():
        print(f"Error: Target file '{env_path}' not found.", file=sys.stderr)
        return 2

    required = parse_env_keys(example_path)
    actual = parse_env_keys(env_path)

    missing = [key for key in required if key not in actual]
    empty = (
        []
        if args.allow_empty
        else [
            key
            for key in required
            if key in actual and actual[key] == ""
        ]
    )

    if not missing and not empty:
        print(
            "OK: All "
            f"{len(required)} required environment variables are set in '{env_path}'."
        )
        return 0

    if missing:
        print("Missing keys:")
        for key in missing:
            print(f"  - {key}")
    if empty:
        print("Empty values:")
        for key in empty:
            print(f"  - {key}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
