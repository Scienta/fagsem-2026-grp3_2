"""Parse tax input blocks and format result blocks."""

import re
from decimal import Decimal
from typing import Iterable

from tax_rules import TaxResult, Taxpayer


_AGE_RE = re.compile(r"^\s*(\d+)\s*år\s*$", re.IGNORECASE)
_AMOUNT_RE = re.compile(r"^\s*([\d\s ]+)\s*NOK\s*$", re.IGNORECASE)


def _split_blocks(text: str) -> list[list[str]]:
    """Split text into blocks of non-empty lines separated by blank lines."""
    blocks: list[list[str]] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line)
    if current:
        blocks.append(current)
    return blocks


def _parse_age(line: str) -> int:
    m = _AGE_RE.match(line)
    if not m:
        raise ValueError(f"Forventet alder på formen 'N år', fikk: {line!r}")
    return int(m.group(1))


def _parse_amount(line: str) -> Decimal:
    m = _AMOUNT_RE.match(line)
    if not m:
        raise ValueError(f"Forventet beløp på formen 'N NOK', fikk: {line!r}")
    digits = re.sub(r"[\s ]", "", m.group(1))
    if not digits:
        raise ValueError(f"Tomt beløp: {line!r}")
    return Decimal(digits)


def parse_taxpayers(text: str) -> list[Taxpayer]:
    """Parse input text into a list of Taxpayer records.

    Each block has exactly three lines: name, '<N> år', '<amount> NOK'.
    """
    result: list[Taxpayer] = []
    for i, block in enumerate(_split_blocks(text), start=1):
        if len(block) != 3:
            raise ValueError(
                f"Blokk {i} må ha 3 linjer (navn, alder, inntekt), har {len(block)}"
            )
        name, age_line, amount_line = block
        result.append(Taxpayer(
            name=name,
            age=_parse_age(age_line),
            salary=_parse_amount(amount_line),
        ))
    return result


def _format_amount(value: Decimal) -> str:
    """Format a whole-krone amount with plain space as thousand separator."""
    whole = int(value.to_integral_value(rounding="ROUND_HALF_UP"))
    sign = "-" if whole < 0 else ""
    digits = str(abs(whole))
    groups = []
    while digits:
        groups.append(digits[-3:])
        digits = digits[:-3]
    return sign + " ".join(reversed(groups))


def format_results(results: Iterable[TaxResult]) -> str:
    """Render results as blocks of 'name\\n<total> NOK' separated by blank lines."""
    blocks = []
    for r in results:
        blocks.append(f"{r.taxpayer.name}\n{_format_amount(r.total)} NOK")
    return "\n\n".join(blocks) + "\n"
