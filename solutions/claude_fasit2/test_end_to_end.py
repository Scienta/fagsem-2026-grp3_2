import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def test_cli_processes_sample_input(tmp_path):
    input_file = HERE / "sample_input.txt"
    result = subprocess.run(
        [sys.executable, str(HERE / "main.py"), str(input_file)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    assert result.stderr == ""
    stdout = result.stdout.strip()
    blocks = stdout.split("\n\n")
    assert len(blocks) == 2
    assert blocks[0].splitlines()[0] == "Roger Rud"
    assert blocks[1].splitlines()[0] == "Per Høneeier"
    for block in blocks:
        lines = block.splitlines()
        assert len(lines) == 2
        assert lines[1].endswith(" NOK")
        tax = int(lines[1].removesuffix(" NOK"))
        assert tax > 0


def test_cli_reports_missing_file(tmp_path):
    missing = tmp_path / "does_not_exist.txt"
    result = subprocess.run(
        [sys.executable, str(HERE / "main.py"), str(missing)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "not found" in result.stderr.lower()


def test_cli_reports_missing_argument():
    result = subprocess.run(
        [sys.executable, str(HERE / "main.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "usage" in result.stderr.lower()
