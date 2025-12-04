resource "aws_eks_cluster" "mlops-cluster" {
  name     = var.cluster_name
  version  = var.cluster_version
  role_arn = var.cluster_iam_role_arn

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  tags = var.tags

  depends_on = [aws_cloudwatch_log_group.eks]
}

resource "aws_eks_addon" "ebs_csi_driver" {
  cluster_name  = aws_eks_cluster.mlops-cluster.name
  addon_name    = "aws-ebs-csi-driver"
  addon_version = "v1.35.0-eksbuild.1"

  service_account_role_arn = var.ebs_csi_driver_role

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  tags = var.tags

  depends_on = [aws_eks_node_group.mlops-node-group]
}

resource "aws_eks_addon" "cloudwatch_observability" {
  cluster_name  = aws_eks_cluster.mlops-cluster.name
  addon_name    = "amazon-cloudwatch-observability"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  tags = var.tags

  depends_on = [aws_eks_node_group.mlops-node-group]
}

resource "kubernetes_service_account" "ecr_pull_sa" {
  metadata {
    name      = "ecr-pull-sa"
    namespace = "default"
    annotations = {
      "eks.amazonaws.com/role-arn" = var.eks_ecr_access_role
    }
  }
  depends_on = [aws_eks_cluster.mlops-cluster, aws_eks_node_group.mlops-node-group]
}

resource "kubernetes_service_account" "aws_load_balancer_controller" {
  metadata {
    name      = "aws-load-balancer-controller"
    namespace = "kube-system"
    annotations = {
      "eks.amazonaws.com/role-arn" = var.eks_aws_load_balancer_controller_role
    }
    labels = {
      "app.kubernetes.io/name"      = "aws-load-balancer-controller"
      "app.kubernetes.io/component" = "controller"
    }
  }

  depends_on = [aws_eks_cluster.mlops-cluster, aws_eks_node_group.mlops-node-group]
}

resource "aws_cloudwatch_log_group" "eks" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 30
  tags              = var.tags
}

resource "aws_eks_node_group" "mlops-node-group" {
  cluster_name    = aws_eks_cluster.mlops-cluster.name
  node_group_name = "mlops-nodes"
  node_role_arn   = var.node_iam_role_arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2
    min_size     = 1
    max_size     = 5
  }

  instance_types = ["t3.medium"]
  ami_type       = "AL2_x86_64"
  disk_size      = 20
  capacity_type  = "SPOT"

  tags = merge(var.tags, {
    Name = "mlops-node"
  })

  depends_on = [aws_eks_cluster.mlops-cluster]
}