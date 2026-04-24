"""CLI entry point: read a taxpayer file, print tax per taxpayer to stdout."""

import sys
from pathlib import Path

from tax_io import format_results, parse_taxpayers
from tax_rules import total_tax_wages


def run(input_path: Path) -> str:
    text = input_path.read_text(encoding="utf-8")
    taxpayers = parse_taxpayers(text)
    entries = tuple(
        (t.name, total_tax_wages(t.gross_wages)) for t in taxpayers
    )
    return format_results(entries)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {argv[0]} <input_file>", file=sys.stderr)
        return 2
    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1
    output = run(input_path)
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
