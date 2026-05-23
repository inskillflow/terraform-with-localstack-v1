variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Nom de l'environnement"
  type        = string
}

variable "owner_name" {
  description = "Responsable ou groupe"
  type        = string
}

variable "table_suffix" {
  description = "Suffixe de la table DynamoDB"
  type        = string
  default     = "students"
}
