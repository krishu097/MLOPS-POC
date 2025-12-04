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

# OIDC Provider - created after EKS cluster
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
  depends_on = [module.eks]
}

data "tls_certificate" "eks" {
  url = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer

  depends_on = [module.eks]
}

# OIDC Provider - created after EKS cluster
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
  depends_on = [module.eks]
}

data "tls_certificate" "eks" {
  url = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = data.aws_eks_cluster.cluster.identity[0].oidc[0].issuer

  depends_on = [module.eks]
}