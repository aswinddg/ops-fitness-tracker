terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "directed-bongo-452118-g3"
  region  = var.region
  zone    = var.zone
  credentials = file("credentials.json")
}

resource "google_compute_instance" "test2" {
  name         = "test2"
  machine_type = var.machine_type
  zone         = var.zone

  tags = ["dev-environment", "ops-fitness"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 40
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = "34.57.86.205"
    }
  }

  service_account {
    scopes = ["cloud-platform"]
  }

  metadata = {
    ssh-keys = "ubuntu:${file("C:/Users/Admin_TI/.ssh/id_rsa.pub")}"
  }
}