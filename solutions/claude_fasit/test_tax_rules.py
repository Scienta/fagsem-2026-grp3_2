"""Tests for tax_rules: calculation functions on 2024 lønnsmottaker Østlandet."""

from decimal import Decimal

import pytest

from tax_rules import (
    MINSTEFRADRAG_MAX_LONN,
    PERSONFRADRAG_KLASSE_1,
    Taxpayer,
    alminnelig_inntekt,
    beregn_skatt,
    inntektsskatt,
    minstefradrag_lonn,
    trinnskatt,
    trygdeavgift_lonn,
)


D = Decimal


class TestMinstefradrag:
    def test_zero_income(self):
        assert minstefradrag_lonn(D("0")) == D("0")

    def test_very_low_income_uses_floor(self):
        # 46% of 5000 = 2300, floor 4000 kicks in
        assert minstefradrag_lonn(D("5000")) == D("4000")

    def test_middle_income_percentage(self):
        assert minstefradrag_lonn(D("100000")) == D("46000")

    def test_capped_at_max(self):
        # 46% of 1 000 000 = 460 000, capped at 104 450
        assert minstefradrag_lonn(D("1000000")) == MINSTEFRADRAG_MAX_LONN


class TestAlminneligInntekt:
    def test_below_deductions_is_zero(self):
        assert alminnelig_inntekt(D("100000"), D("46000")) == D("0")

    def test_positive_result(self):
        # 700 000 - 104 450 - 88 250 = 507 300
        assert alminnelig_inntekt(D("700000"), MINSTEFRADRAG_MAX_LONN) == D("507300")

    def test_exactly_zero(self):
        # sum equals deductions
        sum_ded = MINSTEFRADRAG_MAX_LONN + PERSONFRADRAG_KLASSE_1
        assert alminnelig_inntekt(sum_ded, MINSTEFRADRAG_MAX_LONN) == D("0")


class TestInntektsskatt:
    def test_zero(self):
        assert inntektsskatt(D("0")) == D("0")

    def test_22_percent(self):
        assert inntektsskatt(D("507300")) == D("111606.00")


class TestTrinnskatt:
    def test_below_first_bracket(self):
        assert trinnskatt(D("100000")) == D("0")
        assert trinnskatt(D("208050")) == D("0")

    def test_inside_first_bracket(self):
        # 250 000: (250000 - 208050) * 0.017 = 41 950 * 0.017 = 713.15
        assert trinnskatt(D("250000")) == D("713.150")

    def test_700_000_crosses_three_brackets(self):
        # bracket 1: 84 800 * 0.017 = 1441.60
        # bracket 2: 377 150 * 0.040 = 15086.00
        # bracket 3: 30 000 * 0.136 = 4080.00
        assert trinnskatt(D("700000")) == D("20607.600")

    def test_very_high_income_crosses_all_brackets(self):
        # 7 000 000
        # 84 800 * 0.017 = 1441.60
        # 377 150 * 0.040 = 15086.00
        # 267 900 * 0.136 = 36434.40
        # 412 100 * 0.166 = 68408.60
        # 5 650 000 * 0.176 = 994400.00
        assert trinnskatt(D("7000000")) == D("1115770.600")


class TestTrygdeavgift:
    def test_zero_income(self):
        assert trygdeavgift_lonn(D("0")) == D("0")

    def test_below_frigrense(self):
        assert trygdeavgift_lonn(D("50000")) == D("0")

    def test_nedtrappingsregel_binds(self):
        # 100 000: rå = 7800; maks = (100000-83000)*0.25 = 4250 → maks binds
        assert trygdeavgift_lonn(D("100000")) == D("4250.00")

    def test_full_sats_applies(self):
        # 700 000: rå = 54600; maks = 154250 → rå binds
        assert trygdeavgift_lonn(D("700000")) == D("54600.000")


class TestBeregnSkatt:
    def test_roger_rud_125k(self):
        t = Taxpayer(name="Roger Rud", age=50, salary=D("125000"))
        r = beregn_skatt(t)
        assert r.minstefradrag == D("57500.00")
        assert r.alminnelig_inntekt == D("0")
        assert r.inntektsskatt == D("0")
        assert r.trinnskatt == D("0")
        # rå = 9750; maks = 42000*0.25 = 10500 → rå binds
        assert r.trygdeavgift == D("9750.000")
        assert r.total == D("9750.000")

    def test_per_honeeier_7m(self):
        t = Taxpayer(name="Per Høneeier", age=42, salary=D("7000000"))
        r = beregn_skatt(t)
        assert r.minstefradrag == MINSTEFRADRAG_MAX_LONN
        assert r.alminnelig_inntekt == D("6807300")
        assert r.inntektsskatt == D("1497606.00")
        assert r.trinnskatt == D("1115770.600")
        assert r.trygdeavgift == D("546000.000")
        assert r.total == D("3159376.600")

    @pytest.mark.parametrize("salary,expected_total", [
        (D("0"), D("0")),
        (D("50000"), D("0")),
        (D("125000"), D("9750.000")),
    ])
    def test_low_income_totals(self, salary, expected_total):
        t = Taxpayer(name="X", age=30, salary=salary)
        assert beregn_skatt(t).total == expected_total
