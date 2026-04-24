#!/usr/bin/env python3
import sys
import os
from solutions.gemma4.tax_calculator import calculate_tax_for_data

def main():
    """
    Main entry point for the tax calculator CLI.
    Expected usage: python tax_calculator_cli.py <input_file_path>
    """
    if len(sys.argv) != 2:
        print("Error: Please provide exactly one argument: the path to the input tax data file.")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    if not os.path.exists(input_file_path):
        print(f"Error: Input file not found at {input_file_path}")
        sys.exit(1)
        
    try:
        with open(input_file_path, 'r') as f:
            data_content = f.read()
        
        # Pass the content to the processing function
        calculate_tax_for_data(data_content)
        
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
