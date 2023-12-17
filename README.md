# Armenian Painter Style Transfer Application
Style Transfer demo for Machine Learning Engineering course at Applied Statistics and Data Science in Yerevan State University.

Welcome to the Armenian Painter Style Transfer Application! This innovative tool allows users to apply the unique styles of famous Armenian painters to their own photographs, blending modern photography with classic artistic techniques.

![Screenshot of Application](https://i.ibb.co/JFv3npf/Screenshot-2023-12-17-174951.png)
## Features
- **Painter Selection:** Choose from a curated list of renowned Armenian painters.
- **Photo Upload:** Easily upload your photograph for style transformation.
- **Instant Transformation:** Witness the magic as your photo is reimagined in the style of your chosen painter.
- **Downloadable Results:** Save the transformed image to your device.
- **Side-by-side Comparison:** Compare the original and transformed images side-by-side.

## Setup

### Pre-requisites

- **Docker:** You need Docker installed on your system to run the application in a containerized environment. For installation instructions, visit [Docker's official website](https://www.docker.com/get-started).
- **Terraform:** Terraform is required for automating the deployment of infrastructure. To install Terraform, follow the guidelines on [Terraform's official website](https://www.terraform.io/downloads.html).

### Infrastructure
To set up the infrastructure modify the path to GCP service account file in `main.tf` credentials field accordingly and run

```
terraform init
terraform apply
```

### Run the Application
To set up the project, run

```
docker compose up
```
