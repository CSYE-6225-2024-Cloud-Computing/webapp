packer {
  required_plugins {
    googlecompute = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

variable "project_id" {
  type    = string
  default = "dev-gcp-project-414615"
}

variable "source_image_family" {
  type    = string
  default = "centos-stream-8"
}

variable "zone" {
  type    = string
  default = "us-central1-f"
}
variable "disk_size" {
  type    = string
  default = 100
}

variable "disk_type" {
  type    = string
  default = "pd-balanced"
}

variable "network" {
  type    = string
  default = "default"
}

variable "machine_type" {
  type    = string
  default = "n1-standard-1"
}



source "googlecompute" "centos-stream-8" {
  project_id              = var.project_id
  source_image_project_id = ["centos-cloud"]
  image_name              = "centos-8-packer-${formatdate("YYYYMMDDHHmmss", timestamp())}"
  source_image_family     = var.source_image_family
  machine_type            = var.machine_type
  zone                    = var.zone
  disk_size               = var.disk_size
  disk_type               = var.disk_type
  network                 = var.network # Ensure this is the name of your VPC network
  image_description       = "Custom image with PostgreSQL"
  image_labels = {
    environment = "dev"
  }
  ssh_username = "packer"
}


build {
  sources = ["source.googlecompute.centos-stream-8"]

  provisioner "file" {
    source      = "../webapp.zip"
    destination = "/tmp/webapp.zip"
  }
  

  provisioner "shell" {
  script = "webapp_startup.sh"
  }

}