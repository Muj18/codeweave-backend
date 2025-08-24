
You are a **staff-level cloud engineer** writing a production-grade API Gateway playbook.  
The playbook must:  
- Be authoritative, actionable, and concise.  
- Cover AWS, Azure, and GCP equivalents.  
- Include IaC snippets, risks, compliance, and quick wins.  
- Be structured for DevOps and platform teams.  

Prompt: sample-prompt  
Tool: API Gateway (AWS / Azure API Management / GCP API Gateway)

---

## 1) Executive Summary
- Provide secure, scalable, observable API gateways.  
- Enforce authentication (JWT/OIDC, API keys).  
- Manage traffic (rate limiting, throttling).  
- Ensure compliance (PCI, SOC2, GDPR).  
- Support CI/CD-driven deployments (Terraform/ARM/Deployment Manager).  

---

## 2) Architecture Overview
- **AWS API Gateway** → integrates with Lambda/EKS/Fargate + WAF + CloudWatch.  
- **Azure API Management (APIM)** → integrates with AKS/Functions + Azure Monitor.  
- **GCP API Gateway** → integrates with Cloud Run/GKE + Cloud Armor + Cloud Logging.  

\`\`\`mermaid
flowchart LR
    Client --> Gateway[API Gateway]
    Gateway --> Auth[OIDC/AuthZ]
    Gateway --> RateLimit[Throttling/Quotas]
    Gateway --> Backend[Lambda | AKS | Cloud Run]
    Gateway --> Logs[Central Logging/SIEM]
\`\`\`

---

## 3) IaC Examples

### AWS (Terraform)
\`\`\`hcl
resource "aws_api_gateway_rest_api" "example" {
  name        = "my-api"
  description = "Production API Gateway"
}

resource "aws_api_gateway_resource" "resource" {
  rest_api_id = aws_api_gateway_rest_api.example.id
  parent_id   = aws_api_gateway_rest_api.example.root_resource_id
  path_part   = "items"
}
\`\`\`

### Azure (Bicep)
\`\`\`bicep
resource apim 'Microsoft.ApiManagement/service@2021-12-01-preview' = {
  name: 'my-apim'
  location: resourceGroup().location
  sku: { name: 'Developer', capacity: 1 }
  properties: {
    publisherEmail: 'api-team@example.com'
    publisherName: 'CodeWeave'
  }
}
\`\`\`

### GCP (YAML)
\`\`\`yaml
apiVersion: apigateway.googleapis.com/v1
kind: ApiConfig
metadata:
  name: my-config
spec:
  gateway:
    backend:
      address: https://cloud-run-service.run.app
\`\`\`

---

## 4) Runbook (Ops)

1. **Provision Gateway** (Terraform/CLI).  
2. **Configure Authentication** (JWT, API keys, or OIDC provider).  
3. **Set Rate Limits** (100 RPS per client default).  
4. **Enable Logging & Metrics** (CloudWatch, Azure Monitor, Cloud Logging).  
5. **Deploy Backends** (Lambda, AKS, Cloud Run, etc).  
6. **Test** with Postman or k6 load test.  
7. **Promote** to production via CI/CD pipeline.  

---

## 5) Observability
- Enable structured logs (JSON).  
- Collect metrics: latency, 4xx/5xx error rate, quota rejections.  
- Push traces to X-Ray (AWS), Application Insights (Azure), or Cloud Trace (GCP).  
- Alerts:  
  - High 5xx (>2% for 5 mins).  
  - Latency > p95 SLO.  
  - Exceeded quota.  

---

## 6) Risks & Trade-offs
- ❌ Vendor lock-in → ✅ mitigate with IaC + abstraction (e.g., Terraform modules).  
- ❌ Overly strict throttling → ✅ design per-client policies.  
- ❌ Exposed APIs → ✅ WAF + OAuth2 scopes.  
- ❌ Latency overhead → ✅ regional gateways + edge caching.  

---

## 7) Compliance & Governance
- Enforce TLS 1.2+ only.  
- Audit logs → centralized SIEM.  
- Data residency: deploy gateway in-region.  
- Apply API versioning + deprecation policy.  
- Mandatory review for new routes/endpoints.  

---

## 8) Quick Wins
- Use **rate-limiting defaults** before per-client overrides.  
- Add **mock integrations** for early client testing.  
- Enable **cache** for GET endpoints.  
- Automate deployment with CI/CD pipelines.  

---

## 9) Roadmap
- **0–3 months**: baseline gateway, OIDC, logging, IaC-managed.  
- **3–6 months**: multi-region failover, automated canary releases.  
- **6–12 months**: API monetization, WAF with ML anomaly detection, org-wide policy-as-code.  

[END OF TEMPLATE]