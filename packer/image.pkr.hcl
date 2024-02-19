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
  credentials_file = "./key.json"
}

build {
  sources = ["source.googlecompute.centos-stream-8"]

  provisioner "file" {
    source      = "./dependencies.sh"
    destination = "/home/packer/dependencies.sh"
  }

  provisioner "shell" {
    inline = [
      "cd /bin",
      "chmod +x ~/dependencies.sh",
      "~/dependencies.sh"
    ]
  }

  provisioner "shell" {
    inline = [
      "sudo yum install -y unzip",
      "sudo unzip /tmp/webapp-main.zip -d /home/packer/"
    ]
  }

    provisioner "shell" {
    inline = [
      "cd ~/webapp-main",
      "python3 --version",
      "pwd",
      "ls",
      "pip3 install -r app/requirements.txt"
    ]
  }

//   provisioner "file" {
//     source      = "./database.sh"
//     destination = "/tmp/database.sh"
//   }

//   provisioner "shell" {
//     inline = [
//       "chmod +x /tmp/database.sh",
//       "sudo /tmp/database.sh"
//     ]
//   }

//   provisioner "file" {
//     source      = "./user.sh"
//     destination = "/tmp/user.sh"
//   }

//   provisioner "shell" {
//     inline = [
//       "chmod +x /tmp/user.sh",
//       "sudo /tmp/user.sh"
//     ]
//   }

//   provisioner "file" {
//     source      = "./webapp-main.zip"
//     destination = "/tmp/webapp-main.zip"
//   }

//   provisioner "shell" {
//     inline = [
//       "sudo yum install -y unzip",
//       "sudo unzip /tmp/webapp-main.zip -d /tmp"
//     ]
//   }

//   provisioner "shell" {
//     inline = [
//       "echo 'Web application files ownership set.'",
//       "echo '============================================================================================================================================================================='",
//       "cd /tmp/webapp-main",
//       "python3 --version",
//       "pwd",
//       "ls",
//       "pip3.9 install -r app/requirements.txt",
//       "uvicorn app.main:app --reload"
//     ]
//   }
}



