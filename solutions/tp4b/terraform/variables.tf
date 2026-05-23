variable "project_name" {
  description = "Nom du projet"
  type        = string
  default     = "tp-localstack"
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
  default     = "dev"
}

variable "owner_name" {
  description = "Responsable ou groupe"
  type        = string
  default     = "etudiant"
}
