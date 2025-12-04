variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "mlops-cluster"
}

variable "cluster_version" {
  description = "Kubernetes version to use for the EKS cluster"
  type        = string
  default     = "1.28"
}

variable "cluster_iam_role_arn" {
  description = "ARN of the IAM role for the EKS cluster"
  type        = string
}

variable "node_iam_role_arn" {
  description = "ARN of the IAM role for the EKS node group"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs where the EKS cluster will be deployed"
  type        = list(string)
}

variable "ebs_csi_driver_role" {
  description = "ARN of the IAM role for EBS CSI driver"
  type        = string
}

variable "eks_ecr_access_role" {
  description = "ARN of the IAM role for ECR access"
  type        = string
}

variable "eks_aws_load_balancer_controller_role" {
  description = "ARN of the IAM role for AWS Load Balancer Controller"
  type        = string
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}