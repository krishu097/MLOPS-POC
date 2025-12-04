import pandas as pd
import numpy as np
import re

def format_loan_data(input_file, output_file):
    """Format the messy loan data into clean CSV structure"""
    
    # Read the raw data
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Clean and parse each line
    formatted_data = []
    
    for line in lines:
        # Remove extra spaces and split by comma
        parts = [part.strip() for part in line.strip().split(',')]
        
        # Skip empty lines or incomplete rows
        if len(parts) < 12:
            continue
            
        try:
            # Extract data based on expected structure
            loan_id = int(parts[0])
            no_of_dependents = int(parts[1])
            education = parts[2].strip()
            self_employed = parts[3].strip()
            income_annum = int(parts[4])
            loan_amount = int(parts[5])
            loan_term = int(parts[6])
            credit_score = int(parts[7])
            residential_assets_value = int(parts[8])
            commercial_assets_value = int(parts[9])
            luxury_assets_value = int(parts[10])
            bank_asset_value = int(parts[11])
            loan_status = parts[12].strip()
            
            formatted_data.append({
                'loan_id': loan_id,
                'no_of_dependents': no_of_dependents,
                'education': education,
                'self_employed': self_employed,
                'income_annum': income_annum,
                'loan_amount': loan_amount,
                'loan_term': loan_term,
                'credit_score': credit_score,
                'residential_assets_value': residential_assets_value,
                'commercial_assets_value': commercial_assets_value,
                'luxury_assets_value': luxury_assets_value,
                'bank_asset_value': bank_asset_value,
                'loan_status': loan_status
            })
            
        except (ValueError, IndexError):
            # Skip malformed rows
            continue
    
    # Create DataFrame and save
    df = pd.DataFrame(formatted_data)
    df.to_csv(output_file, index=False)
    print(f"✅ Formatted {len(df)} records and saved to {output_file}")
    
    return df

if __name__ == "__main__":
    format_loan_data('data.csv', 'data_formatted.csv')