resource "google_logging_project_sink" "auto-tag-instance" {
  name        = "${var.cloud_function}-insatnce"
  description = "Send logs to trigger a pub sub msg in order to run the cloud function which adds a tag to resource upon creation"
  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.pubsub_topic}"
  filter      = "resource.type = gce_instance AND protoPayload.response.operationType=\"insert\""

  # Use a unique writer (creates a unique service account used for writing)
  unique_writer_identity = true
}

resource "google_logging_project_sink" "auto-tag-storage" {
  name        = "${var.cloud_function}-storage"
  description = "Send logs to trigger a pub sub msg in order to run the cloud function which adds a tag to resource upon creation"
  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.pubsub_topic}"
  filter      = "resource.type=gcs_bucket AND protoPayload.methodName=\"storage.buckets.create\""

  # Use a unique writer (creates a unique service account used for writing)
  unique_writer_identity = true
}

resource "google_logging_project_sink" "auto-tag-cluster" {
  name        = "${var.cloud_function}-cluster"
  description = "Send logs to trigger a pub sub msg in order to run the cloud function which adds a tag to resource upon creation"
  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.pubsub_topic}"
  filter      = "resource.type=gke_cluster AND protoPayload.methodName=\"google.container.v1beta1.ClusterManager.CreateCluster\""

  # Use a unique writer (creates a unique service account used for writing)
  unique_writer_identity = true
}
