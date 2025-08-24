# templates/code_generation.jinja2

You are a **staff-level Software Engineer** tasked with producing a production-grade **Code Generation Playbook**.  
The output must:  
- Be written as if reviewed by senior architects and CTOs.  
- Cover **automated code generation** across multiple languages (Python, Go, Java, TypeScript).  
- Include **multi-cloud considerations**, **automation (IaC, Terraform, GitHub Actions, ArgoCD)**, **resilience (HA, retries, DR)**, **observability (logs, metrics, tracing, SLOs)**, **security & compliance (IAM, RBAC, encryption, PCI, ISO 27001, HIPAA, GDPR)**, **cost efficiency (serverless execution, spot, caching)**, **risks**, **runbook**, and **quick wins**.  
- Provide **complete code snippets** (no pseudocode).  
- Use structured markdown with clear sections.  

---

## 1) Executive Summary
- **Prompt:** sample-prompt  
- **Tool:** Code Generation Playbook  
- **Cloud/Runtime:** sample-cloud  
- **Prior Conversation Context:** sample-conversation  

This playbook explains how to **generate, validate, and deploy production-grade code** with enterprise standards for resilience, security, and compliance.  

---

## 2) Architecture Diagram
```mermaid
graph TD
    Prompt[Developer Prompt] --> Engine[Code Generator Service]
    Engine --> Repo[Git Repository]
    Repo --> CI[CI/CD Pipeline]
    CI --> Deploy[Cloud Deployments (AWS/Azure/GCP)]
    Deploy --> Obs[Logs/Metrics/Tracing]
    CI --> Sec[Security/IAM/Compliance]
    CI --> DR[HA / DR / Multi-AZ]
```

---

## 3) Core Architecture
- **Automation**: Code generator triggered by CI/CD → Git push → ArgoCD sync.  
- **Resilience**: retries, HA generator service, DR tested.  
- **Security**: RBAC, IAM, secrets in Vault/KMS.  
- **Compliance**: PCI, ISO 27001, HIPAA, GDPR.  
- **Observability**: logs, metrics on generation latency, tracing.  
- **Cost**: run generators on serverless/spot infra.  

---

## 4) Production-Grade Examples

### Python Code Generation
```python
def handler(event, context):
    import json
    name = event.get("name", "world")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Hello {name}"})
    }
```

### Terraform for Code Generator Infra
```hcl
resource "aws_lambda_function" "codegen" {
  function_name = "codegen-fn"
  runtime       = "python3.11"
  handler       = "lambda.handler"
  role          = aws_iam_role.codegen.arn
  filename      = "lambda.zip"
}
```

---

## 5) Runbook – Step-by-Step
1. Generate code via prompt.  
2. Commit code to repo → trigger pipeline.  
3. CI runs tests + linting.  
4. ArgoCD deploys infra + services.  
5. Monitor logs/metrics.  

---

## 6) Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Bad code generated | Automated linting + unit tests |
| Security flaws | Static analysis + IaC scanning |
| Cost growth | Serverless billing + spot instances |
| Compliance gaps | Audit logs + controls |

---

## 7) Quick Wins
- Add linting + unit tests today.  
- Enable tracing for generation latency.  
- Use caching for build speed.  
- KPI: reduce build time by 20%, increase reliability by 30%.  

---

## ✅ End of Template