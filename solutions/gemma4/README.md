# NOTAT

Denne ble generert med simplertask.md av opencode og gemma4. 

# Tax Calculator Utility

## Overview
This project provides a command-line utility to calculate progressive tax owed for wage earners in Norway for the income year 2024, according to simplified regional tax rules.

## Usage
The program requires a single input file containing tax data. The data format must contain records for multiple taxpayers, where each record includes the name, age, gross income, and region.

Run the program using the following command:

```bash
python solutions/gemma4/tax_calculator_cli.py <path_to_input_file>
```

## Input Data Format
The input file should contain records like the example below. Tax records are expected to follow a pattern (Name, Age, Income, Region).

**Example input file (`taxdata.txt`):**
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

## Output
The result is printed to standard output, listing each taxpayer's name followed by the calculated tax owed.

**Example output:**
```
Roger Rud
20 000 NOK

Per Høneeier
1 000 000 NOK
```

## Project Status
* **Initiated:** Apr 24 2026
* **Completed:** Apr 24 2026
