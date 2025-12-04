# Use existing S3 bucket
data "aws_s3_bucket" "training_data" {
  bucket = var.training_data_bucket
}

# Use existing GitHub token secret
data "aws_secretsmanager_secret" "github_token" {
  name = "dr-github-token"
}

# Lambda function for S3 trigger
resource "aws_lambda_function" "s3_github_trigger" {
  filename         = "s3_github_trigger.zip"
  function_name    = "${var.name_prefix}-s3-github-trigger"
  role            = aws_iam_role.lambda_s3_trigger_role.arn
  handler         = "s3_github_trigger.lambda_handler"
  runtime         = "python3.11"
  timeout         = 60

  environment {
    variables = {
      GITHUB_OWNER = var.github_owner
      GITHUB_REPO  = var.github_repo
      SECRET_NAME  = "dr-github-token"
    }
  }

  depends_on = [data.archive_file.s3_trigger_zip]
}

# Package Lambda function
data "archive_file" "s3_trigger_zip" {
  type        = "zip"
  source_file = "../s3_github_trigger.py"
  output_path = "s3_github_trigger.zip"
}

# S3 Event Notification
resource "aws_s3_bucket_notification" "training_trigger" {
  bucket = data.aws_s3_bucket.training_data.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_github_trigger.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "training-data/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}

# Permission for S3 to invoke Lambda
resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.s3_github_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = data.aws_s3_bucket.training_data.arn
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_s3_trigger_role" {
  name = "${var.name_prefix}-lambda-s3-trigger-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_s3_trigger_role.name
}

resource "aws_iam_role_policy" "lambda_s3_secrets_access" {
  name = "${var.name_prefix}-lambda-s3-secrets-access"
  role = aws_iam_role.lambda_s3_trigger_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion"
        ]
        Resource = "${data.aws_s3_bucket.training_data.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:${var.aws_region}:*:secret:dr-github-token*"
      }
    ]
  })
}