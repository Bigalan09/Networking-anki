# Infrastructure as Code

## What is Infrastructure as Code (IaC)?
The practice of **managing and provisioning infrastructure through machine-readable configuration files** instead of manual processes. Infrastructure is treated like software — version-controlled, tested, and automated.

## What are the benefits of IaC?
- **Repeatability**: Same config produces same infrastructure every time
- **Version control**: Track changes, roll back, audit history
- **Collaboration**: Review infrastructure changes via pull requests
- **Speed**: Provision in minutes instead of hours/days
- **Documentation**: Config files document the infrastructure
- **Testing**: Validate infrastructure before applying
- **Cost reduction**: Eliminate manual errors and reduce toil

## What is the difference between mutable and immutable infrastructure?
- **Mutable**: Servers are updated in place (SSH in and change config). Configuration drift accumulates over time.
- **Immutable**: Servers are **never modified**; new images replace old ones. Eliminates drift; rollback is easy.

## What is idempotency in IaC?
An operation is **idempotent** if applying it multiple times has the same result as applying it once. IaC tools should be idempotent — re-running a playbook/plan should not cause unexpected changes.

## What are the main IaC tools and their categories?

| Tool        | Category              | Language     |
|-------------|-----------------------|--------------|
| Terraform   | Provisioning          | HCL          |
| Pulumi      | Provisioning          | TypeScript/Python/Go |
| Ansible     | Config management / provisioning | YAML |
| Chef        | Config management     | Ruby DSL     |
| Puppet      | Config management     | Puppet DSL   |
| CloudFormation | Provisioning (AWS) | YAML/JSON   |
| CDK         | Provisioning (AWS)    | TypeScript/Python |

## What is the difference between provisioning and configuration management?
- **Provisioning**: Creating infrastructure (VMs, networks, databases) — Terraform, CloudFormation
- **Configuration management**: Configuring existing servers (install packages, manage files, start services) — Ansible, Chef, Puppet

## What is declarative vs imperative IaC?
- **Declarative**: Describe the **desired end state**; the tool figures out how to get there (Terraform, CloudFormation)
- **Imperative**: Define the **steps to take** to reach the desired state (Ansible procedurally, scripts)

## What is drift in IaC?
**Configuration drift** — when actual infrastructure state differs from the IaC definition (due to manual changes, failed runs, etc.). Detected by running `terraform plan` or `ansible --check`.

## What is a dry run in IaC?
Running a tool in **check/plan mode** to see what changes would be made **without actually applying them**:
```bash
terraform plan          # Show planned changes
ansible-playbook --check  # Dry run Ansible
```

## What is GitOps?
A practice where **Git is the single source of truth** for infrastructure. Changes are made via pull requests; automation (CI/CD) applies them. The Git history is a full audit trail of infrastructure changes.

## What are the risks of IaC?
- **Misconfiguration at scale**: One bad change can affect many resources
- **Secrets in code**: Credentials accidentally committed
- **State file exposure**: Terraform state can contain sensitive data
- **Dependency complexity**: Modules with complex dependencies
- **Learning curve**: Teams need to learn new tools and practices

## What is a module in IaC?
A **reusable, parameterized unit** of IaC (Terraform module, Ansible role). Encapsulates related resources for reuse across environments.
