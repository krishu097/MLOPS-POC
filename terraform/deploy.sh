#!/bin/bash

echo "🚀 Deploying MLOps EKS Infrastructure..."

# Initialize Terraform with backend config
echo "🔧 Initializing Terraform..."
terraform init -backend-config=../tf_env/Backend_Uat_Config_Ohio.config

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan -var-file=../tf_env/MLOps_Deployment.tfvars

# Ask for confirmation
read -p "🤔 Do you want to proceed with deployment? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Apply the configuration
echo "🚀 Deploying infrastructure..."
terraform apply -var-file=../tf_env/MLOps_Deployment.tfvars -auto-approve

# Get outputs
echo "📊 Deployment completed! Here are the important details:"
echo ""
echo "✅ EKS Cluster: $(terraform output -raw cluster_name)"
echo "✅ ECR Repository: $(terraform output -raw ecr_repository_url)"
echo "✅ VPC ID: $(terraform output -raw vpc_id)"

echo ""
echo "🎯 Next steps:"
echo "   1. Configure kubectl: aws eks update-kubeconfig --name $(terraform output -raw cluster_name)"
echo "   2. Push code to GitHub to trigger MLOps pipeline"
echo "   3. Monitor GitHub Actions for build and deployment"
echo "   4. Access your ML model via ALB endpoint"