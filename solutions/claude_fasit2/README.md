# Tax calculator (claude_fasit2)

A Python program that reads taxpayer data from a file and prints the
calculated annual tax per taxpayer to standard output. Tax rules follow
the simplified 2024 rules described in `../../tax.md`, restricted to:

- Wage earners resident on Østlandet (flat rate 22% on ordinary income)
- Automatic deductions only (minstefradrag wage rate, personfradrag class 1)
- Trinnskatt 2024 wage-earner brackets
- Trygdeavgift 7.8% with the phase-in cap against low incomes

Age is read from the input but has no effect on the calculation.

## Evaluation timestamps

- Initiated: 2026-04-24 15:24:04 CEST (2026-04-24T13:24:04Z)
- Completed: 2026-04-24 15:27:28 CEST (2026-04-24T13:27:28Z)

## Requirements

- Python 3.11 or newer
- `pytest` and `pytest-xdist` (already installed in the project `.venv`)

## Input format

UTF-8 text file. One or more taxpayer blocks, each block on three lines,
blocks separated by a blank line:

```
<name>
<age> years
<amount> NOK
```

- The age suffix accepts `years`, `year`, and the Norwegian `år`
  (case-insensitive).
- Whitespace inside the amount (used as thousand separator) is ignored.

Example:

```
Roger Rud
50 years
125 000 NOK

Per Høneeier
42 years
7 000 000 NOK
```

## Output format

One block per taxpayer, in input order, printed to stdout with blank
lines between blocks:

```
<name>
<total tax in whole NOK> NOK
```

## Running

From the project root (with `.venv` activated and `PYTHONPATH` set as
per `CLAUDE.md`):

```
python solutions/claude_fasit2/main.py solutions/claude_fasit2/sample_input.txt
```

Or from within the sub-folder:

```
cd solutions/claude_fasit2
python main.py sample_input.txt
```

## Tests

From the sub-folder:

```
pytest -n auto
```

All tests must pass with no failures and no warnings.

## Project layout

- `tax_rules.py` — pure calculation functions and 2024 constants
- `tax_io.py` — input parsing and output formatting
- `main.py` — CLI entry point
- `sample_input.txt` — example from the task description
- `test_tax_rules.py`, `test_tax_io.py`, `test_end_to_end.py` — test suite
- `conftest.py` — makes the sub-folder importable during test runs
