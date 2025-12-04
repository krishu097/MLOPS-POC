import pandas as pd
import joblib
import os
import argparse
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

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

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-file', type=str, default='data.csv')
    parser.add_argument('--output-dir', type=str, default='./model')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Read training data
    try:
        df = pd.read_csv(args.data_file)
        # Check if data needs formatting
        if 'loan_id' not in df.columns:
            df = format_raw_data(args.data_file)
    except:
        df = format_raw_data(args.data_file)
    
    print(f"Training with {len(df)} records")
    
    # Feature engineering
    df['education'] = df['education'].map({'Graduate': 0, 'Not Graduate': 1})
    df['self_employed'] = df['self_employed'].map({'No': 0, 'Yes': 1})
    df['loan_status'] = df['loan_status'].map({'Approved': 1, 'Rejected': 0})
    
    # Calculate total assets
    df['total_assets'] = (df['residential_assets_value'] + 
                         df['commercial_assets_value'] + 
                         df['luxury_assets_value'] + 
                         df['bank_asset_value'])
    
    # Log transform numerical features
    numerical_cols = ['income_annum', 'loan_amount', 'total_assets']
    for col in numerical_cols:
        df[col] = np.log(np.abs(df[col]) + 1)
    
    # Select features
    feature_cols = ['no_of_dependents', 'education', 'self_employed', 'income_annum', 
                   'loan_amount', 'loan_term', 'credit_score', 'total_assets']
    
    X = df[feature_cols]
    y = df['loan_status']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Save model
    joblib.dump(model, os.path.join(args.output_dir, 'model.pkl'))
    
    # Save metrics
    metrics = {'accuracy': accuracy, 'f1_score': f1}
    with open(os.path.join(args.output_dir, 'metrics.json'), 'w') as f:
        import json
        json.dump(metrics, f)
    
    print(f"Model saved successfully with accuracy: {accuracy:.4f}, F1: {f1:.4f}")

if __name__ == '__main__':
    train()