"""Command-line entry point: ``python3 -m calc EXPRESSION``."""

from __future__ import annotations

import sys

from calc.evaluator import CalcError, evaluate, format_number

USAGE = "usage: python3 -m calc EXPRESSION"


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        value = evaluate(argv[0])
    except CalcError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(format_number(value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
