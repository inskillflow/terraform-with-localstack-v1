output "s3_bucket_name" {
  description = "Nom du bucket S3 créé dans LocalStack"
  value       = aws_s3_bucket.documents.bucket
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB créée dans LocalStack"
  value       = aws_dynamodb_table.students.name
}

output "sqs_queue_name" {
  description = "Nom de la file SQS créée dans LocalStack"
  value       = aws_sqs_queue.notifications.name
}

output "sqs_queue_url" {
  description = "URL de la file SQS créée dans LocalStack"
  value       = aws_sqs_queue.notifications.url
}

output "localstack_endpoint" {
  description = "Endpoint LocalStack utilisé par Terraform"
  value       = "http://localhost:4566"
}
