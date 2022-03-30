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

# Create the Cloud function triggered by a Pub/Sub
resource "google_cloudfunctions_function" "function" {
  name    = var.cloud_function
  runtime = "python39"

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name
  entry_point           = "hello_pubsub"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${var.cloud_function}"
  }

  depends_on = [
    google_storage_bucket.function_bucket, # declared in `storage.tf`
    google_storage_bucket_object.zip
  ]
}