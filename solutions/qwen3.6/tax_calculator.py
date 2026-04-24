"""
Norsk skattekalkulator for inntektsåret 2024.

Leser inn skattedata fra en input-fil, beregner skatt basert på
forenklede norske skatteregler (skatt.md), og skriver resultat til en output-fil.
"""

import argparse
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Tuple


@dataclass
class Taxpayer:
    name: str
    age: int
    income: Decimal
    income_type: str = "lonn"  # "lonn", "pensjon", "naering"


def parse_input(filepath: str) -> List[Taxpayer]:
    """Parse input file with taxpayer data.

    Format (per taxpayer, separated by blank line):
        Name
        Age years
        Income NOK
    """
    taxpayers = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    i = 0
    while i < len(lines):
        # Skip blank lines
        if not lines[i]:
            i += 1
            continue

        name = lines[i]
        # Parse age line: "X år"
        age_line = lines[i + 1].replace("år", "").strip()
        age = int(age_line)
        # Parse income line: "X NOK"
        income_str = lines[i + 2].replace("NOK", "").strip()
        # Remove spaces as thousands separator (e.g. "125 000")
        income_str = income_str.replace(" ", "")
        income = Decimal(income_str)

        taxpayers.append(Taxpayer(name=name, age=age, income=income))
        i += 3

    return taxpayers


def calc_minstefradrag(lonn: Decimal) -> Decimal:
    """Minstefradrag for lønn: 46% of salary, between 4000 and 104450."""
    return max(Decimal("4000"), min(Decimal("0.46") * lonn, Decimal("104450")))


def calc_pensjon_minstefradrag(pensjon: Decimal) -> Decimal:
    """Minstefradrag for pensjon: 40% of pension, between 4000 and 86250."""
    return max(Decimal("4000"), min(Decimal("0.40") * pensjon, Decimal("86250")))


def calc_personfradrag() -> Decimal:
    """Personfradrag klasse 1 for 2024."""
    return Decimal("88250")


def calc_inntektsskatt(alminnelig_inntekt: Decimal) -> Decimal:
    """Inntektsskatt: flat 22% of alminnelig inntekt."""
    return alminnelig_inntekt * Decimal("0.22")


def calc_trinnskatt(personinntekt: Decimal, income_type: str) -> Decimal:
    """Trinnskatt based on personinntekt (no deductions).

    Uses half-open intervals [lower, upper) matching official Norwegian tax tables.
    """
    if income_type == "pensjon":
        trinn: List[Tuple[Decimal, Decimal | None, Decimal]] = [
            (Decimal("208050"), Decimal("292850"), Decimal("0.009")),
            (Decimal("292850"), Decimal("670000"), Decimal("0.020")),
            (Decimal("670000"), Decimal("937900"), Decimal("0.118")),
            (Decimal("937900"), Decimal("1350000"), Decimal("0.148")),
            (Decimal("1350000"), None, Decimal("0.176")),
        ]
    else:
        # Lonn or naering
        trinn = [
            (Decimal("208050"), Decimal("292850"), Decimal("0.017")),
            (Decimal("292850"), Decimal("670000"), Decimal("0.040")),
            (Decimal("670000"), Decimal("937900"), Decimal("0.136")),
            (Decimal("937900"), Decimal("1350000"), Decimal("0.166")),
            (Decimal("1350000"), None, Decimal("0.176")),
        ]

    trinnskatt = Decimal("0")
    for lower, upper, sats in trinn:
        if personinntekt <= lower:
            break
        top = personinntekt if upper is None else min(personinntekt, upper)
        trinnskatt += (top - lower) * sats

    return trinnskatt


def calc_trygdeavgift(personinntekt: Decimal, income_type: str) -> Decimal:
    """Trygdeavgift with nedtrappingsregel (frikortgrense)."""
    satser = {
        "lonn": Decimal("0.078"),
        "pensjon": Decimal("0.051"),
        "naering": Decimal("0.11"),
    }
    sats = satser.get(income_type, Decimal("0.078"))

    ra_trygdeavgift = personinntekt * sats
    maks_trygdeavgift = max(Decimal("0"), personinntekt - Decimal("83000")) * Decimal("0.25")
    return min(ra_trygdeavgift, maks_trygdeavgift)


def calculate_tax(p: Taxpayer) -> Decimal:
    """Calculate total tax for a taxpayer."""
    brutto = p.income
    income_type = p.income_type

    # STEG 1: personinntekt
    personinntekt = brutto

    # STEG 2: minstefradrag
    if income_type == "pensjon":
        minstefradrag = calc_pensjon_minstefradrag(brutto)
    else:
        minstefradrag = calc_minstefradrag(brutto)

    # STEG 3: alminnelig inntekt
    alminnelig_inntekt = brutto - minstefradrag - calc_personfradrag()
    alminnelig_inntekt = max(Decimal("0"), alminnelig_inntekt)

    # STEG 4: inntektsskatt
    inntektsskatt = calc_inntektsskatt(alminnelig_inntekt)

    # STEG 5: trinnskatt
    trinnskatt = calc_trinnskatt(personinntekt, income_type)

    # STEG 6: trygdeavgift
    trygdeavgift = calc_trygdeavgift(personinntekt, income_type)

    # STEG 7: total skatt
    total_skatt = inntektsskatt + trinnskatt + trygdeavgift

    return total_skatt


def format_number(n: Decimal) -> str:
    """Format a number with space as thousands separator, rounded to whole kroner."""
    whole = int(n.to_integral_value(rounding=ROUND_HALF_UP))
    sign = "-" if whole < 0 else ""
    digits = str(abs(whole))
    groups = []
    while digits:
        groups.append(digits[-3:])
        digits = digits[:-3]
    return sign + " ".join(reversed(groups))


def main():
    parser = argparse.ArgumentParser(description="Norsk skattekalkulator")
    parser.add_argument("input", help="Input fil med skattedata")
    parser.add_argument("-o", "--output", default="skatt_resultat.txt", help="Output fil")
    args = parser.parse_args()

    taxpayers = parse_input(args.input)

    blocks = []
    for p in taxpayers:
        skatt = calculate_tax(p)
        blocks.append(f"{p.name}\n{format_number(skatt)} NOK")

    with open(args.output, "w", encoding="utf-8") as out:
        out.write("\n\n".join(blocks) + "\n")

    print(f"Skatt beregnet for {len(taxpayers)} skatteytere. Resultat lagret i {args.output}")


if __name__ == "__main__":
    main()
