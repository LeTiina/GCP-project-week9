terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  project = "week9-1-323806"
  region  = "us-central1"
  zone    = "us-central1-c"
}


