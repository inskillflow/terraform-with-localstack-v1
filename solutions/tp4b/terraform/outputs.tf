output "s3_bucket_name" {
  description = "Nom du bucket S3 créé par le module s3"
  value       = module.documents_bucket.bucket_name
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB créée par le module dynamodb"
  value       = module.students_table.table_name
}

output "sqs_queue_name" {
  description = "Nom de la file SQS créée par le module sqs"
  value       = module.notifications_queue.queue_name
}

output "sqs_queue_url" {
  description = "URL de la file SQS créée par le module sqs"
  value       = module.notifications_queue.queue_url
}

output "localstack_endpoint" {
  description = "Endpoint LocalStack utilisé"
  value       = "http://localhost:4566"
}

output "project_name" {
  description = "Nom du projet"
  value       = var.project_name
}

output "environment_name" {
  description = "Nom de l'environnement"
  value       = var.environment
}

output "owner_name" {
  description = "Responsable ou groupe"
  value       = var.owner_name
}
