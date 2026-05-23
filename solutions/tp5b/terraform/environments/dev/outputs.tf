output "s3_bucket_name" {
  value = module.documents_bucket.bucket_name
}

output "dynamodb_table_name" {
  value = module.students_table.table_name
}

output "sqs_queue_name" {
  value = module.notifications_queue.queue_name
}

output "sqs_queue_url" {
  value = module.notifications_queue.queue_url
}

output "localstack_endpoint" {
  value = var.localstack_endpoint
}

output "aws_region" {
  value = var.aws_region
}

output "project_name" {
  value = var.project_name
}

output "environment_name" {
  value = var.environment
}

output "owner_name" {
  value = var.owner_name
}
