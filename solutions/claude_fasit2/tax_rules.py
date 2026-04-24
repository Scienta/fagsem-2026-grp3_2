"""Tax calculation rules for Norwegian wage earners on Østlandet, income year 2024.

Pure functions only. No IO. Numbers expressed in NOK.
"""

from dataclasses import dataclass
from typing import Sequence


PERSONAL_DEDUCTION_CLASS_1 = 88_250

MINIMUM_DEDUCTION_WAGE_RATE = 0.46
MINIMUM_DEDUCTION_WAGE_FLOOR = 4_000
MINIMUM_DEDUCTION_WAGE_CEILING = 104_450

INCOME_TAX_RATE_MAINLAND = 0.22

NATIONAL_INSURANCE_WAGE_RATE = 0.078
NATIONAL_INSURANCE_EXEMPTION_THRESHOLD = 83_000
NATIONAL_INSURANCE_PHASE_IN_RATE = 0.25


@dataclass(frozen=True)
class Bracket:
    lower: int
    upper: float
    rate: float


WAGE_BRACKETS_2024: Sequence[Bracket] = (
    Bracket(lower=208_050, upper=292_850, rate=0.017),
    Bracket(lower=292_850, upper=670_000, rate=0.040),
    Bracket(lower=670_000, upper=937_900, rate=0.136),
    Bracket(lower=937_900, upper=1_350_000, rate=0.166),
    Bracket(lower=1_350_000, upper=float("inf"), rate=0.176),
)


def minimum_deduction_wages(gross_wages: float) -> float:
    raw = MINIMUM_DEDUCTION_WAGE_RATE * gross_wages
    capped = min(raw, MINIMUM_DEDUCTION_WAGE_CEILING)
    return max(MINIMUM_DEDUCTION_WAGE_FLOOR, capped)


def ordinary_income(gross_wages: float) -> float:
    deduction = minimum_deduction_wages(gross_wages) + PERSONAL_DEDUCTION_CLASS_1
    return max(0.0, gross_wages - deduction)


def income_tax(gross_wages: float) -> float:
    return ordinary_income(gross_wages) * INCOME_TAX_RATE_MAINLAND


def bracket_tax(personal_income: float,
                brackets: Sequence[Bracket] = WAGE_BRACKETS_2024) -> float:
    return sum(
        (min(personal_income, b.upper) - b.lower) * b.rate
        for b in brackets
        if personal_income > b.lower
    )


def national_insurance_wages(personal_income: float) -> float:
    raw = NATIONAL_INSURANCE_WAGE_RATE * personal_income
    surplus = max(0.0, personal_income - NATIONAL_INSURANCE_EXEMPTION_THRESHOLD)
    cap = NATIONAL_INSURANCE_PHASE_IN_RATE * surplus
    if personal_income <= NATIONAL_INSURANCE_EXEMPTION_THRESHOLD:
        return 0.0
    return min(raw, cap)


def total_tax_wages(gross_wages: float) -> float:
    return (
        income_tax(gross_wages)
        + bracket_tax(gross_wages)
        + national_insurance_wages(gross_wages)
    )
