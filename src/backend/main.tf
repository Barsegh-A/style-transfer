provider "google" {
  credentials = file("../../../ysu-style-transfer-a5426f7b2aa2.json")
  project     = "ysu-style-transfer"
  region      = "europe-west3"
}

resource "google_compute_instance" "ml-instance" {
  name         = "ml-instance"
  machine_type = "g2-standard-4"
  zone         = "europe-west3-b"

  can_ip_forward = false

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
      size = "30"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  guest_accelerator {
    type  = "nvidia-l4"
    count = 1
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install -y nvidia-driver-535
    sudo apt install -y nvidia-utils-535
    sudo apt install -y python3
    sudo apt install -y python3-pip
    sudo apt install -y apache2
    sudo systemctl enable apache2 && sudo systemctl start apache2
    sudo apt install -y openjdk-11-jdk
    sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
        https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
    echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
        https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
        /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt update
    sudo apt install -y jenkins
    sudo systemctl start jenkins.service
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo groupadd docker
    sudo gpasswd -a $USER docker
    sudo gpasswd -a jenkins docker
    sudo service docker restart
    sudo systemctl restart jenkins
  EOF

  scheduling {
    on_host_maintenance = "TERMINATE"
  }
}

resource "google_compute_firewall" "instance" {
  name    = "terraform-example-instance"
  network = "default"

  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8000", "8080"]
  }
}
