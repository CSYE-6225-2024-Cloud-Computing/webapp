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
  default = "us-central1-a"
}

variable "gcp_service_account_key" {
  type    = string
}

source "googlecompute" "centos-stream-8" {
  project_id              = var.project_id
  source_image_project_id = ["centos-cloud"]
  image_name              = "centos-8-packer-${formatdate("YYYYMMDDHHmmss", timestamp())}"
  source_image_family     = var.source_image_family
  machine_type            = "n1-standard-1"
  zone                    = var.zone
  disk_size               = 100
  disk_type               = "pd-balanced"
  network                 = "default" # Ensure this is the name of your VPC network
  image_description       = "Custom image with PostgreSQL"
  image_labels = {
    environment = "dev"
  }
  ssh_username     = "packer"
  credentials_file = var.gcp_service_account_key
}

build {
  sources = ["source.googlecompute.centos-stream-8"]

  provisioner "file" {
    source      = "../webapp-fork.zip"
    destination = "/tmp/webapp-main.zip"
  }

  provisioner "shell" {
    inline = [
      # Install unzip utility 
      "sudo dnf install -y unzip",
      # Install application dependencies and copy artifacts and configuration files
      "sudo unzip /tmp/webapp-main.zip -d /home/csye6225/", # Assuming the artifacts are in the root of the zip file
      "sudo cp /tmp/.env /home/csye6225/webapp-main/.env ",
      "echo '================================================================================================================================================'",
      "echo 'Environment file created in webapp'",
      "echo '================================================================================================================================================'",
      "sudo chown -R csye6225:csye6225 /home/csye6225/webapp-main/",
      "echo '================================================================================================================================================'",
      "echo 'Ownership of the application directory set to the dedicated user - csye6225'",
      "echo '================================================================================================================================================'",
      # Upgrade pip to the latest version
      #"sudo pip3.9 install --upgrade pip",
      "sudo pip3.9 install -r /home/csye6225/webapp-main/app/requirements.txt", # Install Python dependencies
      "echo '================================================================================================================================================'",
      "echo 'Requirements.txt installations completed.'",
      "echo '================================================================================================================================================'",
      "sudo cp /tmp/.env /home/csye6225/webapp-main/.env ",
      # Run integration tests
      "pwd",
      "sudo cd /home/csye6225/webapp-main/app/tests", # Adjust the path based on your application structure
      "sudo pip3.9 install pytest",
      "which pytest",
      "sudo -u csye6225 /bin/pytest -v integration_test.py",
      "if [ $? -eq 0 ]; then",
      "  echo 'Integration tests passed';",
      "else",
      "  echo 'Integration tests failed';",
      "  exit 1;",
      "fi",
      "echo '================================================================================================================================================'",
      "echo 'Custom image setup completed'",
      "echo '================================================================================================================================================'"
    ]
  }
}
