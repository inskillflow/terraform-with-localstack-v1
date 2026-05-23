resource "aws_sqs_queue" "this" {
  name = "${var.project_name}-${var.environment}-${var.queue_suffix}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_name
    ManagedBy   = "Terraform"
    Module      = "sqs"
  }
}
