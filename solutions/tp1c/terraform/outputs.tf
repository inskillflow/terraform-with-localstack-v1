output "s3_bucket_name" {
  description = "Nom du bucket S3 créé dans LocalStack"
  value       = aws_s3_bucket.documents.bucket
}

output "dynamodb_table_name" {
  description = "Nom de la table DynamoDB créée dans LocalStack"
  value       = aws_dynamodb_table.students.name
}

output "localstack_endpoint" {
  description = "Endpoint LocalStack utilisé par Terraform"
  value       = "http://localhost:4566"
}
