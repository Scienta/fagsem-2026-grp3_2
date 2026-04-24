"""Tests for tax_io: parser and formatter."""

from decimal import Decimal

import pytest

from tax_io import _format_amount, format_results, parse_taxpayers
from tax_rules import TaxResult, Taxpayer


D = Decimal


SAMPLE_INPUT = """Roger Rud
50 år
125 000 NOK

Per Høneeier
42 år
7 000 000 NOK
"""


class TestParse:
    def test_sample_input(self):
        taxpayers = parse_taxpayers(SAMPLE_INPUT)
        assert len(taxpayers) == 2
        assert taxpayers[0] == Taxpayer("Roger Rud", 50, D("125000"))
        assert taxpayers[1] == Taxpayer("Per Høneeier", 42, D("7000000"))

    def test_no_thousand_separator(self):
        text = "Ola Nordmann\n30 år\n500000 NOK\n"
        result = parse_taxpayers(text)
        assert result == [Taxpayer("Ola Nordmann", 30, D("500000"))]

    def test_trailing_whitespace_and_blank_lines(self):
        text = "\n\nNavn Navnesen\n25 år\n100 000 NOK\n\n\n"
        result = parse_taxpayers(text)
        assert result == [Taxpayer("Navn Navnesen", 25, D("100000"))]

    def test_empty_input(self):
        assert parse_taxpayers("") == []

    def test_bad_age_line(self):
        with pytest.raises(ValueError, match="alder"):
            parse_taxpayers("Navn\nikke-alder\n100 NOK\n")

    def test_bad_amount_line(self):
        with pytest.raises(ValueError, match="beløp"):
            parse_taxpayers("Navn\n30 år\nhundre kroner\n")

    def test_wrong_block_size(self):
        with pytest.raises(ValueError, match="3 linjer"):
            parse_taxpayers("Navn\n30 år\n")


class TestFormatAmount:
    @pytest.mark.parametrize("value,expected", [
        (D("0"), "0"),
        (D("999"), "999"),
        (D("1000"), "1 000"),
        (D("9750"), "9 750"),
        (D("1234567"), "1 234 567"),
    ])
    def test_grouping(self, value, expected):
        assert _format_amount(value) == expected

    def test_rounds_half_up(self):
        assert _format_amount(D("9750.4")) == "9 750"
        assert _format_amount(D("9750.5")) == "9 751"


class TestFormatResults:
    def test_two_results(self):
        t1 = Taxpayer("Roger Rud", 50, D("125000"))
        t2 = Taxpayer("Per Høneeier", 42, D("7000000"))
        r1 = TaxResult(t1, D("0"), D("0"), D("0"), D("0"), D("9750"), D("9750"))
        r2 = TaxResult(t2, D("0"), D("0"), D("0"), D("0"), D("0"), D("3159376.6"))
        text = format_results([r1, r2])
        assert text == (
            "Roger Rud\n"
            "9 750 NOK\n"
            "\n"
            "Per Høneeier\n"
            "3 159 377 NOK\n"
        )

    def test_empty(self):
        assert format_results([]) == "\n"
