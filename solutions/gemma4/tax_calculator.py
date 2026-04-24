from typing import List, Dict, Tuple

# Define tax brackets structure: (income_from, income_to, rate_percentage)
# income_to = float('inf') indicates no upper bound
TaxBracket = Tuple[float, float, float]
TaxRules = List[TaxBracket]

STANDARD_BRACKETS: TaxRules = [
    (0.0, 208050.0, 0.0),  # Bracket 1: 0 - 208,050, 0 %
    (208051.0, 292850.0, 0.237), # Bracket 2: 208,051 - 292,850, 23.7 %
    (292851.0, 670000.0, 0.260), # Bracket 3: 292,851 - 670,000, 26.0 %
    (670001.0, 937900.0, 0.356), # Bracket 4: 670,001 - 937,900, 35.6 %
    (937901.0, 1350000.0, 0.386), # Bracket 5: 937,901 - 1,350,000, 38.6 %
    (1350001.0, float('inf'), 0.396), # Bracket 6: 1,350,001 - infinity, 39.6 %
]

REDUCED_BRACKETS: TaxRules = [
    (0.0, 208050.0, 0.0), # Bracket 1: 0 - 208,050, 0 %
    (208051.0, 292850.0, 0.202), # Bracket 2: 208,051 - 292,850, 20.2 %
    (292851.0, 670000.0, 0.225), # Bracket 3: 292,851 - 670,000, 22.5 %
    (670001.0, 937900.0, 0.321), # Bracket 4: 670,001 - 937,900, 32.1 %
    (937901.0, 1350000.0, 0.351), # Bracket 5: 937,901 - 1,350,000, 35.1 %
    (1350001.0, float('inf'), 0.361), # Bracket 6: 1,350,001 - infinity, 36.1 %
]

def calculate_tax(gross_income: float, region: str) -> float:
    """
    Calculates the progressive tax owed based on gross income and region.
    
    Args:
        gross_income: The total gross income in NOK.
        region: The tax region ("standard" or "reduced").
        
    Returns:
        The total tax owed in NOK.
        
    Raises:
        ValueError: If the region is unknown.
    """
    
    if region.lower() == "standard":
        brackets = STANDARD_BRACKETS
    elif region.lower() == "reduced":
        brackets = REDUCED_BRACKETS
    else:
        raise ValueError("Invalid region specified. Must be 'standard' or 'reduced'.")

    total_tax = 0.0
    remaining_income = gross_income
    
    # Iterate through brackets to calculate progressive tax
    for lower, upper, rate in brackets:
        if remaining_income <= 0:
            break

        # Determine the portion of income that falls within this bracket
        # The taxable amount starts from 'lower' and goes up to 'upper'
        
        # Check if the bracket entirely precedes the income
        if gross_income <= lower:
            continue
        
        # Calculate the upper limit for taxation in this bracket
        taxable_upper = min(gross_income, upper)
        
        # Calculate amount subject to tax in the current bracket
        taxable_amount = taxable_upper - lower + (1 if lower > 0 and taxable_upper >= lower else 0)
        
        if taxable_amount > 0:
            tax_contribution = taxable_amount * rate
            total_tax += tax_contribution
            
    # Rounding to integer NOK for final output consistency (though float calculation is safer)
    return round(total_tax) # Return as integer/whole number of NOK


def parse_taxpayer_data(data_string: str) -> Tuple[str, float, str]:
    """
    Parses a chunk of the input data to extract Name, Income, and Region.
    
    The data format is assumed to be:
    - Name (2 lines: first line has name, second line might be age/description)
    - Age (1 line: contains 'years')
    - Income (1 line: contains numbers and 'NOK')
    - Region (1 line)
    
    Returns: A tuple (name, income, region)
    """
    lines = [line.strip() for line in data_string.splitlines() if line.strip()]
    
    if len(lines) < 4:
        raise ValueError("Insufficient data lines found for a taxpayer record.")
        
    # Extract Name (Assuming first name is the entity name)
    name = f"{lines[0].split()[0]} {lines[0].split()[-1]}"
    
    try:
        # Extract Income (find the line containing NOK)
        income_line = next(line for line in lines[2:4] if "NOK" in line)
        # Clean up the income string (remove spaces/separators)
        formatted_income = "".join(filter(str.isdigit, income_line.replace(" ", ""))).replace(",", "")
        gross_income = float(formatted_income)
    except StopIteration:
        raise ValueError("Could not find income amount in the data.")
    except Exception as e:
        raise ValueError(f"Error parsing income: {e}")
    
    # Extract Region (Assume the last line is the region)
    region = lines[-1]
    
    return name, gross_income, region


def calculate_tax_for_data(data_string: str):
    """
    Main handler function to process a string of raw input data.
    """
    try:
        # Use a simplified multi-line assumption based on the example
        # To robustly handle the structure (Name/Age/Income/Region are somewhat grouped)
        
        # Split the entire data string into chunks representing individual taxpayers
        # Since the input structure is Name\nAge\nIncome\nRegion and the new record starts with Name,
        # we assume a clean separation can be inferred.
        
        # A reliable assumption based on the prompt's example structure:
        # The entire data is a continuous block. Taxpayer records are separated by a distinct pattern.
        
        # Given the manual parsing requirement, we must rely on the observable grouping.
        # Since there's no clear delimiter, we'll process in chunks that yield 4 logical lines.
        
        # This parsing method requires explicit knowledge of the input pattern separation.
        # Assuming the input file is structured such that records are separated cleanly.
        
        # For simulation, we'll assume records are grouped by consecutive lines:
        all_lines = [line.strip() for line in data_string.splitlines() if line.strip()]
        
        clean_records = []
        
        # The structure suggests groups of 4 logical lines, but name/age are conflated on lines 0 and 1
        
        if len(all_lines) < 4:
            print("Error: Input data does not contain enough records for calculation.")
            return
        
        # Process groups of 4 lines
        for i in range(0, len(all_lines), 4):
            if i + 3 >= len(all_lines):
                # Skip incomplete records at the end
                break
                
            # The prompt example suggests Name is on line 0, Age on line 1, Income on line 2, Region on line 3
            # But the example shows Name/Age/Income/Region are blocks, not individual lines.
            
            # L0: Roger Rud
            # L1: 50 years
            # L2: 125 000 NOK
            # L3: Eastern Norway
            
            record_lines = all_lines[i:i+4]
            
            # Reusing the robust parsing for each expected group of lines
            name, income, region = parse_taxpayer_data("\\n".join(record_lines))
            clean_records.append((name, income, region))


        results = []
        for name, income, region in clean_records:
            tax_owed = calculate_tax(income, region)
            results.append((name, tax_owed))


        # Output the results according to the specified format
        for name, tax_owed in results:
            print(f"{name}")
            print(f"{tax_owed:,.0f} NOK")

    except ValueError as e:
        print(f"Error processing data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python tax_calculator_cli.py <input_file_path>")
    else:
        input_file_path = sys.argv[1]
        with open(input_file_path, 'r') as f:
            data_content = f.read()
        calculate_tax_for_data(data_content)
