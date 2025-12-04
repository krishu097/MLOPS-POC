import pandas as pd
import joblib
import json
import argparse
import os
from sklearn.metrics import accuracy_score, f1_score

def evaluate_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str, default='/opt/ml/processing/model')
    parser.add_argument('--test-path', type=str, default='/opt/ml/processing/test')
    parser.add_argument('--evaluation-path', type=str, default='/opt/ml/processing/evaluation')
    
    args = parser.parse_args()
    
    # Load test data
    test_df = pd.read_csv(f"{args.test_path}/test.csv")
    X_test = test_df.drop('loan_status', axis=1)
    y_test = test_df['loan_status']
    
    # Load model
    model = joblib.load(f"{args.model_path}/model.pkl")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Evaluation report
    report = {
        "metrics": {
            "accuracy": accuracy,
            "f1_score": f1
        },
        "approval_criteria": {
            "min_accuracy": 0.7,
            "min_f1_score": 0.7
        },
        "approved": accuracy >= 0.7 and f1 >= 0.7
    }
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Model Approved: {report['approved']}")
    
    # Save evaluation report
    os.makedirs(args.evaluation_path, exist_ok=True)
    with open(f"{args.evaluation_path}/evaluation.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    evaluate_model()