# Add bucket to store the python code for cloud function
resource "google_storage_bucket" "function_bucket" {
  name                        = "${var.cloud_function}-function"
  location                    = var.region
  uniform_bucket_level_access = true
  labels = {
    created-by  = var.createdBy
    environment = var.enviroment
    project     = var.project_id
  }
}