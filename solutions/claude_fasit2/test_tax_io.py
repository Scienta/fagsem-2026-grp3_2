import pytest

from tax_io import Taxpayer, format_result, format_results, parse_taxpayers


def test_parse_single_taxpayer():
    text = "Roger Rud\n50 years\n125 000 NOK\n"
    result = parse_taxpayers(text)
    assert result == (Taxpayer(name="Roger Rud", age=50, gross_wages=125_000),)


def test_parse_multiple_taxpayers_separated_by_blank_line():
    text = (
        "Roger Rud\n50 years\n125 000 NOK\n"
        "\n"
        "Per Hønseeier\n42 years\n7 000 000 NOK\n"
    )
    result = parse_taxpayers(text)
    assert result == (
        Taxpayer(name="Roger Rud", age=50, gross_wages=125_000),
        Taxpayer(name="Per Hønseeier", age=42, gross_wages=7_000_000),
    )


def test_parse_accepts_norwegian_age_suffix():
    text = "Kari\n30 år\n500 000 NOK\n"
    assert parse_taxpayers(text) == (
        Taxpayer(name="Kari", age=30, gross_wages=500_000),
    )


def test_parse_accepts_amount_without_spaces():
    text = "Ola\n40 years\n400000 NOK\n"
    assert parse_taxpayers(text) == (
        Taxpayer(name="Ola", age=40, gross_wages=400_000),
    )


def test_parse_ignores_trailing_blank_lines():
    text = "Kari\n30 years\n100 000 NOK\n\n\n"
    result = parse_taxpayers(text)
    assert len(result) == 1


def test_parse_rejects_wrong_block_size():
    with pytest.raises(ValueError):
        parse_taxpayers("Roger Rud\n50 years\n")


def test_parse_rejects_invalid_age():
    with pytest.raises(ValueError):
        parse_taxpayers("Roger Rud\nfifty years\n125 000 NOK\n")


def test_parse_rejects_invalid_amount():
    with pytest.raises(ValueError):
        parse_taxpayers("Roger Rud\n50 years\nfive hundred NOK\n")


def test_format_result_rounds_to_whole_kroner():
    assert format_result("Name", 1234.49) == "Name\n1234 NOK"
    assert format_result("Name", 1234.51) == "Name\n1235 NOK"


def test_format_results_joins_blocks_with_blank_line():
    out = format_results([("A", 100), ("B", 200)])
    assert out == "A\n100 NOK\n\nB\n200 NOK"


def test_format_results_empty_returns_empty_string():
    assert format_results([]) == ""
