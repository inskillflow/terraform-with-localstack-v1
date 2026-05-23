variable "project_name" {
  description = "Nom du projet utilisé pour nommer les ressources locales"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Nom du groupe, de l'équipe ou de l'étudiant responsable"
  type        = string
}

variable "aws_region" {
  description = "Région AWS simulée par LocalStack"
  type        = string
  default     = "us-east-1"
}

variable "localstack_endpoint" {
  description = "Endpoint LocalStack"
  type        = string
  default     = "http://localhost:4566"
}
