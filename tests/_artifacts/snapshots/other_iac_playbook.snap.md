# templates/other_iac_playbook.jinja2

You are a **staff-level Cloud Engineer** tasked with producing a production-grade **IaC Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **multi-cloud infrastructure-as-code, automation, resilience, observability, security, compliance, cost, runbook, and risks**.  
- Provide **complete Terraform/YAML examples**.  
- Use structured markdown with clear sections.  

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** IaC Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Conversation Context:** sample-conversation  

This playbook defines **Infrastructure-as-Code (IaC) standards** across AWS, Azure, and GCP. It enforces **HA (multi-AZ, fault tolerant, DR tested)**, **automation with Terraform + GitHub Actions + ArgoCD**, **IAM least privilege with KMS encryption**, compliance with **PCI, ISO 27001, HIPAA, GDPR**, observability with **metrics, logs, tracing**, cost controls, a **step-by-step runbook**, and **quick wins**.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Dev[Developer] --> Repo[Git Repo]
    Repo --> CI[CI/CD (GitHub Actions)]
    CI --> Terraform[Terraform Apply]
    Terraform --> Cloud[(AWS/Azure/GCP)]
    Cloud --> Obs[Metrics/Logs/Tracing + SLOs]
    Cloud --> Sec[Security (IAM/KMS)]
    Cloud --> DR[HA / Multi-AZ / DR / RPO]
```

---

## 3) Core Architecture
- **Automation**: Terraform modules, GitHub Actions pipelines, ArgoCD for GitOps.  
- **Resilience**: multi-AZ deployments, DR tested with RPO/RTO.  
- **Security**: IAM least privilege, secrets in Vault/SM, KMS encryption.  
- **Compliance**: PCI, ISO 27001, HIPAA, GDPR.  
- **Observability**: infra metrics/logs/tracing.  
- **Cost**: rightsizing infra modules, spot nodes.  

---

## 4) Production-Grade Examples

### Terraform VPC
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "iac-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  enable_nat_gateway = true
}
```

### GitHub Actions Terraform CI
```yaml
name: terraform
on: [push]
jobs:
  plan-apply:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v2
      - run: terraform init
      - run: terraform plan
      - run: terraform apply -auto-approve
```

---

## 5) Observability & Monitoring
- Terraform drift detection logs.  
- Infra metrics dashboards.  
- SLOs: drift correction < 15m.  

---

## 6) Security & Compliance
- IAM least privilege in modules.  
- KMS encryption for secrets.  
- Compliance: PCI, ISO 27001, HIPAA, GDPR.  

---

## 7) Runbook – Step-by-Step IaC Ops
1. Push code → GitHub Actions runs plan.  
2. Peer review + approval.  
3. Apply changes with Terraform.  
4. Sync infra with ArgoCD.  
5. Monitor drift & logs.  

---

## 8) Risks, Trade-Offs & Limitations
| Risk | Mitigation |
|------|------------|
| Drift | ArgoCD auto-sync |
| Secrets leaks | KMS + Vault |
| Cost spikes | Rightsizing, spot nodes |
| Compliance gaps | PCI/ISO audits |

**Trade-Offs:**  
- Multi-cloud Terraform modules increase consistency, but add maintenance overhead.  
- ArgoCD improves drift correction but requires cluster-level access.  

**Limitations:**  
- Cross-cloud networking (AWS ↔ Azure ↔ GCP) may require custom modules.  

---

## 9) Cost Optimizations
- Rightsize Terraform module defaults.  
- Spot/preemptible nodes for dev/test.  
- KPI: $ per infra change.  

---

## 10) Quick Wins & Gotchas
- Enable drift detection today.  
- Add pre-commit Terraform fmt/validate.  
- Automate rollback runbook.  
- Weekly KPI tracking.  

**Gotchas:**  
- Forgetting `terraform lock` files causes state drift.  
- Missing lifecycle rules on buckets can drive unexpected storage costs.  

---

## ✅ End of Template