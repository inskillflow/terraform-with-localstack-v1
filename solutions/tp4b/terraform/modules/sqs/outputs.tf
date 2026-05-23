output "queue_name" {
  description = "Nom de la file SQS créée par le module"
  value       = aws_sqs_queue.this.name
}

output "queue_url" {
  description = "URL de la file SQS créée par le module"
  value       = aws_sqs_queue.this.url
}
