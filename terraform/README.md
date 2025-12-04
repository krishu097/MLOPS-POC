# MLOps Infrastructure with Terraform

This directory contains Terraform configurations to deploy the complete MLOps infrastructure on AWS.

## Infrastructure Components

- **S3 Buckets**: ML artifacts and pipeline artifacts storage
- **IAM Roles**: SageMaker execution and CodeBuild/CodePipeline roles
- **CodePipeline**: CI/CD pipeline triggered by GitHub pushes
- **CodeBuild**: Build environment for ML pipeline execution
- **SageMaker**: ML pipeline, model registry, and endpoints

## Quick Start

1. **Configure Variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values (except github_token)
   ```

2. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your GitHub token and AWS credentials
   ```

3. **Deploy Infrastructure**:
   ```bash
   ./deploy-secure.sh
   ```

### Alternative: Export Variables Manually
```bash
export TF_VAR_github_token="your-token-here"
terraform init
terraform plan
terraform apply
```

3. **Push Code to GitHub**:
   - Pipeline automatically triggers on push
   - Monitors `data.csv` changes
   - Trains and deploys models automatically

## Configuration

### Required Variables

- `github_owner`: Your GitHub username
- `github_repo`: Repository name
- `github_token`: Personal access token with repo permissions
- `aws_region`: AWS region (default: eu-central-1)
- `bucket_name`: S3 bucket name (default: teamars)

### GitHub Token Permissions

Your GitHub token needs:
- `repo` (Full control of private repositories)
- `admin:repo_hook` (Read and write repository hooks)

## Cleanup

```bash
./destroy.sh
```

## Manual Commands

```bash
# Initialize
terraform init

# Plan
terraform plan

# Deploy
terraform apply

# Destroy
terraform destroy
```