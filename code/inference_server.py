from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
import os

app = Flask(__name__)

# Load model at startup
model = joblib.load('./model/model.pkl')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Prepare features
        features = [
            data.get('no_of_dependents', 0),
            1 if data.get('education') == 'Not Graduate' else 0,
            1 if data.get('self_employed') == 'Yes' else 0,
            np.log(abs(data.get('income_annum', 1)) + 1),
            np.log(abs(data.get('loan_amount', 1)) + 1),
            data.get('loan_term', 12),
            data.get('credit_score', 300),
            np.log(abs(
                data.get('residential_assets_value', 0) +
                data.get('commercial_assets_value', 0) +
                data.get('luxury_assets_value', 0) +
                data.get('bank_asset_value', 0)
            ) + 1)
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]
        
        result = {
            'prediction': 'Approved' if prediction == 1 else 'Rejected',
            'probability': {
                'approved': float(probability[1]),
                'rejected': float(probability[0])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)