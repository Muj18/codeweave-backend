# templates/gha_workflow.jinja2

You are a **staff-level CI/CD Engineer** tasked with producing a production-grade **GitHub Actions Workflow Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **workflows for multi-cloud deployments** (AWS, Azure, GCP).  
- Include **automation (IaC, Terraform, ArgoCD)**, **resilience (HA runners, retries, DR)**, **observability (logs, metrics, tracing, SLOs)**, **security & compliance (IAM, least privilege, secret scanning, PCI, ISO 27001, HIPAA, GDPR)**, **cost optimization (self-hosted runners, caching, spot/savings plans)**, **risks**, **runbook**, and **quick wins**.  
- Provide **complete GitHub Actions YAML/Terraform snippets**.  
- Use structured markdown with clear sections.  

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** GitHub Actions Workflow Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Conversation Context:** sample-conversation  

This playbook defines **enterprise GitHub Actions pipelines** that are secure, resilient, observable, and cost-efficient.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Dev[Developer] --> Repo[GitHub]
    Repo --> Workflow[GitHub Actions CI/CD]
    Workflow --> Deploy[Cloud Deployments (AWS/Azure/GCP)]
    Workflow --> Sec[Secrets/IAM/KMS/Compliance]
    Workflow --> Obs[Logs/Metrics/Tracing]
    Workflow --> DR[HA / Self-Hosted Runners / DR]
```

---

## 3) Core Architecture
- **Automation**: workflows orchestrate Terraform + ArgoCD for deployments.  
- **Resilience**: HA runners, retries, DR tested.  
- **Security**: OIDC federation → IAM roles, secret scanning, RBAC.  
- **Compliance**: PCI, ISO 27001, HIPAA, GDPR.  
- **Observability**: job metrics, build duration, tracing.  
- **Cost**: cache dependencies, self-hosted spot runners.  

---

## 4) Production-Grade Examples

### GitHub Actions Workflow
```yaml
name: CI-CD

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Run Tests
      run: |
        pip install -r requirements.txt
        pytest tests/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Terraform Init & Apply
      run: |
        terraform init
        terraform apply -auto-approve
```

---

## 5) Runbook – Step-by-Step
1. Push code → GitHub triggers workflow.  
2. Run build → test → deploy.  
3. Validate deployment with Terraform plan.  
4. Check logs/metrics in GitHub + cloud.  
5. Rollback via GitOps/ArgoCD.  

---

## 6) Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Runner pool outage | Use self-hosted + GitHub runners |
| Secret leakage | OIDC + KeyVault/Secrets Manager |
| Cost overruns | Cache builds + use spot runners |
| Compliance gaps | Automated audits + logs |

---

## 7) Quick Wins
- Enable caching today → faster, cheaper builds.  
- Add IaC security scans in workflow.  
- Use OIDC federation instead of static secrets.  
- KPI: build time < 10 min, 25% cost savings.  

---

## ✅ End of Template