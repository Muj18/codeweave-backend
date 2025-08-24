
You are a staff-level cloud platform consultant performing a **Platform Audit**.  
The output must read like a professional report for CTOs/Engineering Directors.

Prompt: sample-prompt
Tool: Platform Audit

---
## 1) Executive Summary
- Scope: evaluate platform maturity, risks, cost efficiency, and resilience.  
- Deliverables: findings, quick wins, long-term roadmap.  
- Target: enterprise-grade reliability, security, and cost optimisation.  

---
## 2) Architecture Diagram
\`\`\`mermaid
graph TD
  Dev[Developers] -->|CI/CD| GitOps[GitOps: ArgoCD/GitHub Actions]
  GitOps -->|Deploys| K8s[Kubernetes/EKS/AKS/GKE]
  K8s -->|Logs| Observability[Prometheus/Grafana/ELK]
  K8s -->|Metrics| Observability
  K8s -->|Traces| Observability
  Cloud[Cloud Providers: AWS/Azure/GCP] --> K8s
\`\`\`

---
## 3) Multi-Cloud & Portability
- Current footprint: sample-cloud_provider.  
- Risks: lock-in, fragmented IAM, region outage exposure.  
- Mitigations:  
  - Use Terraform & Helm for cloud-agnostic provisioning.  
  - Abstract CI/CD into GitHub Actions or GitLab CI.  
  - Evaluate Crossplane or Cluster API for portability.  

---
## 4) Security & Compliance
- IAM: enforce least privilege, rotate service account keys.  
- Secrets: migrate to Vault / AWS Secrets Manager.  
- Network: apply Zero Trust, private subnets, strict SGs/NSGs.  
- Compliance: align with ISO27001, SOC2, GDPR, HIPAA.  
- Add automated policy enforcement (OPA/Gatekeeper, Kyverno).  

---
## 5) Cost Optimisation
- Rightsize clusters and VMs.  
- Replace reserved nodes with Spot/Flexible Savings Plans.  
- Enable autoscaling with guardrails.  
- Monitor per-namespace/project spend with Kubecost or CloudZero.  
- Consolidate redundant monitoring/licensing tools.  

---
## 6) Resilience & DR
- Ensure **multi-AZ deployments** across regions.  
- Validate **RPO/RTO** objectives.  
- Run chaos experiments to prove HA posture.  
- Maintain warm DR cluster or IaC blueprints for rapid rebuild.  

---
## 7) Observability
- Centralised logging (ELK, Loki, or Cloud-native).  
- Metrics with Prometheus + long-term storage (Thanos/Mimir).  
- Distributed tracing with Jaeger/Tempo.  
- SLO dashboards & error budget tracking.  
- Alert fatigue review — ensure actionable signals only.  

---
## 8) Automation & Runbooks
- Standardise Terraform modules for networking, IAM, K8s add-ons.  
- CI/CD pipelines enforce policy + security scans.  
- Create self-service portal for dev teams (reduce ops load).  
- Publish runbooks/playbooks for top 10 failure scenarios.  

---
## 9) Risks & Trade-offs
❌ Over-engineering → ✅ Simplify with CNCF “just enough” stack.  
❌ Under-investment in observability → ✅ MTTR and SLA breaches.  
❌ Cost growth with scale → ✅ introduce FinOps guardrails.  

---
## 10) Compliance & Governance
- Align with regulatory frameworks (PCI, GDPR, HIPAA).  
- Maintain evidence of controls (IaC, CI/CD logs).  
- Ensure redaction of PII in logs before SIEM ingestion.  

---
## 11) Quick Wins
- Add resource limits & liveness probes across workloads.  
- Enable autoscaling with HPA/VPA.  
- Turn on audit logging in clusters and IAM.  
- Container image scanning integrated into CI/CD.  
- Run a FinOps review → reclaim 20–30% infra spend.  

---
## 12) Roadmap
**0–3 months**: security hardening, quick cost savings, observability uplift.  
**3–6 months**: DR readiness, automation expansion, compliance alignment.  
**6–12 months**: multi-cloud abstractions, platform self-service, chaos engineering adoption.  

[END OF TEMPLATE]