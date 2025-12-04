import json
import boto3
import urllib.request
import urllib.parse
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
            
            # Create request
            req_data = json.dumps(data).encode('utf-8')
            request = urllib.request.Request(url, data=req_data, headers=headers)
            request.add_header('Content-Type', 'application/json')
            
            try:
                response = urllib.request.urlopen(request)
                if response.getcode() == 204:
                    print(f"✅ Training triggered for: {key}")
                else:
                    print(f"❌ Unexpected response code: {response.getcode()}")
            except Exception as e:
                print(f"❌ Failed to trigger: {e}")
    
    return {'statusCode': 200}