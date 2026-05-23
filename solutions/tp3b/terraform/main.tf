resource "aws_s3_bucket" "documents" {
  bucket = "${var.project_name}-${var.environment}-documents"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
  }
}

resource "aws_dynamodb_table" "students" {
  name         = "${var.project_name}-${var.environment}-students"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "student_id"

  attribute {
    name = "student_id"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
  }
}

resource "aws_sqs_queue" "notifications" {
  name = "${var.project_name}-${var.environment}-notifications"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
  }
}
