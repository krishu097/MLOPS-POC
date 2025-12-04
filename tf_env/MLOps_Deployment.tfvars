aws_region = "us-east-2"
cluster_name = "mlops-cluster"
cluster_version = "1.33"
vpc_cidr = "10.0.0.0/16"
azs = ["us-east-2a", "us-east-2b"]
name_prefix = "mlops"
enable_nat_gateway = true

tags = {
  Environment = "mlops"
  Project     = "loan-prediction"
  Owner       = "mlops-team"
}

github_owner = "krishu097"
github_repo  = "MLOPS-POC"

# S3 bucket for training data (your existing bucket)
training_data_bucket = "poc-mlops-bucket-gmk"