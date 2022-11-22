terraform {
    backend "gcs" {
    bucket  = "tfstate-auto-tag"
    prefix  = "terraform/state"
  }
}