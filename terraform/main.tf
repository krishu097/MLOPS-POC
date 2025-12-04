# VPC Module
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr           = var.vpc_cidr
  azs                = var.azs
  name_prefix        = var.name_prefix
  enable_nat_gateway = var.enable_nat_gateway

  tags = var.tags
}

# EKS Module
module "eks" {
  source = "./modules/eks"

  cluster_name                           = var.cluster_name
  cluster_version                        = var.cluster_version
  cluster_iam_role_arn                   = aws_iam_role.eks_cluster_role.arn
  node_iam_role_arn                      = aws_iam_role.eks_node_role.arn
  subnet_ids                             = concat(module.vpc.private_subnets, module.vpc.public_subnets)
  ebs_csi_driver_role                    = aws_iam_role.ebs_csi_driver_role.arn
  eks_ecr_access_role                    = aws_iam_role.eks_ecr_access_role.arn
  eks_aws_load_balancer_controller_role  = aws_iam_role.aws_load_balancer_controller_role.arn

  tags = var.tags
}