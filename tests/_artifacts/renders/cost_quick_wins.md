# templates/cost_quick_wins.jinja2

You are a **staff-level Cloud FinOps Engineer** tasked with producing a production-grade **Cost Optimization Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **multi-cloud**, **automation (IaC, Terraform, GitHub Actions, ArgoCD)**, **resilience (HA, multi-AZ, DR, RPO)**, **observability (logs, metrics, tracing, SLOs)**, **security & compliance (IAM, least privilege, encryption, PCI, ISO 27001, HIPAA, GDPR)**, **cost efficiency (rightsizing, spot, savings plans)**, **risks**, **runbook**, and **quick wins**.  
- Provide **complete YAML/HCL examples** (no pseudocode).  
- Use structured markdown with clear sections.

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** Cost Optimization Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Conversation Context:** sample-conversation  

This playbook outlines **immediate cost-saving opportunities** across AWS, Azure, and GCP. It applies **rightsizing, spot/preemptible usage, and savings plans**, while ensuring **HA, security, compliance, and observability**.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Cloud[Multi-Cloud: AWS/Azure/GCP] --> Compute[Rightsized Compute]
    Cloud --> Spot[Spot/Preemptible Nodes]
    Cloud --> Savings[Savings Plans/RI]
    Cloud --> Monitor[Observability: Logs/Metrics/Tracing]
    Cloud --> Sec[Security (IAM/KMS/Least Privilege)]
```

---

## 3) Core Architecture
- **Automation**: Terraform, GitHub Actions, ArgoCD for deployments.  
- **Resilience**: multi-AZ, HA clusters, DR tested with RPO/RTO.  
- **Security**: IAM least privilege, KMS encryption.  
- **Compliance**: PCI, ISO 27001, HIPAA, GDPR.  
- **Observability**: metrics, logs, tracing, SLOs.  
- **Cost**: rightsizing, spot instances, savings plans.  

---

## 4) Production-Grade Examples

### Terraform for Rightsizing
```hcl
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t3.small"
  count         = 2
}
```

### GitHub Actions for Cost Reports
```yaml
name: cost-optimization
on: [schedule]

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Fetch AWS Cost Explorer
        run: python scripts/cost_report.py
```

---

## 5) Runbook – Step-by-Step
1. Enable cost explorer & budgets in each cloud.  
2. Apply Terraform rightsizing for dev/test.  
3. Switch compute to spot/preemptible where safe.  
4. Purchase savings plans for steady workloads.  
5. Automate monthly KPI reports with GitHub Actions.  

---

## 6) Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Spot interruption | Use mixed ASGs, graceful termination |
| Under-provisioning | Rightsize only after 30 days metrics |
| Compliance gaps | Ensure budgets don’t disable critical HA |
| Savings plan lock-in | Start small (1yr, partial upfront) |

---

## 7) Quick Wins
- Immediate savings: shift non-prod to spot/preemptible.  
- Enable storage tiering to S3 IA / GCS Nearline.  
- Delete unattached volumes & idle IPs.  
- Automate KPI: **cloud cost per team per month**.  

---

## ✅ End of Template