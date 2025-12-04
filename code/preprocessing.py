import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import argparse
import os
import boto3

def format_raw_data(raw_file):
    """Format messy CSV data into clean structure"""
    formatted_data = []
    
    with open(raw_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        parts = [part.strip() for part in line.strip().split(',')]
        
        if len(parts) < 12:
            continue
            
        try:
            formatted_data.append({
                'loan_id': int(parts[0]),
                'no_of_dependents': int(parts[1]),
                'education': parts[2].strip(),
                'self_employed': parts[3].strip(),
                'income_annum': int(parts[4]),
                'loan_amount': int(parts[5]),
                'loan_term': int(parts[6]),
                'credit_score': int(parts[7]),
                'residential_assets_value': int(parts[8]),
                'commercial_assets_value': int(parts[9]),
                'luxury_assets_value': int(parts[10]),
                'bank_asset_value': int(parts[11]),
                'loan_status': parts[12].strip()
            })
        except (ValueError, IndexError):
            continue
    
    return pd.DataFrame(formatted_data)

def preprocess_data():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-data', type=str, default='/opt/ml/processing/input')
    parser.add_argument('--output-train', type=str, default='/opt/ml/processing/train')
    parser.add_argument('--output-test', type=str, default='/opt/ml/processing/test')
    
    args = parser.parse_args()
    
    # Format raw data first
    raw_file = f"{args.input_data}/data.csv"
    df = format_raw_data(raw_file)
    
    print(f"Formatted {len(df)} records")
    
    # Feature engineering
    df['education'] = df['education'].map({'Graduate': 0, 'Not Graduate': 1})
    df['self_employed'] = df['self_employed'].map({'No': 0, 'Yes': 1})
    df['loan_status'] = df['loan_status'].map({'Approved': 1, 'Rejected': 0})
    
    # Calculate total assets
    df['total_assets'] = (df['residential_assets_value'] + 
                         df['commercial_assets_value'] + 
                         df['luxury_assets_value'] + 
                         df['bank_asset_value'])
    
    # Log transform numerical features (add 1 to handle zeros/negatives)
    numerical_cols = ['income_annum', 'loan_amount', 'total_assets']
    for col in numerical_cols:
        df[col] = np.log(np.abs(df[col]) + 1)
    
    # Select features for training
    feature_cols = ['no_of_dependents', 'education', 'self_employed', 'income_annum', 
                   'loan_amount', 'loan_term', 'credit_score', 'total_assets']
    
    X = df[feature_cols]
    y = df['loan_status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save processed data
    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)
    
    train_data.to_csv(f"{args.output_train}/train.csv", index=False)
    test_data.to_csv(f"{args.output_test}/test.csv", index=False)
    
    print("✅ Data preprocessing completed")

if __name__ == "__main__":
    preprocess_data()