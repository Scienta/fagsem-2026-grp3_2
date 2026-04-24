# Skattekalkulator for Norge (Østlandet)

## Oppsett

1. Sørg for at virtual environment er aktivert:
```bash
.venv/Scripts/activate  # Windows
.venv/bin/activate      # Linux/Mac
```

2. Kjør løsningen:
```bash
python solutions/claude_glm/tax_calculator.py <input-fil> [output-fil]
```

## Input-format

Filformat er enkelt: hver linje representerer en person.

Format:
```
<navn>
<alder>
<inntekt>
```

Eksempel (test_input.txt):
```
Ola Nordmann
30
600000
```

## Beregnede satser

- **Inntektsskatt**: 22%
- **Trinnskatt**: Progressivt basert på inntekt (5 trinn)
- **Trygdeavgift**: 7.8% (maks 25% på overskudd over 83,000)
- **Personfradrag**: 88,250
- **Minstefradrag**: 46% av bruttoinntekt (maks 104,450)

## Output-format

Fil med navn og total skatt:
```
Ola Nordmann
150133 NOK
```

## Koden

Løsningen er skrevet i `tax_calculator.py` og inneholder:

1. `TaxCalculator`-klassen som håndterer skattberegningen
2. Funksjoner for å lese input og skrive output
3. Støtte for lønn, pensjon og næringsinntekt
4. Alvorlig iht. skatt.md for Østlandet

## Eksempel

```
$ python solutions/claude_glm/tax_calculator.py test_input.txt
Skatt beregnet for 2 personer
Resultat lagret i: resultat.txt
```

Se `resultat.txt` for resultater.