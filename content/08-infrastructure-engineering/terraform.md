# Terraform

## What is Terraform?
Terraform is an **open-source IaC (Infrastructure as Code) tool** by HashiCorp that lets you define and provision infrastructure using **HCL (HashiCorp Configuration Language)** or JSON. It supports hundreds of cloud providers via **providers**.

## What is HCL?
**HashiCorp Configuration Language** — a declarative configuration language used in Terraform. Human-readable and supports variables, expressions, and functions:
```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name = "web-server"
  }
}
```

## What are the core Terraform concepts?

| Concept      | Description |
|--------------|-------------|
| **Provider** | Plugin to interact with an API (AWS, GCP, Azure, etc.) |
| **Resource** | An infrastructure component to manage (VM, VPC, DNS record) |
| **Data source** | Read existing resources not managed by Terraform |
| **Variable** | Input parameter for reusability |
| **Output** | Values exposed after `apply` |
| **Module** | Reusable, parameterized Terraform configuration |
| **State** | JSON file tracking the current state of managed resources |

## What are the core Terraform commands?
```bash
terraform init      # Initialize working directory, download providers
terraform plan      # Preview changes (dry run)
terraform apply     # Apply changes to reach desired state
terraform destroy   # Destroy all managed infrastructure
terraform validate  # Validate configuration syntax
terraform fmt       # Format code to canonical style
terraform show      # Show current state
terraform output    # Show output values
```

## What is the Terraform state file?
A **JSON file** (`terraform.tfstate`) that tracks the mapping between Terraform configuration and real infrastructure. Used to:
- Determine what changes need to be made
- Store resource metadata (IDs, attributes)
- Enable `destroy` and `refresh` operations

**Critical**: The state file can contain sensitive data. Store it securely in remote state (S3, Terraform Cloud).

## What is remote state in Terraform?
Storing the state file in a **shared, remote backend** instead of locally:
```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-locks"  # State locking
  }
}
```

## What is state locking?
Prevents **concurrent Terraform operations** from corrupting the state file. DynamoDB (AWS) or Terraform Cloud provides locking. Running `terraform apply` acquires a lock, releases it when done.

## What is a Terraform module?
A **directory of `.tf` files** that can be called like a function with inputs (variables) and outputs:
```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
  region = "us-east-1"
}
```

## What is the difference between `terraform plan` and `terraform apply`?
- `plan`: **Preview** — shows what changes would be made (create, update, destroy) without making them
- `apply`: **Execute** — makes the actual changes to infrastructure

## What is `terraform import`?
Bring **existing infrastructure** (not created by Terraform) under Terraform management:
```bash
terraform import aws_instance.web i-1234567890abcdef0
```

## What is `terraform taint`?
Mark a resource as **degraded/tainted**, forcing it to be destroyed and recreated on the next `apply`:
```bash
terraform taint aws_instance.web
```
(Replaced by `terraform apply -replace` in newer versions)

## What is the Terraform provider registry?
The **Terraform Registry** (`registry.terraform.io`) is the public repository of providers and modules. Thousands of providers are available (AWS, GCP, Azure, GitHub, Cloudflare, etc.).

## What is `terraform workspace`?
Workspaces allow **multiple state files** for the same configuration, enabling different environments (dev, staging, prod) from the same code:
```bash
terraform workspace new prod
terraform workspace select prod
```

## What is a null_resource in Terraform?
A resource with no real infrastructure backing. Used to run **local-exec or remote-exec provisioners** or as a trigger for other resources when Terraform can't directly manage something.
