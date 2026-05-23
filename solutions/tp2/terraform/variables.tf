variable "project_name" {
  description = "Nom du projet utilisé pour nommer les ressources locales"
  type        = string
  default     = "tp-localstack"
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
  default     = "dev"
}
