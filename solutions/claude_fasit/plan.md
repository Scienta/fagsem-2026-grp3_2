# Plan: Skattekalkulator (claude_fasit)

- [x] Phase 1 — Plan document
- [x] Phase 2 — Tax rules module (`tax_rules.py`)
- [x] Phase 3 — Parser and formatter (`tax_io.py`)
- [x] Phase 4 — CLI entry point (`main.py`) + sample input
- [x] Phase 5 — Pytest test suite; all green, no warnings

## Scope

Implement a Norwegian tax calculator for the 2024 income year, restricted to:

- Taxpayers on Østlandet (flat rate 22% on alminnelig inntekt)
- Lønnsinntekt only (no pension, no næring, no kapital)
- Only automatic deductions: minstefradrag (lønn) and personfradrag klasse 1
- Trinnskatt 2024 for lønnsmottakere
- Trygdeavgift 7,8% med nedtrappingsregel

Age is parsed but does not alter the calculation (all inputs are treated as salary earners on Østlandet per the task description).

## Input/Output format

Input: UTF-8 text file with blocks separated by a blank line. Each block is:

```
<name>
<age> år
<amount> NOK
```

Whitespace in the amount (thousand separator) is ignored.

Output: matching blocks with name and computed total skatt rounded to whole kroner:

```
<name>
<total> NOK
```

## File layout (inside `solutions/claude_fasit/`)

- `tax_rules.py` — pure calculation functions and 2024 constants
- `tax_io.py` — parsing and formatting
- `main.py` — CLI: `python main.py <input> <output>`
- `sample_input.txt` — example from `oppgave.md`
- `test_tax_rules.py`, `test_tax_io.py`, `test_end_to_end.py`
- `conftest.py` — ensures package-local imports

## Acceptance

- `pytest -n auto` in the subfolder reports 0 failures, 0 warnings
- Running `python main.py sample_input.txt out.txt` produces a well-formed output file
