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

variable "bucket_suffix" {
  description = "Suffixe du bucket S3"
  type        = string
  default     = "documents"
}
