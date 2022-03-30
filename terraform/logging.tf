resource "google_logging_project_sink" "auto-tag-instance" {
  name        = "${var.cloud_function}-insatnce"
  description = "Send logs to trigger a pub sub msg in order to run the cloud function which adds a tag to resource upon creation"
  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.pubsub_topic}"
  filter      = "resource.type = gce_instance AND protoPayload.response.operationType=\"insert\""

  # Use a unique writer (creates a unique service account used for writing)
  unique_writer_identity = true
}