import joblib
import pandas as pd
import numpy as np
import json
import os

def model_fn(model_dir):
    """Load model from the model_dir"""
    model = joblib.load(os.path.join(model_dir, "model.pkl"))
    return model

def input_fn(request_body, request_content_type):
    """Parse input data for predictions"""
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        df = pd.DataFrame([input_data])
        
        # Feature engineering
        if 'education' in df.columns:
            df['education'] = df['education'].str.strip().map({'Graduate': 0, 'Not Graduate': 1})
        if 'self_employed' in df.columns:
            df['self_employed'] = df['self_employed'].str.strip().map({'No': 0, 'Yes': 1})
        
        # Calculate total assets if individual asset columns exist
        if all(col in df.columns for col in ['residential_assets_value', 'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value']):
            df['total_assets'] = (df['residential_assets_value'] + 
                                 df['commercial_assets_value'] + 
                                 df['luxury_assets_value'] + 
                                 df['bank_asset_value'])
            
            # Log transform
            numerical_cols = ['income_annum', 'loan_amount', 'total_assets']
            for col in numerical_cols:
                if col in df.columns:
                    df[col] = np.log(df[col] + 1)
            
            # Select features
            feature_cols = ['no_of_dependents', 'education', 'self_employed', 'income_annum', 
                           'loan_amount', 'loan_term', 'credit_score', 'total_assets']
        else:
            # Fallback for old structure
            numerical_cols = ['income_annum', 'loan_amount', 'total_asset']
            for col in numerical_cols:
                if col in df.columns:
                    df[col] = np.log(df[col] + 1)
            
            feature_cols = ['no_of_dependents', 'education', 'self_employed', 'income_annum', 
                           'loan_amount', 'loan_term', 'credit_score', 'total_asset']
        
        return df[feature_cols]
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Make predictions using the loaded model"""
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    return {"prediction": prediction, "probability": probability}

def output_fn(prediction, content_type):
    """Format the output"""
    if content_type == 'application/json':
        result = {
            "prediction": int(prediction["prediction"][0]),
            "loan_status": "Approved" if prediction["prediction"][0] == 1 else "Rejected",
            "confidence": float(max(prediction["probability"][0]))
        }
        return json.dumps(result)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")