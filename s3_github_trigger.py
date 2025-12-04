import json
import boto3
import requests
import os

def lambda_handler(event, context):
    """Trigger GitHub Actions when new data arrives in S3"""
    
    # Get GitHub token from Secrets Manager
    secrets_client = boto3.client('secretsmanager')
    secret_name = os.environ['SECRET_NAME']
    
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        github_token = response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return {'statusCode': 500, 'body': 'Failed to retrieve GitHub token'}
    
    repo_owner = os.environ['GITHUB_OWNER'] 
    repo_name = os.environ['GITHUB_REPO']
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Only trigger for training data
        if key.startswith('training-data/') and key.endswith('.csv'):
            
            # Trigger GitHub Actions workflow
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/mlops-pipeline.yaml/dispatches"
            
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'ref': 'main',
                'inputs': {
                    'trigger_reason': f'New data uploaded: {key}',
                    'data_path': f's3://{bucket}/{key}'
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 204:
                print(f"✅ Training triggered for: {key}")
            else:
                print(f"❌ Failed to trigger: {response.text}")
    
    return {'statusCode': 200}