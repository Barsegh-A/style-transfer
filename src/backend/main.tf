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
    apt-get update
    apt install nvidia-driver-535
    apt install nvidia-utils-535
    apt-get install -y python3-pip
    pip3 install torch
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
    ports    = ["80", "443", "8000"]
  }
}
