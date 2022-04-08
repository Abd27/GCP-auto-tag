# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"

  # Append to the MD5 checksum of the files's content
  # to force the zip to be updated as soon as a change occurs
  name   = "src-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name

  depends_on = [
    google_storage_bucket.function_bucket, # declared in storage.tf
    data.archive_file.source
  ]
}

# Role for function's sercice account
resource "google_project_iam_custom_role" "custom-function-role" {
  role_id = "CustomRoleCloudFunctionAutoTag"
  title   = "auto-tag-resource-cloud-function"
  permissions = [
    "storage.buckets.get",
    "storage.buckets.update",
    "compute.disks.get",
    "compute.disks.list",
    "compute.disks.setLabels",
    "compute.instances.get",
    "compute.instances.setLabels",
    "container.clusters.get",
    "container.clusters.update"
  ]
}

# Service account for cloud function
resource "google_service_account" "function-sa" {
  account_id = "function-auto-tager-sa"
}


resource "google_project_iam_member" "member-role" {
  role    = "projects/${var.project_id}/roles/${google_project_iam_custom_role.custom-function-role.role_id}"
  member  = "serviceAccount:${google_service_account.function-sa.email}"
  project = var.project_id
}

# Create the Cloud function triggered by a Pub/Sub
resource "google_cloudfunctions_function" "function" {
  name                  = var.cloud_function
  runtime               = "python39"
  service_account_email = google_service_account.function-sa.email
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name
  entry_point           = "hello_pubsub"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${var.cloud_function}"
  }

  labels = {
    created_by  = var.createdBy
    environment = var.enviroment
    project     = var.project_id
  }

  depends_on = [
    google_storage_bucket.function_bucket, # declared in `storage.tf`
    google_storage_bucket_object.zip,
    google_service_account.function-sa
  ]
}
