"""End-to-end test: run main.run on the sample input, compare output."""

from pathlib import Path

from main import run


SAMPLE = """Roger Rud
50 år
125 000 NOK

Per Høneeier
42 år
7 000 000 NOK
"""


def test_sample_input_produces_output_file(tmp_path: Path):
    input_path = tmp_path / "input.txt"
    output_path = tmp_path / "output.txt"
    input_path.write_text(SAMPLE, encoding="utf-8")

    count = run(input_path, output_path)
    assert count == 2

    produced = output_path.read_text(encoding="utf-8")
    assert produced == (
        "Roger Rud\n"
        "9 750 NOK\n"
        "\n"
        "Per Høneeier\n"
        "3 159 377 NOK\n"
    )


def test_included_sample_input_file():
    """The repo-shipped sample_input.txt should parse and compute cleanly."""
    here = Path(__file__).resolve().parent
    sample = here / "sample_input.txt"
    out = here / ".pytest_sample_output.tmp"
    try:
        count = run(sample, out)
        assert count == 2
        content = out.read_text(encoding="utf-8")
        assert "Roger Rud" in content
        assert "Per Høneeier" in content
        assert "NOK" in content
    finally:
        if out.exists():
            out.unlink()
