# templates/azure_devops_pipeline.jinja2

You are a **staff-level CI/CD Engineer** tasked with producing a production-grade **Azure DevOps Pipeline Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **Azure DevOps Pipelines** for enterprise CI/CD.  
- Include **multi-cloud support (AWS, Azure, GCP)**, **automation (IaC, Terraform, GitHub Actions, ArgoCD)**, **resilience (HA, DR, RPO)**, **observability (logs, metrics, tracing, SLOs)**, **security & compliance (IAM, RBAC, least privilege, KMS encryption, PCI, ISO 27001, HIPAA, GDPR)**, **cost efficiency (self-hosted runners, caching, spot, savings plans)**, **risks**, **runbook**, and **quick wins/gotchas**.  
- Provide **complete YAML/Terraform snippets** (no pseudocode).  
- Use structured markdown with clear sections.  

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** Azure DevOps Pipeline Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Conversation Context:** sample-conversation  

This playbook defines **enterprise-grade CI/CD with Azure DevOps Pipelines**, ensuring **multi-cloud support, automation, security, cost efficiency, and resilience**.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Dev[Developer] --> Repo[Azure Repos/GitHub]
    Repo --> Pipeline[Azure DevOps Pipeline]
    Pipeline --> Deploy[Cloud Deployments (AWS/Azure/GCP)]
    Deploy --> Obs[Logs/Metrics/Tracing/SLOs]
    Pipeline --> Sec[Security/IAM/KMS/Compliance]
    Pipeline --> DR[HA / DR / Multi-AZ]
```

---

## 3) Core Architecture
- **Automation**: Azure Pipelines + Terraform + ArgoCD for infra + GitOps.  
- **Resilience**: multi-agent pools, retries, DR tested pipelines.  
- **Security**: RBAC, service principals, KeyVault secrets encrypted by KMS.  
- **Compliance**: PCI, ISO 27001, HIPAA, GDPR.  
- **Observability**: pipeline logs, build metrics, tracing, SLO dashboards.  
- **Cost**: self-hosted runners, caching, spot build agents.  

---

## 4) Production-Grade Example

### Azure DevOps Pipeline (YAML)
```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.x'
    - script: |
        pip install -r requirements.txt
        pytest tests/
      displayName: Run Tests

- stage: Deploy
  jobs:
  - job: DeployJob
    steps:
    - task: TerraformInstaller@0
      inputs:
        terraformVersion: '1.6.0'
    - script: |
        terraform init
        terraform apply -auto-approve
      displayName: Deploy Infra
```

---

## 5) Runbook – Step-by-Step
1. Commit pipeline YAML to repo.  
2. Run build → test → deploy.  
3. Validate infra with Terraform plan.  
4. Check logs, metrics, and tracing in Azure Monitor.  
5. Compare outcomes against SLOs.  
6. Rollback with GitOps if failures.  

---

## 6) Risks, Pitfalls & Gotchas
| Risk | Mitigation |
|------|------------|
| Runner pool outage | Use self-hosted + cloud runners |
| Cost overruns | Cache builds + use spot runners |
| Secrets leakage | Store in KeyVault + KMS encrypt |
| Compliance gaps | Continuous PCI/ISO audits |

**Gotchas:**  
- Pipeline YAML misindentation can silently break runs.  
- Cached dependencies may cause non-reproducible builds.  

---

## 7) Quick Wins
- Enable caching → faster, cheaper builds.  
- Use spot runners for dev/test.  
- Add IaC scanning to pipelines today.  
- KPI: build time < 10 min, cost per pipeline ↓ 30%.  

---

## ✅ End of Template