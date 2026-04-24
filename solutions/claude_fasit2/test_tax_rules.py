import math

import pytest

from tax_rules import (
    MINIMUM_DEDUCTION_WAGE_CEILING,
    MINIMUM_DEDUCTION_WAGE_FLOOR,
    bracket_tax,
    income_tax,
    minimum_deduction_wages,
    national_insurance_wages,
    ordinary_income,
    total_tax_wages,
)


def test_minimum_deduction_floor_applies_to_low_wages():
    assert minimum_deduction_wages(0) == MINIMUM_DEDUCTION_WAGE_FLOOR
    assert minimum_deduction_wages(5_000) == MINIMUM_DEDUCTION_WAGE_FLOOR


def test_minimum_deduction_is_proportional_in_middle_range():
    assert minimum_deduction_wages(100_000) == pytest.approx(46_000)


def test_minimum_deduction_ceiling_applies_to_high_wages():
    assert minimum_deduction_wages(1_000_000) == MINIMUM_DEDUCTION_WAGE_CEILING


def test_ordinary_income_cannot_be_negative():
    assert ordinary_income(50_000) == 0.0


def test_ordinary_income_for_700k_matches_tax_md_example():
    assert ordinary_income(700_000) == pytest.approx(507_300)


def test_income_tax_is_22_percent_of_ordinary_income():
    assert income_tax(700_000) == pytest.approx(507_300 * 0.22)


def test_bracket_tax_is_zero_below_first_threshold():
    assert bracket_tax(208_050) == 0.0


def test_bracket_tax_first_kroner_in_bracket_1():
    assert bracket_tax(208_051) == pytest.approx(0.017, rel=1e-6)


def test_bracket_tax_full_bracket_1():
    assert bracket_tax(292_850) == pytest.approx(84_800 * 0.017)


def test_bracket_tax_for_700k_covers_brackets_1_through_3():
    expected = (
        84_800 * 0.017
        + (670_000 - 292_850) * 0.040
        + (700_000 - 670_000) * 0.136
    )
    assert bracket_tax(700_000) == pytest.approx(expected)


def test_bracket_tax_for_high_income_covers_all_brackets():
    expected = (
        84_800 * 0.017
        + (670_000 - 292_850) * 0.040
        + (937_900 - 670_000) * 0.136
        + (1_350_000 - 937_900) * 0.166
        + (7_000_000 - 1_350_000) * 0.176
    )
    assert bracket_tax(7_000_000) == pytest.approx(expected)


def test_national_insurance_zero_below_threshold():
    assert national_insurance_wages(83_000) == 0.0
    assert national_insurance_wages(50_000) == 0.0


def test_national_insurance_uses_phase_in_cap_just_above_threshold():
    income = 90_000
    cap = 0.25 * (income - 83_000)
    raw = 0.078 * income
    assert national_insurance_wages(income) == pytest.approx(min(cap, raw))
    assert national_insurance_wages(income) == pytest.approx(cap)


def test_national_insurance_uses_flat_rate_at_high_income():
    assert national_insurance_wages(700_000) == pytest.approx(0.078 * 700_000)


def test_total_tax_for_125k_matches_manual_calculation():
    # below personal_deduction + minstefradrag ⇒ no income tax, no bracket tax
    expected = 0.078 * 125_000
    assert total_tax_wages(125_000) == pytest.approx(expected)


def test_total_tax_is_sum_of_components():
    income = 900_000
    expected = (
        income_tax(income)
        + bracket_tax(income)
        + national_insurance_wages(income)
    )
    assert total_tax_wages(income) == pytest.approx(expected)


def test_bracket_tax_is_non_decreasing():
    previous = -math.inf
    for income in (0, 100_000, 250_000, 500_000, 1_000_000, 2_000_000, 10_000_000):
        current = bracket_tax(income)
        assert current >= previous
        previous = current
