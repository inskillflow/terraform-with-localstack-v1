resource "aws_s3_bucket" "this" {
  bucket = "${var.project_name}-${var.environment}-${var.bucket_suffix}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
    Module      = "s3"
  }
}
