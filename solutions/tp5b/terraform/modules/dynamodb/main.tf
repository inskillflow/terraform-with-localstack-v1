resource "aws_dynamodb_table" "this" {
  name         = "${var.project_name}-${var.environment}-${var.table_suffix}"
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
    Module      = "dynamodb"
  }
}
