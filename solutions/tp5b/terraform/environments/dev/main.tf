module "documents_bucket" {
  source = "../../modules/s3"

  project_name  = var.project_name
  environment   = var.environment
  owner_name    = var.owner_name
  bucket_suffix = "documents"
}

module "students_table" {
  source = "../../modules/dynamodb"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  table_suffix = "students"
}

module "notifications_queue" {
  source = "../../modules/sqs"

  project_name = var.project_name
  environment  = var.environment
  owner_name   = var.owner_name
  queue_suffix = "notifications"
}
