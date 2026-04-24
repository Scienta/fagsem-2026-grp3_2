"""CLI entry point: read taxpayer file, compute tax, write result file."""

import argparse
import sys
from pathlib import Path

from tax_io import format_results, parse_taxpayers
from tax_rules import beregn_skatt


def run(input_path: Path, output_path: Path) -> int:
    text = input_path.read_text(encoding="utf-8")
    taxpayers = parse_taxpayers(text)
    results = [beregn_skatt(t) for t in taxpayers]
    output_path.write_text(format_results(results), encoding="utf-8")
    return len(results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Beregn skatt for lønnsmottakere på Østlandet (2024)."
    )
    parser.add_argument("input", type=Path, help="Inndatafil")
    parser.add_argument("output", type=Path, help="Utdatafil")
    args = parser.parse_args(argv)
    count = run(args.input, args.output)
    print(f"Skrev resultat for {count} skatteyter(e) til {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
