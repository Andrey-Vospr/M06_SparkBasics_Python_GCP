terraform {
  backend "gcs" {}
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

provider "random" {}

resource "random_pet" "bucket_name_suffix" {
  keepers = {
    project = var.project
    region  = var.region
    zone    = var.zone
  }
}

resource "random_pet" "k8s_suffix" {
  keepers = {
    project = var.project
    region  = var.region
    zone    = var.zone
  }
}

resource "google_project_service" "container_service" {
  service                     = "container.googleapis.com"
  disable_dependent_services = true
}

resource "google_storage_bucket" "storage_bucket" {
  name          = "storage-bucket-${random_pet.bucket_name_suffix.id}"
  location      = var.location
  force_destroy = false
  storage_class = "STANDARD"
}

resource "google_container_cluster" "kubernetes_cluster" {
  name                     = "k8s-cluster-${random_pet.k8s_suffix.id}"
  location                 = var.zone
  remove_default_node_pool = true
  deletion_protection      = false
  initial_node_count       = 1

  node_config {
    machine_type = "e2-medium"
  }

  depends_on = [google_project_service.container_service]
}
