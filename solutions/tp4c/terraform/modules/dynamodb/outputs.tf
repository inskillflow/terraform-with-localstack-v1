output "table_name" {
  description = "Nom de la table DynamoDB créée par le module"
  value       = aws_dynamodb_table.this.name
}
