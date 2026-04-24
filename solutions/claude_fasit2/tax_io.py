"""Parse taxpayer input blocks and format tax-per-taxpayer output blocks."""

import re
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Taxpayer:
    name: str
    age: int
    gross_wages: int


_AGE_PATTERN = re.compile(r"^\s*(\d+)\s+(?:years?|år)\s*$", re.IGNORECASE)
_AMOUNT_PATTERN = re.compile(r"^\s*([\d\s ]+)\s*NOK\s*$", re.IGNORECASE)


def _parse_age(line: str) -> int:
    match = _AGE_PATTERN.match(line)
    if match is None:
        raise ValueError(f"Unrecognised age line: {line!r}")
    return int(match.group(1))


def _parse_amount(line: str) -> int:
    match = _AMOUNT_PATTERN.match(line)
    if match is None:
        raise ValueError(f"Unrecognised amount line: {line!r}")
    digits = re.sub(r"\s", "", match.group(1))
    if not digits:
        raise ValueError(f"Amount line has no digits: {line!r}")
    return int(digits)


def _split_blocks(text: str) -> Sequence[Sequence[str]]:
    blocks = []
    current: list[str] = []
    for raw in text.splitlines():
        if raw.strip() == "":
            if current:
                blocks.append(tuple(current))
                current = []
        else:
            current.append(raw)
    if current:
        blocks.append(tuple(current))
    return tuple(blocks)


def parse_taxpayers(text: str) -> Sequence[Taxpayer]:
    taxpayers = []
    for block in _split_blocks(text):
        if len(block) != 3:
            raise ValueError(
                f"Taxpayer block must have 3 lines, got {len(block)}: {block!r}"
            )
        name = block[0].strip()
        age = _parse_age(block[1])
        amount = _parse_amount(block[2])
        taxpayers.append(Taxpayer(name=name, age=age, gross_wages=amount))
    return tuple(taxpayers)


def format_result(name: str, total_tax: float) -> str:
    rounded = int(round(total_tax))
    return f"{name}\n{rounded} NOK"


def format_results(entries: Iterable[tuple[str, float]]) -> str:
    blocks = [format_result(name, tax) for name, tax in entries]
    return "\n\n".join(blocks)
