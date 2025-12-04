#!/bin/bash

# Secure Terraform Deployment Script

set -e

echo "🔐 Secure MLOps Infrastructure Deployment"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "📋 Please copy .env.example to .env and fill in your values"
    exit 1
fi

# Load environment variables
echo "🔧 Loading environment variables..."
source .env

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found!"
    echo "📋 Please copy terraform.tfvars.example to terraform.tfvars and fill in your values"
    exit 1
fi

# Validate required environment variables
if [ -z "$TF_VAR_github_token" ]; then
    echo "❌ TF_VAR_github_token not set in .env file"
    exit 1
fi

echo "✅ Environment variables loaded"

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Plan deployment
echo "📋 Planning deployment..."
terraform plan

# Ask for confirmation
read -p "🤔 Do you want to proceed with deployment? (y/N): " confirm
if [[ $confirm != [yY] ]]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

# Apply deployment
echo "🚀 Deploying infrastructure..."
terraform apply -auto-approve

echo "✅ Infrastructure deployed successfully!"
echo ""
echo "📊 Outputs:"
terraform output