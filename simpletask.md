The task is to produce a command-line utility in Python that can perform the following task: 

1. Read a file containing tax data for one or more persons who are wage earners in Eastern Norway.
2. For each person, calculate tax owed. The rules for the calculation can be found in the Appendix A
3. Output the result of the calculation for each person.

The program should written from scratch as a stand-alone project, in the output directory given by the `$FILE_DIR`
environment variable.

The program should accept a single input file as an argument and produce the answer on stdout.

The project directory should contain a `README.md` file with instructions on how to run the program. For evaluation
purposes, the README file should contain a section saying when the project was initiated, and when it was completed. The
timestamps should be in a resolution of seconds.

Example input file, with two taxpayers where name, age, and income are provided:

```
Roger Rud
50 years
125 000 NOK

Per Høneeier
42 years
7 000 000 NOK
```

Example result output, where the taxpayers are listed with tax owed:

```
Roger Rud
20 000 NOK

Per Hønseeier
1 000 000
```

# Appendix A

# Norwegian tax rules (simplified) – for a tax calculator

> **Validity:** Income year 2024 (tax settlement 2025)
> **Audience:** Coding agent implementing a Norwegian tax calculator
> **Source:** Skatteetaten.no (simplified presentation – not legal advice)

---

## 1. Basic concepts

| Term | Explanation |
|---|---|
| **Gross income** | Wages, business income, pension, etc. before deductions |
| **Ordinary income** | Gross income minus all deductions (minimum deduction, personal deduction, interest, etc.) |
| **Personal income** | Gross income (wages/pension) – basis for bracket tax and national insurance contribution |
| **Tax municipality** | The municipality one is resident in as of January 1 of the income year |

---

## 2. Taxes and contributions – overview

A typical Norwegian wage earner pays four components:

```
Total tax = Income tax (flat) + Bracket tax + National insurance contribution + (Wealth tax if applicable)
```

---

## 3. Income tax (flat tax on ordinary income)

Flat rate on **ordinary income** (after deductions):

| Taxpayer | Rate |
|---|---|
| Person resident in Norway (outside Finnmark/Nord-Troms) | **22 %** |
| Person resident in Finnmark or Nord-Troms | **18.5 %** |

> The rate covers the sum of municipal tax + county tax + common tax.

---

## 4. Bracket tax (on personal income)

Bracket tax is calculated **directly on gross personal income** (wages, pension) – **no deductions are subtracted**.

### Wage earners and self-employed – brackets 2024

| Bracket | Income from (NOK) | Income to (NOK) | Rate |
|---|---|---|---|
| 1 | 208 051 | 292 850 | 1.7 % |
| 2 | 292 851 | 670 000 | 4.0 % |
| 3 | 670 001 | 937 900 | 13.6 % |
| 4 | 937 901 | 1 350 000 | 16.6 % |
| 5 | 1 350 001 | ∞ | 17.6 % |

> Below 208 051 NOK: **no bracket tax**

### Pensioners – brackets 2024

| Bracket | Income from (NOK) | Income to (NOK) | Rate |
|---|---|---|---|
| 1 | 208 051 | 292 850 | 0.9 % |
| 2 | 292 851 | 670 000 | 2.0 % |
| 3 | 670 001 | 937 900 | 11.8 % |
| 4 | 937 901 | 1 350 000 | 14.8 % |
| 5 | 1 350 001 | ∞ | 17.6 % |

**Calculation (bracket tax is progressive – marginal per bracket):**
```
bracket_tax = sum over all brackets of:
    min(personal_income, upper_limit) - lower_limit) * rate
    (only if personal_income > lower_limit)
```

---

## 5. National insurance contribution (on personal income)

| Income type | Rate 2024 |
|---|---|
| Wage income | **7.8 %** |
| Business income (self-employed) | **11.0 %** |
| Pension and benefits | **5.1 %** |
| Below the exemption threshold (83 000 NOK) | **0 %** |

**Phase-in rule (exemption threshold):**
The national insurance contribution **cannot exceed 25 % of income above 83 000 NOK**.
This prevents the contribution from consuming more than the surplus at low income levels.

```
max_national_insurance = 0.25 * max(0, personal_income - 83_000)
national_insurance = min(rate * personal_income, max_national_insurance)
```

---

## 6. Deductions

### 6.1 Minimum deduction (automatic)

Calculated automatically for wages and pensions. Subtracted from gross income before tax on ordinary income.

| Type | Rate | Minimum (NOK) | Maximum (NOK) |
|---|---|---|---|
| Wages | 46 % of wages | 4 000 | 104 450 |
| Pension | 40 % of pension | 4 000 | 86 250 |

```
minimum_deduction_wages = max(4_000, min(0.46 * wages, 104_450))
minimum_deduction_pension = max(4_000, min(0.40 * pension, 86_250))
```

### 6.2 Personal deduction

Fixed amount subtracted from ordinary income after the minimum deduction.

| Tax class | Amount 2024 (NOK) |
|---|---|
| Class 1 (all adults) | 88 250 |
| Class 2 (discontinued) | No longer in use |

> Nearly all taxpayers use class 1.

### 6.3 Other common deductions (optional to implement)

| Deduction | Max (NOK) | Description |
|---|---|---|
| Interest expenses | Unlimited | Debt interest on mortgages etc. |
| BSU (home savings for youth) | 27 500/year saved → 10 % tax deduction (max 2 750 NOK) | Under 34 years of age |
| Union dues | 7 700 | Direct deduction from ordinary income |
| Commuter deduction | Varies | Travel expenses above 14 400 NOK/year |
| Parental deduction | 25 000 (1 child), +15 000 per additional child | Childcare |

---

## 7. Calculation – step by step

```
INPUT:
  - gross_wages         (NOK)
  - other_income        (NOK, e.g. pension, capital income)
  - interest_expenses   (NOK)
  - other_deductions    (NOK, sum of optional deductions)
  - income_type         ("wages" | "pension" | "business")

STEP 1 – Calculate personal income
  personal_income = gross_wages + other_income (only wages/pension/business)

STEP 2 – Calculate minimum deduction
  minimum_deduction = max(4_000, min(0.46 * gross_wages, 104_450))
  (use pension rate if pension)

STEP 3 – Calculate ordinary income
  ordinary_income = personal_income
                    - minimum_deduction
                    - personal_deduction (88_250)
                    - interest_expenses
                    - other_deductions
  ordinary_income = max(0, ordinary_income)  # never negative

STEP 4 – Income tax (22 %)
  income_tax = ordinary_income * 0.22

STEP 5 – Bracket tax
  bracket_tax = sum of marginal tax per bracket (see table above)

STEP 6 – National insurance contribution
  raw_national_insurance = personal_income * rate  (7.8% / 11% / 5.1%)
  max_national_insurance = max(0, personal_income - 83_000) * 0.25
  national_insurance = min(raw_national_insurance, max_national_insurance)

STEP 7 – Total tax
  total_tax = income_tax + bracket_tax + national_insurance

STEP 8 – Net income
  net = gross_wages - total_tax
  effective_tax_rate = total_tax / gross_wages * 100
```

---

## 8. Example calculation (wages 700 000 NOK, 2024)

| Item | Amount (NOK) |
|---|---|
| Gross wages | 700 000 |
| Minimum deduction | −104 450 (max) |
| Personal deduction | −88 250 |
| **Ordinary income** | **507 300** |
| Income tax (22 %) | 111 606 |
| Bracket tax (brackets 1+2+3 partial) | 1 445 + 15 124 + 4 082 = **20 651** |
| National insurance contribution (7.8 %) | 54 600 |
| **Total tax** | **186 857** |
| **Net income** | **513 143** |
| **Effective tax rate** | **26.7 %** |

---

## 9. Wealth tax (optional to implement)

| Threshold | Rate |
|---|---|
| Below 1 700 000 NOK (single) / 3 400 000 NOK (married couple) | 0 % |
| Above the threshold | 1.0 % (municipal 0.7 % + state 0.3 %) |

Wealth includes: bank deposits (100 %), shares (80 % of value), primary residence (25 % of market value), secondary residence (100 %), holiday property (30 % of value), minus debt.
