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
}

build {
  sources = ["source.googlecompute.centos-stream-8"]

  provisioner "file" {
    source      = "../webapp.zip"
    destination = "/tmp/webapp.zip"
  }

  provisioner "shell" {
    inline = [
      # Install unzip utility 
      "sudo dnf install -y unzip",
      # Install application dependencies and copy artifacts and configuration files
      "sudo unzip /tmp/webapp.zip -d /home/csye6225/", # Assuming the artifacts are in the root of the zip file
      "echo '================================================================================================================================================'",
      "echo 'Unzipping Completed.",
      "echo '================================================================================================================================================'",
      # copy service file to the correct location
      "sudo cp /home/csye6225/webapp/service/webapp.service /lib/systemd/system/webapp.service",
      # User Creation Installation
      "chmod +x /home/csye6225/webapp/packer/userInstall.sh",
      "sudo /home/csye6225/webapp/packer/userInstall.sh",
      # Database Installation
      "chmod +x /home/csye6225/webapp/packer/databaseInstall.sh",
      "sudo /home/csye6225/webapp/packer/databaseInstall.sh",
      # Python Installation
      "chmod +x /home/csye6225/webapp/packer/pythonInstall.sh",
      "sudo /home/csye6225/webapp/packer/pythonInstall.sh",      
      # Pip Requirements Installation
      "sudo pip3.9 install -r /home/csye6225/webapp/app/requirements.txt", 
      "echo '================================================================================================================================================'",
      "echo 'Requirements.txt installations completed.'",
      "echo '================================================================================================================================================'",
      #give ownership permission to csye6225
      "sudo chown -R csye6225:csye6225 /home/csye6225/webapp/",
      "echo '================================================================================================================================================'",
      "echo 'Ownership of the application directory set to the dedicated user - csye6225'",
      "echo '================================================================================================================================================'",
      "echo '================================================================================================================================================'",
      "echo 'Custom image setup completed'",
      "echo '================================================================================================================================================'"
    ]
  }
}
