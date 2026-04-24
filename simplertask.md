The task is to produce a command-line utility in Python that can perform the following task:

1. Read a file containing tax data for one or more persons who are wage earners.
2. For each person, calculate tax owed. The rules for the calculation can be found in the Appendix A
3. Output the result of the calculation for each person.

The program should written from scratch as a stand-alone project, in the output directory given by the `$FILE_DIR`
environment variable.

The program should accept a single input file as an argument and produce the answer on stdout.

The Python project should be located in the subdirectory `solutions/gemma4`.

The project directory should contain a `README.md` file with instructions on how to run the program. For evaluation
purposes, the README file should contain a section saying when the project was initiated, and when it was completed. The
timestamps should be in a resolution of seconds.

Example input file, with two taxpayers where name, age, income, and region are provided:

```
Roger Rud
50 years
125 000 NOK
Eastern Norway

Per Høneeier
42 years
7 000 000 NOK
Finnmark
```

Example result output, where the taxpayers are listed with tax owed:

```
Roger Rud
20 000 NOK

Per Hønseeier
1 000 000 NOK
```

# Appendix A

# Simplified tax rules – for a tax calculator

> **Validity:** Income year 2024
> **Audience:** Coding agent implementing a simplified tax calculator
> **Scope:** Income brackets and regional differences only

---

## 1. Regions

Two regions are distinguished:

| Region | Description |
|---|---|
| **Standard** | All of Norway except Finnmark and Nord-Troms |
| **Reduced** | Finnmark and Nord-Troms |

The region determines which rate table applies.

---

## 2. Income brackets – Standard region

Tax is calculated progressively on gross income. Each bracket's rate applies only to the portion of income within that bracket.

| Bracket | Income from (NOK) | Income to (NOK) | Rate |
|---|---|---|---|
| 1 | 0 | 208 050 | 0 % |
| 2 | 208 051 | 292 850 | 23.7 % |
| 3 | 292 851 | 670 000 | 26.0 % |
| 4 | 670 001 | 937 900 | 35.6 % |
| 5 | 937 901 | 1 350 000 | 38.6 % |
| 6 | 1 350 001 | ∞ | 39.6 % |

---

## 3. Income brackets – Reduced region (Finnmark / Nord-Troms)

| Bracket | Income from (NOK) | Income to (NOK) | Rate |
|---|---|---|---|
| 1 | 0 | 208 050 | 0 % |
| 2 | 208 051 | 292 850 | 20.2 % |
| 3 | 292 851 | 670 000 | 22.5 % |
| 4 | 670 001 | 937 900 | 32.1 % |
| 5 | 937 901 | 1 350 000 | 35.1 % |
| 6 | 1 350 001 | ∞ | 36.1 % |

---

## 4. Calculation

```
INPUT:
  - gross_income   (NOK)
  - region         ("standard" | "reduced")

STEP 1 – Select bracket table based on region

STEP 2 – Compute progressive tax
  tax = 0
  for each bracket (lower, upper, rate):
      if gross_income > lower:
          taxable_in_bracket = min(gross_income, upper) - lower
          tax += taxable_in_bracket * rate

STEP 3 – Output total tax
  total_tax = tax
```

---

## 5. Example calculation (gross income 700 000 NOK, Standard region)

| Bracket | Portion in bracket (NOK) | Rate | Tax (NOK) |
|---|---|---|---|
| 1 (0 – 208 050) | 208 050 | 0 % | 0 |
| 2 (208 051 – 292 850) | 84 800 | 23.7 % | 20 098 |
| 3 (292 851 – 670 000) | 377 150 | 26.0 % | 98 059 |
| 4 (670 001 – 700 000) | 30 000 | 35.6 % | 10 680 |
| **Total** | | | **128 837** |
